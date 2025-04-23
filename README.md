# Book Converter

A PDF conversion tool that can transform PDF files into various formats including EPUB, HTML, TXT, DOCX, and Markdown.

## Features

- Convert PDF files to multiple formats:
  - EPUB (.epub)
  - HTML (.html)
  - Markdown (.md)
  - Plain text (.txt)
  - Word document (.docx)
  - MOBI (.mobi) - requires Calibre's ebook-convert
- Preserve formatting, images, and tables when possible
- Batch conversion of multiple files
- Command-line interface for easy automation
- Python API for integration into other applications
- Customizable conversion options

## Installation

### From PyPI
```bash
pip install book-converter
```

### From Source
```bash
git clone https://github.com/yourusername/book-converter.git
cd book-converter
pip install -e .
```

## Quick Start

### Command Line Usage
```bash
# Convert a PDF to EPUB
book-converter convert input.pdf --output output.epub

# Convert a PDF to DOCX
book-converter convert input.pdf --output output.docx

# Batch conversion
book-converter convert *.pdf --output-dir converted --format epub
```

### Python API
```python
from book_converter import PDFConverter

# Initialize converter
converter = PDFConverter("input.pdf")

# Convert to EPUB
converter.to_epub("output.epub")

# Or convert with custom options
converter.to_epub(
    "output.epub",
    title="My Book",
    author="John Doe",
    cover_image="cover.jpg"
)
```

## MOBI Conversion Note

MOBI conversion requires Calibre's `ebook-convert` command-line tool to be installed and available in your PATH. If Calibre is not installed, the converter will fall back to creating an EPUB file with a .mobi extension.

To install Calibre:
- Visit [Calibre's download page](https://calibre-ebook.com/download)
- Follow the installation instructions for your operating system
- Make sure the `ebook-convert` tool is available in your system PATH

## Documentation

For more detailed documentation, see the [docs](docs/) directory:

- [Installation Guide](docs/installation.md)
- [Usage Guide](docs/usage.md)
- [API Reference](docs/api.md)
- [Examples](docs/examples.md)
- [Troubleshooting](docs/troubleshooting.md)

## Requirements

- Python 3.7+
- PyMuPDF (fitz)
- ebooklib
- python-docx
- Pillow
- BeautifulSoup4
- lxml
- Calibre (optional, for MOBI conversion)

See requirements.txt for all dependencies.

## License

MIT License
