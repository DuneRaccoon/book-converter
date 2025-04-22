#!/usr/bin/env python3
"""
Example demonstrating how to use chapter patterns when converting PDFs to EPUB.
"""
import os
import sys
from pathlib import Path

# Add parent directory to the path to import the library
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from book_converter import PDFConverter, CHAPTER_PATTERNS, CHAPTER_STYLES

def main():
    """Main function to demonstrate chapter pattern detection."""
    # Replace with your PDF file path
    input_pdf = "path/to/your/file.pdf"
    
    if not os.path.exists(input_pdf):
        print(f"Error: File not found: {input_pdf}")
        print("Please update the script with a valid PDF path")
        return 1
    
    # Create output path
    output_epub = os.path.splitext(input_pdf)[0] + "_with_chapters.epub"
    
    try:
        # Initialize the converter
        print(f"Converting {input_pdf} to EPUB format with chapter detection...")
        converter = PDFConverter(input_pdf)
        
        # Print the available chapter patterns
        print("\nAvailable chapter patterns:")
        for pattern_name, pattern in CHAPTER_PATTERNS.items():
            print(f"  - {pattern_name}: {pattern}")
        
        print("\nAvailable chapter styles:")
        for style_name in CHAPTER_STYLES:
            print(f"  - {style_name}")
        
        # Using the predefined 'quoted' pattern, which matches:
        # "Chapter X: Title", quote, and ending with "~"
        # Example:
        # Chapter 3: Forge and Flame
        # "Fire reveals the truth in the heart of metal and man alike; it is both a crucible and a judge."
        # ~
        
        # Perform the conversion with custom options
        converter.to_epub(
            output_epub,
            title="My Book With Detected Chapters",
            author="Book Converter",
            language="en",
            chapter_pattern="quoted",  # Use predefined pattern
            chapter_style_name="quoted",  # Use predefined style
            toc_depth=3  # Include headings up to level 3 in the TOC
        )
        
        print(f"\nSuccessfully converted to: {output_epub}")
        print("The EPUB now has specially formatted chapter openings where the pattern was detected.")
        
        # Example with custom pattern
        print("\nExample with custom pattern:")
        custom_pattern = r"Chapter\s+\d+\.\s+[^\n]+\n"  # Matches "Chapter N. Title"
        custom_style = """
            .chapter-opening {
                margin: 3em 0;
                font-family: 'Georgia', serif;
                font-size: 1.2em;
                text-align: center;
                color: #444;
                border-bottom: 1px dotted #999;
                padding-bottom: 1em;
            }
        """
        
        output_custom = os.path.splitext(input_pdf)[0] + "_custom_chapters.epub"
        
        converter.to_epub(
            output_custom,
            title="My Book With Custom Chapter Detection",
            chapter_pattern=custom_pattern,
            chapter_style=custom_style
        )
        
        print(f"Successfully created second EPUB with custom pattern: {output_custom}")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
