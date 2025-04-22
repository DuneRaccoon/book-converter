#!/usr/bin/env python3
"""
Simple example of converting a PDF to EPUB format.
"""
import os
import sys
from pathlib import Path

# Add parent directory to the path to import the library
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from book_converter import PDFConverter

def main():
    """Main function to demonstrate PDF to EPUB conversion."""
    # Replace with your PDF file path
    input_pdf = "path/to/your/file.pdf"
    
    if not os.path.exists(input_pdf):
        print(f"Error: File not found: {input_pdf}")
        print("Please update the script with a valid PDF path")
        return 1
    
    # Create output path
    output_epub = os.path.splitext(input_pdf)[0] + ".epub"
    
    try:
        # Initialize the converter
        print(f"Converting {input_pdf} to EPUB format...")
        converter = PDFConverter(input_pdf)
        
        # Get some info about the PDF
        print(f"PDF has {len(converter.pages)} pages")
        print(f"Metadata: {converter.metadata}")
        
        # Perform the conversion with custom options
        converter.to_epub(
            output_epub,
            title="My Converted Book",
            author="Book Converter",
            language="en",
            toc_depth=3  # Include headings up to level 3 in the TOC
        )
        
        print(f"Successfully converted to: {output_epub}")
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
