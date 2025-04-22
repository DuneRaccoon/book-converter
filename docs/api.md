# API Reference

This document provides detailed information about the Book Converter API.

## PDFConverter Class

The main class for converting PDF files to other formats.

### Constructor

```python
PDFConverter(pdf_path, password=None)
```

**Parameters:**
- `pdf_path` (str): Path to the input PDF file
- `password` (Optional[str]): Password for encrypted PDFs

**Raises:**
- `FileNotFoundError`: If the PDF file doesn't exist
- `ValueError`: If the file is not a valid PDF or the password is incorrect

### Properties

- `pdf_path` (str): Path to the input PDF file
- `doc` (fitz.Document): PyMuPDF document object
- `metadata` (Dict[str, str]): Extracted metadata from the PDF
- `pages` (List[fitz.Page]): List of PDF pages
- `images` (List[Dict]): List of extracted images
- `toc` (List[Tuple]): Table of contents extracted from the PDF

### Methods

#### extract_text

```python
extract_text(include_tables=True, detect_columns=True)
```

Extract text content from each page of the PDF.

**Parameters:**
- `include_tables` (bool): Whether to extract tables as structured text
- `detect_columns` (bool): Whether to try to detect and handle columns

**Returns:**
- `List[str]`: List of text content for each page

#### to_epub

```python
to_epub(output_path, **kwargs)
```

Convert the PDF to EPUB format.

**Parameters:**
- `output_path` (str): Path to save the output EPUB file
- `**kwargs`: Additional options:
  - `title` (str): Book title
  - `author` (str): Book author
  - `language` (str): Book language (default: 'en')
  - `cover_image` (str): Path to cover image
  - `css` (str): Custom CSS
  - `toc_depth` (int): Table of contents depth (default: 3)

**Returns:**
- `str`: Path to the output EPUB file

**Raises:**
- `ValueError`: If conversion fails

#### to_docx

```python
to_docx(output_path, **kwargs)
```

Convert the PDF to DOCX format.

**Parameters:**
- `output_path` (str): Path to save the output DOCX file
- `**kwargs`: Additional options:
  - `title` (str): Document title
  - `include_images` (bool): Whether to include images (default: True)
  - `add_title_page` (bool): Whether to add a title page (default: True)

**Returns:**
- `str`: Path to the output DOCX file

**Raises:**
- `ValueError`: If conversion fails

#### to_html

```python
to_html(output_path, **kwargs)
```

Convert the PDF to HTML format.

**Parameters:**
- `output_path` (str): Path to save the output HTML file
- `**kwargs`: Additional options:
  - `title` (str): Document title
  - `include_images` (bool): Whether to include images (default: True)
  - `css` (str): Custom CSS
  - `embed_images` (bool): Whether to embed images as base64 (default: False)

**Returns:**
- `str`: Path to the output HTML file

**Raises:**
- `ValueError`: If conversion fails

#### to_text

```python
to_text(output_path, **kwargs)
```

Convert the PDF to plain text format.

**Parameters:**
- `output_path` (str): Path to save the output text file
- `**kwargs`: Additional options:
  - `include_metadata` (bool): Whether to include metadata (default: True)
  - `line_width` (int): Maximum line width

**Returns:**
- `str`: Path to the output text file

**Raises:**
- `ValueError`: If conversion fails

#### to_markdown

```python
to_markdown(output_path, **kwargs)
```

Convert the PDF to Markdown format.

**Parameters:**
- `output_path` (str): Path to save the output Markdown file
- `**kwargs`: Additional options:
  - `include_metadata` (bool): Whether to include metadata (default: True)
  - `include_toc` (bool): Whether to include table of contents (default: True)
  - `include_images` (bool): Whether to include images (default: True)

**Returns:**
- `str`: Path to the output Markdown file

**Raises:**
- `ValueError`: If conversion fails

#### to_mobi

```python
to_mobi(output_path, **kwargs)
```

Convert the PDF to MOBI format.

**Parameters:**
- `output_path` (str): Path to save the output MOBI file
- `**kwargs`: Additional options (same as `to_epub`)

**Returns:**
- `str`: Path to the output MOBI file

**Raises:**
- `ValueError`: If conversion fails

#### batch_convert

```python
batch_convert(output_dir, formats, **kwargs)
```

Convert the PDF to multiple formats at once.

**Parameters:**
- `output_dir` (str): Directory to save the output files
- `formats` (List[str]): List of formats to convert to ('epub', 'docx', 'html', 'txt', 'md', 'mobi')
- `**kwargs`: Additional options for the conversions

**Returns:**
- `Dict[str, str]`: Dictionary mapping formats to output paths

**Raises:**
- `ValueError`: If an invalid format is specified

## Format-Specific Converter Classes

### BaseFormatConverter

Abstract base class for all format converters.

### EPUBConverter

Converter for EPUB format.

```python
EPUBConverter(pdf_converter).convert(output_path, **kwargs)
```

### DOCXConverter

Converter for DOCX format.

```python
DOCXConverter(pdf_converter).convert(output_path, **kwargs)
```

### HTMLConverter

Converter for HTML format.

```python
HTMLConverter(pdf_converter).convert(output_path, **kwargs)
```

### TextConverter

Converter for plain text format.

```python
TextConverter(pdf_converter).convert(output_path, **kwargs)
```

### MarkdownConverter

Converter for Markdown format.

```python
MarkdownConverter(pdf_converter).convert(output_path, **kwargs)
```

### MOBIConverter

Converter for MOBI format.

```python
MOBIConverter(pdf_converter).convert(output_path, **kwargs)
```

## Utility Functions

### extract_images

```python
extract_images(doc)
```

Extract images from a PDF document.

**Parameters:**
- `doc` (fitz.Document): PyMuPDF document object

**Returns:**
- `List[Dict]`: List of dictionaries containing image data

### get_toc

```python
get_toc(doc)
```

Extract table of contents from a PDF document.

**Parameters:**
- `doc` (fitz.Document): PyMuPDF document object

**Returns:**
- `List[Tuple[int, str, int]]`: List of tuples containing (level, title, page)

### normalize_text

```python
normalize_text(text)
```

Normalize extracted text to fix common issues.

**Parameters:**
- `text` (str): Raw text to normalize

**Returns:**
- `str`: Normalized text

### detect_columns

```python
detect_columns(page, threshold=0.3)
```

Detect text columns in a PDF page.

**Parameters:**
- `page` (fitz.Page): PyMuPDF page object
- `threshold` (float): Overlap threshold for column detection

**Returns:**
- `List[List[float]]`: List of column boundaries [x0, y0, x1, y1]

### is_mostly_text

```python
is_mostly_text(doc)
```

Determine if a PDF document is mostly text or mostly images.

**Parameters:**
- `doc` (fitz.Document): PyMuPDF document object

**Returns:**
- `bool`: True if the document is mostly text, False if mostly images

### compare_pdf_dimensions

```python
compare_pdf_dimensions(doc)
```

Determine if the PDF is likely a book, article, or presentation based on dimensions.

**Parameters:**
- `doc` (fitz.Document): PyMuPDF document object

**Returns:**
- `str`: Document type guess ('book', 'article', 'presentation', or 'unknown')

### sanitize_filename

```python
sanitize_filename(name)
```

Sanitize a filename to ensure it's safe for all operating systems.

**Parameters:**
- `name` (str): Original filename

**Returns:**
- `str`: Sanitized filename
