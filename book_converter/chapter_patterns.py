"""
Chapter pattern detection and formatting for book conversion.
"""
import re
import logging
from typing import Optional, List, Dict, Tuple, Match

logger = logging.getLogger(__name__)

class ChapterDetector:
    """
    Detects and formats chapter openings in text using regular expressions.
    """
    
    def __init__(self, pattern: str, style_class: str = "chapter-opening"):
        """
        Initialize the chapter detector.
        
        Args:
            pattern (str): Regex pattern to detect chapter openings
            style_class (str): CSS class to apply to the chapter opening
        """
        self.pattern = pattern
        self.style_class = style_class
        self._compile_pattern()
    
    def _compile_pattern(self) -> None:
        """Compile the regex pattern."""
        try:
            self.regex = re.compile(self.pattern, re.MULTILINE | re.DOTALL)
        except re.error as e:
            logger.error(f"Invalid regex pattern: {e}")
            raise ValueError(f"Invalid chapter pattern: {e}")
    
    def format_chapter_openings(self, text: str) -> str:
        """
        Detect and format chapter openings in text.
        
        Args:
            text (str): Text content to process
            
        Returns:
            str: Processed text with formatted chapter openings
        """
        if not self.pattern:
            return text
            
        # Find all matches, from last to first to avoid offset issues
        matches = list(self.regex.finditer(text))
        
        # Process in reverse order
        for match in reversed(matches):
            opening = match.group(0)
            styled_opening = f'<div class="{self.style_class}">{opening}</div>'
            
            # Replace the matched text with the styled version
            start, end = match.span()
            text = text[:start] + styled_opening + text[end:]
            
        return text
    
    def extract_chapter_titles(self, text: str) -> List[str]:
        """
        Extract just the chapter titles from text.
        
        Args:
            text (str): Text content to process
            
        Returns:
            List[str]: List of chapter titles
        """
        if not self.pattern:
            return []
            
        # Find all matches
        matches = list(self.regex.finditer(text))
        return [match.group(0) for match in matches]


# Predefined chapter patterns
CHAPTER_PATTERNS = {
    # Basic chapter pattern: "Chapter X" or "Chapter X: Title"
    "standard": r"Chapter\s+\d+(?:\s*:\s*[^\n]+)?\s*\n",
    
    # Pattern for chapters with quotes: "Chapter X: Title", quote, and ending with "~"
    "quoted": r"Chapter\s+\d+(?:\s*:\s*[^\n]+)?\s*\n\s*\"[^\"]+\"\s*\n\s*~\s*",
    
    # Pattern for numbered chapters without the word "Chapter"
    "numbered": r"^\s*\d+\.\s+[^\n]+\s*$",
    
    # Pattern for chapters with roman numerals
    "roman": r"^\s*(?:I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII|XIII|XIV|XV|XVI|XVII|XVIII|XIX|XX)\.\s+[^\n]+\s*$",
}

# Default CSS styles for chapter openings
CHAPTER_STYLES = {
    "standard": """
        .chapter-opening {
            margin: 2em 0;
            font-weight: bold;
            font-size: 1.2em;
            text-align: center;
        }
    """,
    
    "quoted": """
        .chapter-opening {
            margin: 3em 0;
            font-style: italic;
            font-size: 1.1em;
            text-align: center;
            line-height: 1.8;
            color: #333;
            border-bottom: 1px solid #eee;
            padding-bottom: 1.5em;
        }
        .chapter-opening::before,
        .chapter-opening::after {
            content: "";
            display: block;
            height: 1px;
            background: #ddd;
            margin: 1em auto;
            width: 30%;
        }
    """,
    
    "decorative": """
        .chapter-opening {
            margin: 3em auto;
            font-family: 'Georgia', serif;
            font-size: 1.2em;
            line-height: 1.6;
            text-align: center;
            max-width: 80%;
            padding: 1.5em;
            border: 1px solid #ddd;
            border-radius: 5px;
            background-color: #f9f9f9;
            box-shadow: 0 0 5px rgba(0,0,0,0.1);
        }
    """,
}
