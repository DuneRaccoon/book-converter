"""
Core PDF converter class for the book-converter package.
"""
import os
import logging
from typing import Dict, Any, List, Optional, Tuple, Union
from pathlib import Path

import fitz  # PyMuPDF

from .formats import (
    EPUBConverter,
    DOCXConverter,
    HTMLConverter,
    TextConverter,
    MarkdownConverter,
    MOBIConverter,
)
from .utils import extract_images, get_toc, normalize_text, detect_columns

# Configure logger
logger = logging.getLogger(__name__)


class PDFConverter:
    """
    Main converter class for handling PDF conversion to various formats.
    
    Attributes:
        pdf_path (str): Path to the input PDF file
        doc (fitz.Document): PyMuPDF document object
        metadata (Dict[str, str]): Extracted metadata from the PDF
        pages (List[fitz.Page]): List of PDF pages
        images (List[Dict]): List of extracted images
        toc (List[Tuple]): Table of contents extracted from the PDF
    """

    def __init__(self, pdf_path: str, password: Optional[str] = None):
        """
        Initialize the PDFConverter with a PDF file.
        
        Args:
            pdf_path (str): Path to the input PDF file
            password (Optional[str]): Password for encrypted PDFs
        
        Raises:
            FileNotFoundError: If the PDF file doesn't exist
            ValueError: If the file is not a valid PDF
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        self.pdf_path = pdf_path
        
        try:
            self.doc = fitz.open(pdf_path)
            if self.doc.needs_pass and password:
                auth_success = self.doc.authenticate(password)
                if not auth_success:
                    raise ValueError("Incorrect password for encrypted PDF")
            elif self.doc.needs_pass and not password:
                raise ValueError("PDF is encrypted, password required")
                
            # Extract basic metadata
            self.metadata = self._extract_metadata()
            self.pages = [page for page in self.doc]
            self.images = extract_images(self.doc)
            self.toc = get_toc(self.doc)
            
            logger.info(f"Successfully loaded PDF: {pdf_path}")
            logger.info(f"Pages: {len(self.pages)}")
            logger.info(f"Images: {len(self.images)}")
            
        except Exception as e:
            logger.error(f"Error opening PDF: {e}")
            raise ValueError(f"Could not open PDF file: {e}")
    
    def _extract_metadata(self) -> Dict[str, str]:
        """
        Extract metadata from the PDF file.
        
        Returns:
            Dict[str, str]: Dictionary of metadata
        """
        metadata = {
            "title": self.doc.metadata.get("title", ""),
            "author": self.doc.metadata.get("author", ""),
            "subject": self.doc.metadata.get("subject", ""),
            "keywords": self.doc.metadata.get("keywords", ""),
            "creator": self.doc.metadata.get("creator", ""),
            "producer": self.doc.metadata.get("producer", ""),
            "page_count": len(self.doc),
        }
        
        # Clean up empty metadata fields
        return {k: v for k, v in metadata.items() if v}
    
    def extract_text(self, include_tables: bool = True, detect_columns: bool = True, preserve_style: bool = True) -> List[str]:
        """
        Extract text content from each page of the PDF.
        
        Args:
            include_tables (bool): Whether to extract tables as structured text
            detect_columns (bool): Whether to try to detect and handle columns
            
        Returns:
            List[str]: List of text content for each page
        """
        text_by_page = []
    
        for page_num, page in enumerate(self.pages):
            if detect_columns:
                text = self._extract_columns(page)
            else:
                # Use raw text extraction to preserve more formatting details
                text = page.get_text()
            
            # Use the enhanced normalization with style preservation
            text = normalize_text(text, preserve_style=preserve_style)
            text_by_page.append(text)
            
        return text_by_page
    
    def _extract_columns(self, page: 'fitz.Page') -> str:
        """
        Extract text from a page with column detection.
        
        Args:
            page (fitz.Page): PDF page object
            
        Returns:
            str: Extracted text with columns properly handled
        """
        # Implementation detail: This would use algorithms to detect columns
        # and reconstruct the proper reading order.
        # For now, we use a simplified approach
        blocks = page.get_text("blocks")
        blocks.sort(key=lambda b: (int(b[1] / 20), b[0]))  # Sort by y then x
        return "\n".join(b[4] for b in blocks)
    
    def to_epub(self, output_path: str, **kwargs) -> str:
        """
        Convert the PDF to EPUB format.
        
        Args:
            output_path (str): Path to save the output EPUB file
            **kwargs: Additional options for the EPUB conversion
            
        Returns:
            str: Path to the output EPUB file
            
        Raises:
            ValueError: If conversion fails
        """
        converter = EPUBConverter(self)
        return converter.convert(output_path, **kwargs)
    
    def to_docx(self, output_path: str, **kwargs) -> str:
        """
        Convert the PDF to DOCX format.
        
        Args:
            output_path (str): Path to save the output DOCX file
            **kwargs: Additional options for the DOCX conversion
            
        Returns:
            str: Path to the output DOCX file
            
        Raises:
            ValueError: If conversion fails
        """
        converter = DOCXConverter(self)
        return converter.convert(output_path, **kwargs)
    
    def to_html(self, output_path: str, **kwargs) -> str:
        """
        Convert the PDF to HTML format.
        
        Args:
            output_path (str): Path to save the output HTML file
            **kwargs: Additional options for the HTML conversion
            
        Returns:
            str: Path to the output HTML file
            
        Raises:
            ValueError: If conversion fails
        """
        converter = HTMLConverter(self)
        return converter.convert(output_path, **kwargs)
    
    def to_text(self, output_path: str, **kwargs) -> str:
        """
        Convert the PDF to plain text format.
        
        Args:
            output_path (str): Path to save the output text file
            **kwargs: Additional options for the text conversion
            
        Returns:
            str: Path to the output text file
            
        Raises:
            ValueError: If conversion fails
        """
        converter = TextConverter(self)
        return converter.convert(output_path, **kwargs)
    
    def to_markdown(self, output_path: str, **kwargs) -> str:
        """
        Convert the PDF to Markdown format.
        
        Args:
            output_path (str): Path to save the output Markdown file
            **kwargs: Additional options for the Markdown conversion
            
        Returns:
            str: Path to the output Markdown file
            
        Raises:
            ValueError: If conversion fails
        """
        converter = MarkdownConverter(self)
        return converter.convert(output_path, **kwargs)
    
    def to_mobi(self, output_path: str, **kwargs) -> str:
        """
        Convert the PDF to MOBI format.
        
        Args:
            output_path (str): Path to save the output MOBI file
            **kwargs: Additional options for the MOBI conversion
            
        Returns:
            str: Path to the output MOBI file
            
        Raises:
            ValueError: If conversion fails
        """
        converter = MOBIConverter(self)
        return converter.convert(output_path, **kwargs)
    
    def batch_convert(self, output_dir: str, formats: List[str], **kwargs) -> Dict[str, str]:
        """
        Convert the PDF to multiple formats at once.
        
        Args:
            output_dir (str): Directory to save the output files
            formats (List[str]): List of formats to convert to
            **kwargs: Additional options for the conversions
            
        Returns:
            Dict[str, str]: Dictionary mapping formats to output paths
            
        Raises:
            ValueError: If an invalid format is specified
        """
        os.makedirs(output_dir, exist_ok=True)
        
        output_paths = {}
        
        # Get base filename without extension
        base_filename = os.path.splitext(os.path.basename(self.pdf_path))[0]
        
        for fmt in formats:
            fmt = fmt.lower().strip('.')
            output_path = os.path.join(output_dir, f"{base_filename}.{fmt}")
            
            try:
                if fmt == 'epub':
                    output_paths[fmt] = self.to_epub(output_path, **kwargs)
                elif fmt == 'docx':
                    output_paths[fmt] = self.to_docx(output_path, **kwargs)
                elif fmt == 'html':
                    output_paths[fmt] = self.to_html(output_path, **kwargs)
                elif fmt == 'txt':
                    output_paths[fmt] = self.to_text(output_path, **kwargs)
                elif fmt == 'md':
                    output_paths[fmt] = self.to_markdown(output_path, **kwargs)
                elif fmt == 'mobi':
                    output_paths[fmt] = self.to_mobi(output_path, **kwargs)
                else:
                    raise ValueError(f"Unsupported format: {fmt}")
                    
                logger.info(f"Successfully converted to {fmt}: {output_path}")
                
            except Exception as e:
                logger.error(f"Error converting to {fmt}: {e}")
                
        return output_paths
    
    def __del__(self):
        """Close the PDF document when the converter is garbage collected."""
        if hasattr(self, 'doc') and self.doc:
            try:
                self.doc.close()
            except:
                pass
