# Troubleshooting Guide

This guide helps you solve common problems you might encounter when using Book Converter.

## Installation Issues

### "Module not found" Errors

**Problem**: Python cannot find the Book Converter module.

```
ImportError: No module named book_converter
```

**Solutions**:
1. Make sure the package is installed:
   ```bash
   pip list | grep book-converter
   ```

2. If not installed, install it:
   ```bash
   pip install book-converter
   ```

3. If installed but still not found, check your Python environment:
   ```bash
   which python  # On Unix/Linux/macOS
   where python  # On Windows
   ```

4. Try reinstalling the package:
   ```bash
   pip uninstall book-converter
   pip install book-converter
   ```

### PyMuPDF Installation Problems

**Problem**: Issues installing PyMuPDF (fitz) dependency.

**Solutions**:
1. For Windows, try installing the pre-built binary:
   ```bash
   pip install --find-links=https://pypi.org/simple/ PyMuPDF
   ```

2. For Linux, install required system dependencies:
   ```bash
   sudo apt-get install build-essential libffi-dev libssl-dev python3-dev
   sudo apt-get install libmupdf-dev
   pip install PyMuPDF
   ```

3. For macOS:
   ```bash
   brew install mupdf
   pip install PyMuPDF
   ```

## Conversion Issues

### PDF Cannot Be Opened

**Problem**: Error when trying to open the PDF.

```
ValueError: Could not open PDF file: cannot open input file
```

**Solutions**:
1. Verify the PDF path is correct:
   ```bash
   ls -l /path/to/your/file.pdf  # Unix/Linux/macOS
   dir "C:\path\to\your\file.pdf"  # Windows
   ```

2. Check if the file is corrupted:
   ```bash
   book-converter convert input.pdf --output test.txt --verbose
   ```

3. Make sure you have permission to read the file:
   ```bash
   chmod +r /path/to/your/file.pdf  # Unix/Linux/macOS
   ```

### Encrypted PDF Issues

**Problem**: Cannot open an encrypted PDF.

```
ValueError: PDF is encrypted, password required
```

**Solutions**:
1. Provide the correct password:
   ```bash
   book-converter convert secure.pdf --output secure.epub --password "yourpassword"
   ```

2. For Python API:
   ```python
   converter = PDFConverter("secure.pdf", password="yourpassword")
   ```

### EPUB Conversion Error with Integer TOC

**Problem**: Error about integer objects with no title attribute during EPUB conversion.

```
AttributeError: 'int' object has no attribute 'title'
```

**Solutions**:
1. The issue is related to the table of contents structure. You can try:
   ```python
   converter.to_epub("output.epub", toc_depth=2)  # Limit TOC depth
   ```

2. If the error persists, you can disable using the PDF's TOC:
   ```bash
   # Add a --no-toc option in your converter
   ```

3. For a specific file that's problematic, consider creating a custom TOC or using a different format.

### MOBI Conversion Issues

**Problem**: Cannot convert to MOBI format.

**Solutions**:
1. Ensure Calibre is installed with the ebook-convert tool:
   ```bash
   ebook-convert --version
   ```

2. If not installed, download Calibre from [calibre-ebook.com](https://calibre-ebook.com/download)

3. Add Calibre to your PATH:
   ```bash
   # On Windows, usually at:
   # C:\Program Files\Calibre2\
   
   # On macOS, usually at:
   # /Applications/calibre.app/Contents/MacOS/
   ```

4. If Calibre cannot be installed, use EPUB format instead:
   ```bash
   book-converter convert input.pdf --output output.epub
   ```

### Output Quality Issues

**Problem**: Poor output quality in converted files.

**Solutions**:
1. Try enabling column detection:
   ```bash
   book-converter convert input.pdf --output output.epub --detect-columns
   ```

2. For complex layouts, try different output formats:
   ```bash
   book-converter convert input.pdf --output output.docx  # DOCX often preserves layout better
   ```

3. For EPUB issues, try different settings:
   ```python
   converter.to_epub(
       "output.epub",
       include_images=True,
       detect_columns=True,
       toc_depth=3
   )
   ```

### Missing or Garbled Text

**Problem**: Output has missing or garbled text.

**Solutions**:
1. Check if the PDF contains actual text or just images of text:
   ```python
   converter = PDFConverter("input.pdf")
   text = converter.extract_text()
   if not ''.join(text).strip():
       print("PDF might contain scanned text only")
   ```

2. Try using OCR (not built into the tool):
   ```bash
   # Use an OCR tool first, then convert
   # Example with Tesseract (separate installation required)
   tesseract input.pdf output_ocr
   ```

3. Check encoding issues:
   ```bash
   # Try specifying the language for better text extraction
   book-converter convert input.pdf --output output.epub --language "ja"  # For Japanese
   ```

### Image-Related Issues

**Problem**: Images not appearing or appearing incorrectly in output.

**Solutions**:
1. Make sure images are enabled:
   ```bash
   book-converter convert input.pdf --output output.epub --include-images
   ```

2. Check if the PDF actually contains extractable images:
   ```python
   converter = PDFConverter("input.pdf")
   print(f"Found {len(converter.images)} images in the PDF")
   ```

3. For HTML output, try embedding images:
   ```python
   converter.to_html("output.html", embed_images=True)
   ```

## Command-Line Issues

### Command Not Found

**Problem**: The `book-converter` command is not recognized.

**Solutions**:
1. Check if the package is installed with entry points:
   ```bash
   pip show book-converter
   ```

2. Try running with Python directly:
   ```bash
   python -m book_converter.cli convert input.pdf --output output.epub
   ```

3. Check your PATH environment variable:
   ```bash
   echo $PATH  # Unix/Linux/macOS
   echo %PATH%  # Windows
   ```

### Unexpected Arguments Error

**Problem**: Error about unexpected arguments.

**Solutions**:
1. Check command syntax:
   ```bash
   book-converter --help
   book-converter convert --help
   ```

2. Use quotes for paths with spaces:
   ```bash
   book-converter convert "My Document.pdf" --output "My Document.epub"
   ```

## Getting Additional Help

If you encounter issues not covered in this guide:

1. Check the [GitHub Issues](https://github.com/yourusername/book-converter/issues) page to see if others have reported the same problem.

2. Enable verbose logging for more information:
   ```bash
   book-converter convert input.pdf --output output.epub --verbose
   ```

3. Create a minimal reproducible example and submit an issue.
