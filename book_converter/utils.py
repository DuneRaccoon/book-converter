"""
Utility functions for PDF conversion.
"""
import os
import re
import logging
import tempfile
from typing import Dict, Any, List, Optional, Tuple, Union
import io
import unicodedata

import fitz  # PyMuPDF
from PIL import Image

# Configure logger
logger = logging.getLogger(__name__)


def extract_images(doc: 'fitz.Document') -> List[Dict]:
    """
    Extract images from a PDF document.
    
    Args:
        doc (fitz.Document): PyMuPDF document object
        
    Returns:
        List[Dict]: List of dictionaries containing image data
    """
    images = []
    
    try:
        for page_index, page in enumerate(doc):
            image_list = page.get_images(full=True)
            
            for img_index, img_info in enumerate(image_list):
                xref = img_info[0]  # Image reference in the PDF
                
                try:
                    base_image = doc.extract_image(xref)
                    
                    if base_image:
                        image_data = {
                            'page': page_index + 1,
                            'index': img_index + 1,
                            'width': base_image.get('width', 0),
                            'height': base_image.get('height', 0),
                            'ext': base_image.get('ext', 'png'),
                            'colorspace': base_image.get('colorspace', 0),
                            'image': base_image.get('image', b'')
                        }
                        
                        # Check if the image has a reasonable size (not too small)
                        if image_data['width'] > 50 and image_data['height'] > 50:
                            images.append(image_data)
                            
                except Exception as e:
                    logger.warning(f"Failed to extract image: {e}")
                    continue
    
    except Exception as e:
        logger.error(f"Error extracting images: {e}")
        
    return images


def get_toc(doc: 'fitz.Document') -> List[Tuple[int, str, int]]:
    """
    Extract table of contents from a PDF document.
    
    Args:
        doc (fitz.Document): PyMuPDF document object
        
    Returns:
        List[Tuple[int, str, int]]: List of tuples containing (level, title, page)
    """
    toc = []
    
    try:
        pdf_toc = doc.get_toc()
        
        if pdf_toc:
            for item in pdf_toc:
                if len(item) >= 3:
                    level, title, page = item[:3]
                    if isinstance(level, int) and isinstance(title, str) and isinstance(page, int):
                        toc.append((level, title, page))
    
    except Exception as e:
        logger.error(f"Error extracting table of contents: {e}")
        
    return toc


def normalize_text(text: str) -> str:
    """
    Normalize extracted text to fix common issues.
    
    Args:
        text (str): Raw text to normalize
        
    Returns:
        str: Normalized text
    """
    if not text:
        return ""
        
    # Normalize Unicode characters
    text = unicodedata.normalize('NFC', text)
    
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Fix common OCR/PDF extraction issues
    text = text.replace('fi', 'fi')  # Fix ligatures
    text = text.replace('fl', 'fl')  # Fix ligatures
    
    # Fix paragraph breaks
    text = re.sub(r'([a-z])\s*\n\s*([a-z])', r'\1 \2', text)  # Join broken lines
    text = re.sub(r'([^.!?:])\s*\n\s*\n', r'\1\n\n', text)    # Preserve paragraph breaks
    
    # Fix hyphenation at line breaks
    text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)
    
    # Normalize whitespace at the start and end
    text = text.strip()
    
    # Remove consecutive blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text


def detect_columns(page: 'fitz.Page', threshold: float = 0.3) -> List[List[float]]:
    """
    Detect text columns in a PDF page.
    
    Args:
        page (fitz.Page): PyMuPDF page object
        threshold (float): Overlap threshold for column detection
        
    Returns:
        List[List[float]]: List of column boundaries [x0, y0, x1, y1]
    """
    # Get the blocks which represent cohesive text units
    blocks = page.get_text("blocks")
    
    if not blocks:
        return []
        
    # Extract x coordinates for each block
    x_coords = [(b[0], b[2]) for b in blocks]  # (x0, x1) for each block
    
    # Group blocks by their x coordinates to identify columns
    columns = []
    
    # This is a simplified algorithm for column detection
    # A more sophisticated algorithm would use clustering or histogram analysis
    
    # Sort blocks by x0 coordinate
    sorted_blocks = sorted(blocks, key=lambda b: b[0])
    
    # Find potential column boundaries based on x distribution
    current_column = [sorted_blocks[0][0], 0, sorted_blocks[0][2], page.rect.height]
    
    for block in sorted_blocks[1:]:
        # If this block starts significantly to the right of the current column's end
        if block[0] > current_column[2] + threshold * (page.rect.width):
            # Save the current column
            columns.append(current_column)
            # Start a new column
            current_column = [block[0], 0, block[2], page.rect.height]
        else:
            # Expand the current column if necessary
            current_column[2] = max(current_column[2], block[2])
            
    # Add the last column
    columns.append(current_column)
    
    return columns


def is_mostly_text(doc: 'fitz.Document') -> bool:
    """
    Determine if a PDF document is mostly text or mostly images.
    
    Args:
        doc (fitz.Document): PyMuPDF document object
        
    Returns:
        bool: True if the document is mostly text, False if mostly images
    """
    text_count = 0
    image_count = 0
    
    # Sample a few pages to determine content type
    sample_size = min(5, len(doc))
    sample_pages = list(range(sample_size))
    
    for page_idx in sample_pages:
        page = doc[page_idx]
        text = page.get_text()
        images = page.get_images(full=True)
        
        if len(text) > 100:  # Arbitrary threshold for "significant text"
            text_count += 1
            
        if len(images) > 2:  # Arbitrary threshold for "significant images"
            image_count += 1
    
    # If more sample pages have significant text than images, consider it text-based
    return text_count >= image_count


def compare_pdf_dimensions(doc: 'fitz.Document') -> str:
    """
    Determine if the PDF is likely a book, article, or presentation based on dimensions.
    
    Args:
        doc (fitz.Document): PyMuPDF document object
        
    Returns:
        str: Document type guess ('book', 'article', 'presentation', or 'unknown')
    """
    if len(doc) == 0:
        return "unknown"
        
    # Get dimensions of the first page
    first_page = doc[0]
    width, height = first_page.rect.width, first_page.rect.height
    
    aspect_ratio = width / height if height > 0 else 0
    
    # Make a guess based on aspect ratio and other factors
    if 0.6 <= aspect_ratio <= 0.75:  # Common book ratio
        return "book"
    elif aspect_ratio < 0.6:  # Taller than wide
        return "article"
    elif aspect_ratio > 1.3:  # Wider than tall
        return "presentation"
    else:
        return "unknown"


def sanitize_filename(name: str) -> str:
    """
    Sanitize a filename to ensure it's safe for all operating systems.
    
    Args:
        name (str): Original filename
        
    Returns:
        str: Sanitized filename
    """
    # Replace invalid characters
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, '_', name)
    
    # Trim spaces and periods from beginning and end
    sanitized = sanitized.strip('. ')
    
    # Ensure not too long
    if len(sanitized) > 255:
        sanitized = sanitized[:250] + '...'
        
    # If name would be empty, provide a default
    if not sanitized:
        sanitized = 'unnamed_file'
        
    return sanitized
