"""
Tests for the PDF converter functionality.
"""
import os
import pytest
import tempfile
from pathlib import Path

import fitz  # PyMuPDF

from book_converter.converter import PDFConverter
from book_converter.formats import EPUBConverter, DOCXConverter, HTMLConverter, TextConverter, MarkdownConverter


# Skip tests if a PDF file is not available
sample_pdf_path = os.path.join(os.path.dirname(__file__), 'sample.pdf')
needs_pdf = pytest.mark.skipif(
    not os.path.exists(sample_pdf_path),
    reason="Sample PDF file not available"
)


class TestPDFConverter:
    """Tests for the PDFConverter class."""
    
    def test_init_with_invalid_file(self):
        """Test initializing with an invalid file."""
        with pytest.raises(FileNotFoundError):
            PDFConverter('nonexistent.pdf')
    
    @needs_pdf
    def test_extract_metadata(self):
        """Test extracting metadata from a PDF."""
        converter = PDFConverter(sample_pdf_path)
        metadata = converter._extract_metadata()
        
        assert isinstance(metadata, dict)
        assert 'page_count' in metadata
        assert metadata['page_count'] > 0
    
    @needs_pdf
    def test_extract_text(self):
        """Test extracting text from a PDF."""
        converter = PDFConverter(sample_pdf_path)
        text_by_page = converter.extract_text()
        
        assert isinstance(text_by_page, list)
        assert len(text_by_page) == len(converter.pages)
        assert all(isinstance(page_text, str) for page_text in text_by_page)


class TestFormatConverters:
    """Tests for the format-specific converters."""
    
    @needs_pdf
    def test_to_epub(self):
        """Test converting to EPUB format."""
        converter = PDFConverter(sample_pdf_path)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, 'output.epub')
            result = converter.to_epub(output_path)
            
            assert os.path.exists(output_path)
            assert os.path.getsize(output_path) > 0
            assert result == output_path
    
    @needs_pdf
    def test_to_text(self):
        """Test converting to plain text format."""
        converter = PDFConverter(sample_pdf_path)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, 'output.txt')
            result = converter.to_text(output_path)
            
            assert os.path.exists(output_path)
            assert os.path.getsize(output_path) > 0
            assert result == output_path
            
            # Check content
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
                assert len(content) > 0
    
    @needs_pdf
    def test_to_markdown(self):
        """Test converting to Markdown format."""
        converter = PDFConverter(sample_pdf_path)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, 'output.md')
            result = converter.to_markdown(output_path)
            
            assert os.path.exists(output_path)
            assert os.path.getsize(output_path) > 0
            assert result == output_path
            
            # Check content
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
                assert '# ' in content  # Should have at least one heading
    
    @needs_pdf
    def test_batch_convert(self):
        """Test batch conversion to multiple formats."""
        converter = PDFConverter(sample_pdf_path)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            formats = ['txt', 'md']
            results = converter.batch_convert(temp_dir, formats)
            
            assert isinstance(results, dict)
            assert len(results) == len(formats)
            
            for fmt in formats:
                assert fmt in results
                assert os.path.exists(results[fmt])
                assert os.path.getsize(results[fmt]) > 0
