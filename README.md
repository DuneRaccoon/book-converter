# Book Converter

A powerful, production-ready PDF conversion tool that can transform PDF files into various formats including EPUB, MOBI, HTML, TXT, DOCX, and more.

## Features

- Convert PDF files to multiple formats:
  - EPUB (.epub)
  - HTML (.html)
  - Markdown (.md)
  - Plain text (.txt)
  - Word document (.docx)
  - Mobi (.mobi)
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
git clone https://github.com/duneraccoon/book-converter.git
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
book-converter convert *.pdf --output-dir converted_books --format epub
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

## Documentation

For more detailed documentation, see the [docs](docs/) directory:

- [Installation Guide](docs/installation.md)
- [Usage Guide](docs/usage.md)
- [API Reference](docs/api.md)
- [Examples](docs/examples.md)
- [Troubleshooting](docs/troubleshooting.md)

## Requirements

- Python 3.7+
- See requirements.txt for dependencies

## License

MIT License
