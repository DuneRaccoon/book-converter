"""
Command-line interface for book-converter.
"""
import os
import sys
import logging
import argparse
from typing import List, Optional
from pathlib import Path
import glob

from . import __version__
from .converter import PDFConverter

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Args:
        args (Optional[List[str]]): Command-line arguments
        
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='Convert PDF files to various formats',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  book-converter convert input.pdf --output output.epub
  book-converter convert input.pdf --output output.docx --title "My Book"
  book-converter batch *.pdf --output-dir converted --format epub,docx
'''
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    subparsers.required = True
    
    # 'convert' command for single file conversion
    convert_parser = subparsers.add_parser(
        'convert',
        help='Convert a single PDF file'
    )
    convert_parser.add_argument(
        'input',
        help='Input PDF file'
    )
    convert_parser.add_argument(
        '--output', '-o',
        required=True,
        help='Output file with extension (.epub, .docx, .html, .txt, .md, .mobi)'
    )
    convert_parser.add_argument(
        '--password',
        help='Password for encrypted PDF'
    )
    convert_parser.add_argument(
        '--title',
        help='Title for the output document'
    )
    convert_parser.add_argument(
        '--author',
        help='Author for the output document'
    )
    convert_parser.add_argument(
        '--language', '-l',
        default='en',
        help='Language code (default: en)'
    )
    convert_parser.add_argument(
        '--cover-image',
        help='Path to cover image file'
    )
    convert_parser.add_argument(
        '--include-images',
        action='store_true',
        default=True,
        help='Include images in the output (default: True)'
    )
    convert_parser.add_argument(
        '--no-images',
        action='store_false',
        dest='include_images',
        help='Exclude images from the output'
    )
    convert_parser.add_argument(
        '--detect-columns',
        action='store_true',
        default=True,
        help='Detect columns in the PDF (default: True)'
    )
    convert_parser.add_argument(
        '--no-detect-columns',
        action='store_false',
        dest='detect_columns',
        help='Disable column detection'
    )
    convert_parser.add_argument(
        '--toc-depth',
        type=int,
        default=3,
        help='Maximum depth for table of contents (default: 3)'
    )
    convert_parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    # 'batch' command for batch conversion
    batch_parser = subparsers.add_parser(
        'batch',
        help='Convert multiple PDF files'
    )
    batch_parser.add_argument(
        'inputs',
        nargs='+',
        help='Input PDF files (supports wildcards)'
    )
    batch_parser.add_argument(
        '--output-dir', '-o',
        required=True,
        help='Output directory'
    )
    batch_parser.add_argument(
        '--format', '-f',
        required=True,
        help='Output format(s) as comma-separated list (epub,docx,html,txt,md,mobi)'
    )
    batch_parser.add_argument(
        '--password',
        help='Password for encrypted PDFs (applied to all)'
    )
    batch_parser.add_argument(
        '--include-images',
        action='store_true',
        default=True,
        help='Include images in the output (default: True)'
    )
    batch_parser.add_argument(
        '--no-images',
        action='store_false',
        dest='include_images',
        help='Exclude images from the output'
    )
    batch_parser.add_argument(
        '--detect-columns',
        action='store_true',
        default=True,
        help='Detect columns in the PDF (default: True)'
    )
    batch_parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    return parser.parse_args(args)


def validate_output_format(output_path: str) -> str:
    """
    Validate the output format based on the file extension.
    
    Args:
        output_path (str): Output path with extension
        
    Returns:
        str: Validated format
        
    Raises:
        ValueError: If the format is not supported
    """
    ext = os.path.splitext(output_path)[1].lower()
    
    supported_formats = {
        '.epub': 'epub',
        '.docx': 'docx',
        '.html': 'html',
        '.htm': 'html',
        '.txt': 'text',
        '.md': 'markdown',
        '.mobi': 'mobi'
    }
    
    if ext not in supported_formats:
        raise ValueError(
            f"Unsupported output format: {ext}\n"
            f"Supported formats: {', '.join(supported_formats.keys())}"
        )
        
    return supported_formats[ext]


def convert_single_file(args: argparse.Namespace) -> int:
    """
    Convert a single PDF file.
    
    Args:
        args (argparse.Namespace): Parsed arguments
        
    Returns:
        int: Exit code
    """
    try:
        input_path = args.input
        output_path = args.output
        
        # Check if input file exists
        if not os.path.exists(input_path):
            logger.error(f"Input file not found: {input_path}")
            return 1
            
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            
        # Validate output format
        format_name = validate_output_format(output_path)
        
        # Set log level
        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
            
        # Initialize the converter
        logger.info(f"Converting {input_path} to {format_name.upper()}")
        converter = PDFConverter(input_path, password=args.password)
        
        # Prepare conversion options
        options = {
            'include_tables': True,
            'detect_columns': args.detect_columns,
            'include_images': args.include_images,
            'toc_depth': args.toc_depth
        }
        
        # Add optional parameters if provided
        if args.title:
            options['title'] = args.title
        if args.author:
            options['author'] = args.author
        if args.language:
            options['language'] = args.language
        if args.cover_image:
            options['cover_image'] = args.cover_image
            
        # Perform the conversion
        if format_name == 'epub':
            converter.to_epub(output_path, **options)
        elif format_name == 'docx':
            converter.to_docx(output_path, **options)
        elif format_name == 'html':
            converter.to_html(output_path, **options)
        elif format_name == 'text':
            converter.to_text(output_path, **options)
        elif format_name == 'markdown':
            converter.to_markdown(output_path, **options)
        elif format_name == 'mobi':
            converter.to_mobi(output_path, **options)
            
        logger.info(f"Successfully converted to {output_path}")
        return 0
        
    except Exception as e:
        logger.error(f"Error during conversion: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def batch_convert_files(args: argparse.Namespace) -> int:
    """
    Convert multiple PDF files.
    
    Args:
        args (argparse.Namespace): Parsed arguments
        
    Returns:
        int: Exit code
    """
    try:
        # Set log level
        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
            
        # Create output directory
        os.makedirs(args.output_dir, exist_ok=True)
        
        # Parse formats
        formats = [fmt.strip().lower() for fmt in args.format.split(',')]
        for fmt in formats:
            if fmt not in ('epub', 'docx', 'html', 'txt', 'md', 'mobi'):
                logger.error(f"Unsupported format: {fmt}")
                return 1
                
        # Collect input files
        input_files = []
        for input_pattern in args.inputs:
            matched_files = glob.glob(input_pattern)
            input_files.extend([f for f in matched_files if f.lower().endswith('.pdf')])
            
        if not input_files:
            logger.error("No PDF files found matching the input pattern(s)")
            return 1
            
        # Convert each file
        logger.info(f"Found {len(input_files)} PDF files to convert")
        
        success_count = 0
        for input_path in input_files:
            try:
                # Get base filename without extension
                base_filename = os.path.splitext(os.path.basename(input_path))[0]
                
                logger.info(f"Converting {input_path}")
                
                # Initialize the converter
                converter = PDFConverter(input_path, password=args.password)
                
                # Prepare conversion options
                options = {
                    'include_tables': True,
                    'detect_columns': args.detect_columns,
                    'include_images': args.include_images
                }
                
                # Convert to each requested format
                for fmt in formats:
                    output_path = os.path.join(args.output_dir, f"{base_filename}.{fmt}")
                    
                    try:
                        if fmt == 'epub':
                            converter.to_epub(output_path, **options)
                        elif fmt == 'docx':
                            converter.to_docx(output_path, **options)
                        elif fmt == 'html':
                            converter.to_html(output_path, **options)
                        elif fmt == 'txt':
                            converter.to_text(output_path, **options)
                        elif fmt == 'md':
                            converter.to_markdown(output_path, **options)
                        elif fmt == 'mobi':
                            converter.to_mobi(output_path, **options)
                            
                        logger.info(f"Successfully converted to {output_path}")
                        
                    except Exception as format_error:
                        logger.error(f"Error converting {input_path} to {fmt}: {format_error}")
                        
                success_count += 1
                
            except Exception as file_error:
                logger.error(f"Error processing {input_path}: {file_error}")
                if args.verbose:
                    import traceback
                    traceback.print_exc()
                    
        logger.info(f"Successfully converted {success_count} out of {len(input_files)} files")
        
        return 0 if success_count > 0 else 1
        
    except Exception as e:
        logger.error(f"Error during batch conversion: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the CLI.
    
    Args:
        args (Optional[List[str]]): Command-line arguments
        
    Returns:
        int: Exit code
    """
    try:
        parsed_args = parse_args(args)
        
        if parsed_args.command == 'convert':
            return convert_single_file(parsed_args)
        elif parsed_args.command == 'batch':
            return batch_convert_files(parsed_args)
        else:
            logger.error(f"Unknown command: {parsed_args.command}")
            return 1
            
    except Exception as e:
        logger.error(f"Unhandled error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
