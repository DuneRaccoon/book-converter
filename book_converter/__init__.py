"""
Book Converter - A tool to convert PDF files to various formats.
"""

__version__ = "1.0.0"

from .converter import PDFConverter
from .formats import EPUBConverter, DOCXConverter, HTMLConverter, TextConverter, MarkdownConverter, MOBIConverter
from .chapter_patterns import ChapterDetector, CHAPTER_PATTERNS, CHAPTER_STYLES

__all__ = [
    "PDFConverter", 
    "EPUBConverter", 
    "DOCXConverter", 
    "HTMLConverter", 
    "TextConverter", 
    "MarkdownConverter",
    "MOBIConverter",
    "ChapterDetector",
    "CHAPTER_PATTERNS",
    "CHAPTER_STYLES"
]
