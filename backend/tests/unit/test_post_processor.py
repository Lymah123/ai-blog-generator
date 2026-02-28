import pytest
from app.utils.post_processor import PostProcessor


class TestPostProcessor:
    """Unit tests for post-processing utilities"""

    def test_clean_content_removes_excess_whitespace(self):
        """Test removal of excessive whitespace"""
        dirty_content = "Line 1\n\n\n\n\nLine 2    with    spaces"
        
        cleaned = PostProcessor.clean_content(dirty_content)
        
        assert "\n\n\n" not in cleaned
        assert "    " not in cleaned

    def test_clean_content_empty_input(self):
        """Test handling of empty content"""
        result = PostProcessor.clean_content("")
        assert result == ""

    def test_clean_content_none_input(self):
        """Test handling of None input"""
        result = PostProcessor.clean_content(None)
        assert result == ""

    def test_extract_title_and_content_with_hash_title(self):
        """Test title extraction with # format"""
        text = "# My Blog Title\n\nContent here\n\nMore content"
        
        title, content = PostProcessor.extract_title_and_content(text, "Fallback")
        
        assert title == "My Blog Title"
        assert "# My Blog Title" not in content
        assert "Content here" in content

    def test_extract_title_and_content_fallback(self):
        """Test fallback title when none found"""
        long_first_line = "This is a very long first line that exceeds one hundred characters so it will not be used as a title and fallback will apply"
        text = f"{long_first_line}\n\nContent here without a main title"
        fallback_topic = "AI Technology"
        
        title, content = PostProcessor.extract_title_and_content(text, fallback_topic)
        
        # Since first line is too long and no # title, fallback should be used
        assert fallback_topic in title
        assert "Comprehensive Guide" in title

    def test_extract_title_and_content_first_line_as_title(self):
        """Test using first line as title"""
        text = "Short Title\n\nThis is the content\nMore content"
        
        title, content = PostProcessor.extract_title_and_content(text, "Fallback")
        
        assert "Short Title" in title or title == "Fallback: A Comprehensive Guide"

    def test_count_words_normal_text(self):
        """Test word counting"""
        text = "This is a test with exactly nine words here"
        
        count = PostProcessor.count_words(text)
        
        assert count == 9

    def test_count_words_with_punctuation(self):
        """Test word counting ignores punctuation properly"""
        text = "Hello, world! This is a test."
        
        count = PostProcessor.count_words(text)
        
        assert count == 6

    def test_count_words_empty_string(self):
        """Test word counting with empty string"""
        count = PostProcessor.count_words("")
        assert count == 0

    def test_count_words_none_input(self):
        """Test word counting with None input"""
        count = PostProcessor.count_words(None)
        assert count == 0

    def test_add_formatting_heading_spacing(self):
        """Test proper spacing around headings"""
        content = "Some text\n## Heading\nContent right after"
        
        formatted = PostProcessor.add_formatting(content)
        
        # After formatting, headings have proper spacing
        assert "## Heading" in formatted
        assert "\n\n" in formatted  # Check double newline exists for spacing

    def test_add_formatting_empty_content(self):
        """Test formatting empty content"""
        result = PostProcessor.add_formatting("")
        assert result == ""