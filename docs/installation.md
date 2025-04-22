# Installation Guide

This guide provides detailed installation instructions for the Book Converter tool.

## Prerequisites

Book Converter requires:

- Python 3.7 or newer
- Pip package manager
- Approximately 500MB of disk space (including dependencies)

## Installation Methods

### 1. Install from PyPI (Recommended)

The simplest way to install Book Converter is directly from PyPI:

```bash
pip install book-converter
```

For a user-specific installation (without admin privileges):

```bash
pip install --user book-converter
```

### 2. Install from Source

If you want the latest development version or need to modify the code:

```bash
# Clone the repository
git clone https://github.com/yourusername/book-converter.git
cd book-converter

# Install in development mode
pip install -e .
```

### 3. Virtual Environment Installation (Recommended for Developers)

Using a virtual environment is recommended to avoid dependency conflicts:

```bash
# Create a virtual environment
python -m venv book-converter-env

# Activate the virtual environment
# On Windows:
book-converter-env\Scripts\activate
# On macOS/Linux:
source book-converter-env/bin/activate

# Install from source
cd book-converter
pip install -e .
```

## Dependencies

Book Converter relies on the following key libraries:

- **PyMuPDF**: For PDF processing
- **ebooklib**: For EPUB creation
- **python-docx**: For DOCX creation
- **Pillow**: For image processing
- **BeautifulSoup4**: For HTML processing

These dependencies will be automatically installed when you install Book Converter.

## Installing Optional Dependencies

Some features require additional dependencies:

```bash
# For development
pip install book-converter[dev]

# For testing only
pip install book-converter[test]
```

## Verifying Installation

To verify the installation:

```bash
book-converter --version
```

You should see the version number of Book Converter printed to the console.

## Troubleshooting

### Common Issues

#### Missing PyMuPDF Dependency

If you encounter an error about missing MuPDF libraries:

**On Linux:**
```bash
sudo apt-get install libmupdf-dev
pip install --upgrade PyMuPDF
```

**On macOS:**
```bash
brew install mupdf
pip install --upgrade PyMuPDF
```

#### Permission Errors

If you encounter permission errors during installation:

```bash
# Try installing for the current user only
pip install --user book-converter

# Or use a virtual environment (as described above)
```

#### Import Errors

If you're getting import errors when trying to use the package:

1. Make sure you've activated the correct virtual environment (if using one)
2. Try reinstalling the package: `pip uninstall book-converter && pip install book-converter`

### Getting Help

If you encounter any issues not covered here:

1. Check our [GitHub Issues](https://github.com/yourusername/book-converter/issues) to see if someone has already solved your problem
2. Open a new issue if your problem is unique

## Uninstallation

To remove Book Converter:

```bash
pip uninstall book-converter
```
