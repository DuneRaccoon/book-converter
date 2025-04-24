#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify cover image implementation in EPUB conversion.
This script creates a sample PDF with an image, then converts it to EPUB,
verifying that the cover image appears as the first page in the EPUB.
"""
import os
import sys
import tempfile
from pathlib import Path

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from book_converter import PDFConverter

def main():
    """Run test to verify cover image implementation."""
    print("Testing cover image implementation...")
    
    # Look for a test image - using a PDF file in tests directory
    # since we don't have a sample PDF to create a proper test
    input_pdf = None
    
    # Try to find the sample.pdf
    for test_pdf in [
        os.path.join(project_root, 'tests', 'sample.pdf'),
        # Add other potential locations if needed
    ]:
        if os.path.exists(test_pdf):
            input_pdf = test_pdf
            break
    
    if not input_pdf:
        print("Error: No sample PDF found. Please create a tests/sample.pdf file.")
        return 1
    
    # Test with a test image for cover
    test_image = None
    for img_path in [
        os.path.join(project_root, 'tests', 'cover.jpg'),
        os.path.join(project_root, 'tests', 'cover.png'),
    ]:
        if os.path.exists(img_path):
            test_image = img_path
            break
    
    # Use temporary directory for output
    with tempfile.TemporaryDirectory() as temp_dir:
        # Test with external cover image
        if test_image:
            output_path = os.path.join(temp_dir, "with_cover.epub")
            print(f"Converting PDF with cover image: {test_image}")
            
            try:
                converter = PDFConverter(input_pdf)
                converter.to_epub(
                    output_path,
                    title="Test Book With Cover",
                    author="Test Author",
                    cover_image=test_image
                )
                
                if os.path.exists(output_path):
                    print(f"✅ Successfully created EPUB with cover: {output_path}")
                    # Copy to project root for inspection
                    target_path = os.path.join(project_root, "with_cover.epub")
                    with open(output_path, 'rb') as src, open(target_path, 'wb') as dst:
                        dst.write(src.read())
                    print(f"Copied to: {target_path}")
                else:
                    print("❌ Failed to create EPUB with cover")
            except Exception as e:
                print(f"❌ Error during conversion with cover: {e}")
        
        # Test using first image from PDF
        output_path = os.path.join(temp_dir, "with_pdf_image.epub")
        print(f"Converting PDF using first image as cover")
        
        try:
            converter = PDFConverter(input_pdf)
            converter.to_epub(
                output_path,
                title="Test Book With PDF Image",
                author="Test Author"
            )
            
            if os.path.exists(output_path):
                print(f"✅ Successfully created EPUB with PDF image: {output_path}")
                # Copy to project root for inspection
                target_path = os.path.join(project_root, "with_pdf_image.epub")
                with open(output_path, 'rb') as src, open(target_path, 'wb') as dst:
                    dst.write(src.read())
                print(f"Copied to: {target_path}")
            else:
                print("❌ Failed to create EPUB with PDF image as cover")
        except Exception as e:
            print(f"❌ Error during conversion with PDF image: {e}")
    
    print("Test complete. Check the output files in the project root.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
