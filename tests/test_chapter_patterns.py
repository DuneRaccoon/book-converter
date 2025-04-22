"""
Tests for the chapter pattern detection functionality.
"""
import os
import pytest

from book_converter.chapter_patterns import ChapterDetector, CHAPTER_PATTERNS, CHAPTER_STYLES


class TestChapterDetector:
    """Tests for the ChapterDetector class."""
    
    def test_init_with_invalid_pattern(self):
        """Test initializing with an invalid regex pattern."""
        with pytest.raises(ValueError):
            ChapterDetector("(unclosed parenthesis")
    
    def test_format_chapter_openings_standard(self):
        """Test detecting and formatting standard chapter pattern."""
        detector = ChapterDetector(CHAPTER_PATTERNS["standard"])
        
        sample_text = """
        Some introductory text.
        
        Chapter 1: The Beginning
        
        It was a dark and stormy night...
        """
        
        formatted_text = detector.format_chapter_openings(sample_text)
        
        # Check that the chapter title was wrapped in a div with the class
        assert '<div class="chapter-opening">Chapter 1: The Beginning' in formatted_text
    
    def test_format_chapter_openings_quoted(self):
        """Test detecting and formatting quoted chapter pattern."""
        detector = ChapterDetector(CHAPTER_PATTERNS["quoted"])
        
        sample_text = """
        Some introductory text.
        
        Chapter 3: Forge and Flame
        "Fire reveals the truth in the heart of metal and man alike; it is both a crucible and a judge."
        ~
        
        The blacksmith's hammer fell...
        """
        
        formatted_text = detector.format_chapter_openings(sample_text)
        
        # Check that the chapter opening was wrapped in a div with the class
        assert '<div class="chapter-opening">Chapter 3: Forge and Flame' in formatted_text
        assert '"Fire reveals the truth in the heart of metal and man alike; it is both a crucible and a judge."' in formatted_text
        assert '~' in formatted_text
    
    def test_format_chapter_openings_with_custom_class(self):
        """Test formatting chapters with a custom CSS class."""
        detector = ChapterDetector(CHAPTER_PATTERNS["standard"], style_class="custom-chapter")
        
        sample_text = "Chapter 2: The Middle\n\nContent here..."
        
        formatted_text = detector.format_chapter_openings(sample_text)
        
        # Check that the custom class was used
        assert '<div class="custom-chapter">Chapter 2: The Middle' in formatted_text
    
    def test_extract_chapter_titles(self):
        """Test extracting chapter titles."""
        detector = ChapterDetector(CHAPTER_PATTERNS["standard"])
        
        sample_text = """
        Some introductory text.
        
        Chapter 1: The Beginning
        
        Content of chapter 1...
        
        Chapter 2: The Middle
        
        Content of chapter 2...
        
        Chapter 3: The End
        
        Content of chapter 3...
        """
        
        titles = detector.extract_chapter_titles(sample_text)
        
        # Check that all titles were extracted
        assert len(titles) == 3
        assert "Chapter 1: The Beginning" in titles[0]
        assert "Chapter 2: The Middle" in titles[1]
        assert "Chapter 3: The End" in titles[2]
