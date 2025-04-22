#!/usr/bin/env python3
"""
Example of batch converting multiple PDF files to various formats.
"""
import os
import sys
import glob
from pathlib import Path

# Add parent directory to the path to import the library
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from book_converter import PDFConverter

def main():
    """Main function to demonstrate batch PDF conversion."""
    # Directory containing PDF files
    input_dir = "path/to/your/pdfs"
    
    # Output directory for converted files
    output_dir = "path/to/your/output"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all PDF files in the input directory
    pdf_files = glob.glob(os.path.join(input_dir, "*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in: {input_dir}")
        return 1
    
    print(f"Found {len(pdf_files)} PDF files to convert")
    
    # Convert each PDF to multiple formats
    for pdf_file in pdf_files:
        try:
            # Get base filename without extension
            base_name = os.path.splitext(os.path.basename(pdf_file))[0]
            print(f"\nProcessing: {pdf_file}")
            
            # Initialize the converter
            converter = PDFConverter(pdf_file)
            
            # Convert to multiple formats
            formats = ["epub", "txt", "html"]
            results = converter.batch_convert(
                output_dir,
                formats,
                include_images=True,
                detect_columns=True
            )
            
            # Print results
            for fmt, output_path in results.items():
                print(f"  Converted to {fmt.upper()}: {output_path}")
                
        except Exception as e:
            print(f"  Error processing {pdf_file}: {e}")
    
    print("\nBatch conversion completed")
    return 0

if __name__ == "__main__":
    sys.exit(main())
