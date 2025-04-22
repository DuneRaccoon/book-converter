# Usage Guide

This guide provides detailed instructions on how to use Book Converter for both command-line operations and as a Python library.

## Command-Line Interface

Book Converter provides a comprehensive command-line interface for converting PDF files to various formats.

### Basic Syntax

```bash
book-converter <command> [options]
```

Available commands:
- `convert`: Convert a single PDF file
- `batch`: Convert multiple PDF files

### Converting a Single PDF

To convert a single PDF file:

```bash
book-converter convert input.pdf --output output.epub
```

#### Options for Single Conversion

| Option | Description |
|--------|-------------|
| `--output`, `-o` | Output file path (required) |
| `--password` | Password for encrypted PDFs |
| `--title` | Set title for the output document |
| `--author` | Set author for the output document |
| `--language`, `-l` | Language code (default: en) |
| `--cover-image` | Path to cover image file |
| `--include-images` | Include images in the output (default: True) |
| `--no-images` | Exclude images from the output |
| `--detect-columns` | Detect columns in the PDF (default: True) |
| `--no-detect-columns` | Disable column detection |
| `--toc-depth` | Maximum depth for table of contents (default: 3) |
| `--verbose`, `-v` | Enable verbose output |

### Batch Converting Multiple PDFs

To convert multiple PDF files at once:

```bash
book-converter batch *.pdf --output-dir converted --format epub,docx
```

#### Options for Batch Conversion

| Option | Description |
|--------|-------------|
| `--output-dir`, `-o` | Output directory (required) |
| `--format`, `-f` | Output format(s) as comma-separated list (required) |
| `--password` | Password for encrypted PDFs (applied to all) |
| `--include-images` | Include images in the output (default: True) |
| `--no-images` | Exclude images from the output |
| `--detect-columns` | Detect columns in the PDF (default: True) |
| `--verbose`, `-v` | Enable verbose output |

### Examples

Convert a PDF to EPUB with a custom title and author:

```bash
book-converter convert mybook.pdf --output mybook.epub --title "My Amazing Book" --author "Jane Doe"
```

Convert all PDFs in a directory to both EPUB and DOCX formats:

```bash
book-converter batch *.pdf --output-dir converted --format epub,docx
```

Convert a password-protected PDF:

```bash
book-converter convert secret.pdf --output secret.epub --password "mypassword"
```

Convert a PDF without including images:

```bash
book-converter convert document.pdf --output document.md --no-images
```

## Python API

Book Converter can also be used as a Python library in your own scripts.

### Basic Usage

```python
from book_converter import PDFConverter

# Initialize the converter with a PDF file
converter = PDFConverter("input.pdf")

# Convert to EPUB
converter.to_epub("output.epub")

# Or convert to DOCX
converter.to_docx("output.docx")
```

### Conversion with Custom Options

```python
from book_converter import PDFConverter

# Initialize the converter
converter = PDFConverter("input.pdf")

# Convert to EPUB with custom options
converter.to_epub(
    "output.epub",
    title="Custom Title",
    author="Author Name",
    language="en",
    cover_image="path/to/cover.jpg",
    toc_depth=2
)
```

### Batch Conversion to Multiple Formats

```python
from book_converter import PDFConverter

# Initialize the converter
converter = PDFConverter("input.pdf")

# Convert to multiple formats at once
results = converter.batch_convert(
    output_dir="converted",
    formats=["epub", "docx", "txt"],
    include_images=True,
    detect_columns=True
)

# The results dictionary maps formats to output paths
for fmt, path in results.items():
    print(f"Converted to {fmt}: {path}")
```

### Working with Encrypted PDFs

```python
from book_converter import PDFConverter

# Initialize with a password for encrypted PDFs
converter = PDFConverter("encrypted.pdf", password="mypassword")

# Convert normally
converter.to_epub("output.epub")
```

### Accessing PDF Metadata and Content

```python
from book_converter import PDFConverter

# Initialize the converter
converter = PDFConverter("input.pdf")

# Access metadata
print(f"Title: {converter.metadata.get('title', 'Unknown')}")
print(f"Author: {converter.metadata.get('author', 'Unknown')}")
print(f"Number of pages: {len(converter.pages)}")

# Extract text content
text_by_page = converter.extract_text()
for i, page_text in enumerate(text_by_page):
    print(f"Page {i+1} preview: {page_text[:100]}...")

# Access images
print(f"Number of images: {len(converter.images)}")
```

## Supported Output Formats

Book Converter supports the following output formats:

| Format | Extension | Method | Description |
|--------|-----------|--------|-------------|
| EPUB | `.epub` | `to_epub()` | E-book format for most e-readers |
| DOCX | `.docx` | `to_docx()` | Microsoft Word document |
| HTML | `.html` | `to_html()` | Web page format |
| Text | `.txt` | `to_text()` | Plain text format |
| Markdown | `.md` | `to_markdown()` | Markdown format |

## Advanced Usage

### Customizing EPUB Output

```python
converter.to_epub(
    "output.epub",
    title="My Book",
    author="Author Name",
    language="fr",  # French
    cover_image="cover.jpg",
    css="body { font-family: Arial; }",  # Custom CSS
    toc_depth=3
)
```

### Customizing HTML Output

```python
converter.to_html(
    "output.html",
    title="My Document",
    css="body { max-width: 800px; margin: 0 auto; }",
    embed_images=True  # Embed images as base64 instead of separate files
)
```

### Customizing Text Output

```python
converter.to_text(
    "output.txt",
    include_metadata=True,
    line_width=80  # Wrap lines at 80 characters
)
```

## Error Handling

```python
from book_converter import PDFConverter

try:
    converter = PDFConverter("input.pdf")
    converter.to_epub("output.epub")
except FileNotFoundError:
    print("The PDF file was not found")
except ValueError as e:
    print(f"Error during conversion: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```
