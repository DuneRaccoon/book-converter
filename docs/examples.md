# Examples

This document provides practical examples of using Book Converter for various common tasks.

## Basic Conversion Examples

### Converting a PDF to EPUB

Command-line:
```bash
book-converter convert document.pdf --output document.epub
```

Python code:
```python
from book_converter import PDFConverter

converter = PDFConverter("document.pdf")
converter.to_epub("document.epub")
```

### Converting a PDF to DOCX

Command-line:
```bash
book-converter convert document.pdf --output document.docx
```

Python code:
```python
from book_converter import PDFConverter

converter = PDFConverter("document.pdf")
converter.to_docx("document.docx")
```

### Converting a PDF to Plain Text

Command-line:
```bash
book-converter convert document.pdf --output document.txt
```

Python code:
```python
from book_converter import PDFConverter

converter = PDFConverter("document.pdf")
converter.to_text("document.txt")
```

### Converting a PDF to Markdown

Command-line:
```bash
book-converter convert document.pdf --output document.md
```

Python code:
```python
from book_converter import PDFConverter

converter = PDFConverter("document.pdf")
converter.to_markdown("document.md")
```

## Advanced Conversion Examples

### Converting with Custom Metadata

Command-line:
```bash
book-converter convert book.pdf --output book.epub --title "My Custom Title" --author "Jane Author" --language "fr"
```

Python code:
```python
from book_converter import PDFConverter

converter = PDFConverter("book.pdf")
converter.to_epub(
    "book.epub",
    title="My Custom Title",
    author="Jane Author",
    language="fr"
)
```

### Adding a Custom Cover Image

Command-line:
```bash
book-converter convert book.pdf --output book.epub --cover-image cover.jpg
```

Python code:
```python
from book_converter import PDFConverter

converter = PDFConverter("book.pdf")
converter.to_epub(
    "book.epub",
    cover_image="cover.jpg"
)
```

### Converting Without Images

Command-line:
```bash
book-converter convert document.pdf --output document.epub --no-images
```

Python code:
```python
from book_converter import PDFConverter

converter = PDFConverter("document.pdf")
converter.to_epub(
    "document.epub",
    include_images=False
)
```

### Converting with Column Detection Disabled

Command-line:
```bash
book-converter convert newspaper.pdf --output newspaper.txt --no-detect-columns
```

Python code:
```python
from book_converter import PDFConverter

converter = PDFConverter("newspaper.pdf")
converter.to_text(
    "newspaper.txt",
    detect_columns=False
)
```

### Converting a Password-Protected PDF

Command-line:
```bash
book-converter convert secure.pdf --output secure.epub --password "mysecret"
```

Python code:
```python
from book_converter import PDFConverter

converter = PDFConverter("secure.pdf", password="mysecret")
converter.to_epub("secure.epub")
```

## Batch Conversion Examples

### Converting Multiple PDFs to a Single Format

Command-line:
```bash
book-converter batch *.pdf --output-dir converted --format epub
```

Python code:
```python
import os
import glob
from book_converter import PDFConverter

output_dir = "converted"
os.makedirs(output_dir, exist_ok=True)

for pdf_file in glob.glob("*.pdf"):
    try:
        converter = PDFConverter(pdf_file)
        base_name = os.path.splitext(os.path.basename(pdf_file))[0]
        output_path = os.path.join(output_dir, f"{base_name}.epub")
        converter.to_epub(output_path)
        print(f"Converted {pdf_file} to {output_path}")
    except Exception as e:
        print(f"Error converting {pdf_file}: {e}")
```

### Converting a PDF to Multiple Formats

Command-line:
```bash
book-converter batch document.pdf --output-dir converted --format epub,docx,txt
```

Python code:
```python
from book_converter import PDFConverter

converter = PDFConverter("document.pdf")
results = converter.batch_convert(
    output_dir="converted",
    formats=["epub", "docx", "txt"]
)

for fmt, path in results.items():
    print(f"Converted to {fmt}: {path}")
```

## HTML-Specific Examples

### Creating HTML with Embedded Images

Command-line:
```bash
# Not directly supported via command line
```

Python code:
```python
from book_converter import PDFConverter

converter = PDFConverter("document.pdf")
converter.to_html(
    "document_embedded.html",
    embed_images=True  # Images will be base64-encoded in the HTML
)
```

### Creating HTML with Custom CSS

Python code:
```python
from book_converter import PDFConverter

custom_css = """
body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f9f9f9;
}

h1, h2, h3 {
    color: #2c3e50;
}

img {
    max-width: 100%;
    height: auto;
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 5px;
}
"""

converter = PDFConverter("document.pdf")
converter.to_html(
    "document_styled.html",
    css=custom_css
)
```

## EPUB-Specific Examples

### Creating EPUB with Custom CSS

Python code:
```python
from book_converter import PDFConverter

custom_css = """
body {
    font-family: 'Palatino', serif;
    line-height: 1.5;
    margin: 5%;
}

h1 {
    font-size: 1.5em;
    text-align: center;
    margin-bottom: 1em;
}

h2 {
    font-size: 1.2em;
    margin-top: 2em;
}

p {
    text-indent: 1em;
    margin-top: 0.5em;
    margin-bottom: 0.5em;
}
"""

converter = PDFConverter("book.pdf")
converter.to_epub(
    "book_styled.epub",
    css=custom_css
)
```

### Controlling Table of Contents Depth

Command-line:
```bash
book-converter convert book.pdf --output book.epub --toc-depth 2
```

Python code:
```python
from book_converter import PDFConverter

converter = PDFConverter("book.pdf")
converter.to_epub(
    "book.epub",
    toc_depth=2  # Only include level 1 and 2 headings in TOC
)
```

## Using Chapter Pattern Detection

### Detecting Chapter Patterns in PDF Content

Command-line:
```bash
book-converter convert novel.pdf --output novel.epub --chapter-pattern quoted --chapter-style quoted
```

Python code:
```python
from book_converter import PDFConverter, CHAPTER_PATTERNS, CHAPTER_STYLES

converter = PDFConverter("novel.pdf")

# Using predefined patterns and styles
converter.to_epub(
    "novel.epub",
    chapter_pattern="quoted",    # Detect "Chapter X: Title", quote, and ~
    chapter_style_name="quoted" # Apply the quoted style
)
```

### Using Custom Chapter Patterns

Command-line:
```bash
book-converter convert novel.pdf --output novel.epub --custom-chapter-pattern "Chapter\\s+\\d+\\s*:\\s*[^\\n]+\\n" --chapter-style decorative
```

Python code:
```python
from book_converter import PDFConverter, CHAPTER_PATTERNS, CHAPTER_STYLES

converter = PDFConverter("novel.pdf")

# Custom pattern with predefined style
converter.to_epub(
    "novel.epub",
    chapter_pattern=r"Chapter\s+\d+\s*:\s*[^\n]+\n",  # Custom regex pattern
    chapter_style_name="decorative"  # Use decorative style
)

# Custom pattern with custom CSS
custom_style = """
.chapter-opening {
    margin: 3em auto;
    font-family: 'Georgia', serif;
    font-size: 1.2em;
    line-height: 1.6;
    text-align: center;
    color: #444;
    border-bottom: 2px double #999;
    padding-bottom: 1em;
}
"""

converter.to_epub(
    "novel_custom.epub",
    chapter_pattern=r"Chapter\s+\d+\s*:\s*[^\n]+\n",  # Custom regex pattern
    chapter_style=custom_style  # Custom CSS
)
```

### Extracting Chapter Titles

Python code:
```python
from book_converter import PDFConverter, ChapterDetector

# First extract text from PDF
converter = PDFConverter("novel.pdf")
text_by_page = converter.extract_text()
text_content = "\n".join(text_by_page)

# Create a chapter detector with the pattern
chapter_detector = ChapterDetector(r"Chapter\s+\d+(?:\s*:\s*[^\n]+)?\s*\n")

# Extract chapter titles
chapter_titles = chapter_detector.extract_chapter_titles(text_content)

print(f"Found {len(chapter_titles)} chapters:")
for title in chapter_titles:
    print(f"  - {title.strip()}")
```

## Working with Extracted Content

### Extracting and Processing Text

Python code:
```python
from book_converter import PDFConverter

converter = PDFConverter("document.pdf")
text_by_page = converter.extract_text()

# Count words across all pages
total_words = 0
for page_text in text_by_page:
    words = page_text.split()
    total_words += len(words)

print(f"The document contains approximately {total_words} words")

# Find occurrences of a specific term
search_term = "example"
occurrences = 0
for page_num, page_text in enumerate(text_by_page, 1):
    count = page_text.lower().count(search_term.lower())
    if count > 0:
        print(f"Found '{search_term}' {count} times on page {page_num}")
        occurrences += count

print(f"Total occurrences of '{search_term}': {occurrences}")
```

### Working with Extracted Images

Python code:
```python
import os
from book_converter import PDFConverter

converter = PDFConverter("document.pdf")

# Save all images to a directory
image_dir = "extracted_images"
os.makedirs(image_dir, exist_ok=True)

for i, img_data in enumerate(converter.images):
    if "image" in img_data:
        img_path = os.path.join(image_dir, f"image_{i+1}.{img_data['ext']}")
        with open(img_path, "wb") as f:
            f.write(img_data["image"])
        print(f"Saved image {i+1}: {img_path}")

print(f"Extracted {len(converter.images)} images to {image_dir}")
```

### Working with Table of Contents

Python code:
```python
from book_converter import PDFConverter

converter = PDFConverter("book.pdf")

if converter.toc:
    print("Table of Contents:")
    for level, title, page in converter.toc:
        indent = "  " * (level - 1)
        print(f"{indent}- {title} (page {page})")
else:
    print("No table of contents found in the document")
```

## Error Handling Examples

Python code:
```python
from book_converter import PDFConverter
import sys

def convert_pdf(input_path, output_path):
    try:
        converter = PDFConverter(input_path)
        
        # Determine output format based on extension
        ext = output_path.lower().split('.')[-1]
        
        if ext == 'epub':
            converter.to_epub(output_path)
        elif ext == 'docx':
            converter.to_docx(output_path)
        elif ext == 'html':
            converter.to_html(output_path)
        elif ext == 'txt':
            converter.to_text(output_path)
        elif ext == 'md':
            converter.to_markdown(output_path)
        elif ext == 'mobi':
            converter.to_mobi(output_path)
        else:
            print(f"Unsupported output format: {ext}")
            return False
            
        print(f"Successfully converted to {output_path}")
        return True
        
    except FileNotFoundError:
        print(f"Error: Input file not found: {input_path}")
        return False
    except ValueError as e:
        print(f"Error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input.pdf output.ext")
        sys.exit(1)
        
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    success = convert_pdf(input_path, output_path)
    sys.exit(0 if success else 1)
```
