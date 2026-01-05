import re
from typing import Tuple

class PostProcessor:
    """Post-process generated blog content"""

    @staticmethod
    def clean_content(text: str) -> str:
        """Clean and format generated text."""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r' {2,}', ' ', text)
        
        # Remove incomplete sentences at the end
        text = text.strip()
        
        return text
    
    @staticmethod
    def extract_title_and_content(text: str, fallback_topic: str) -> Tuple[str, str]:
        """Extract title from the content."""
        if not text:
            return f"{fallback_topic}: A Comprehensive Guide", ""
        
        lines = text.split('\n')
        title = None
        content_lines = []

        for line in lines:
            line = line.strip()
            if line.startswith('# ') and not title:
                title = line.replace('# ', '').strip()
            elif line:
                content_lines.append(line)

        if not title:
            # Try to find title in the first line
            if lines and lines[0].strip():
                potential_title = lines[0].strip().replace('#', '').replace('*', '').strip()
                if len(potential_title) < 100:
                    title = potential_title
                    content_lines = content_lines[1:] if content_lines else []

        if not title:
            title = f"{fallback_topic}: A Comprehensive Guide"

        content = '\n\n'.join(content_lines) if content_lines else ""
        return title, content
    
    @staticmethod
    def count_words(text: str) -> int:
        """Count words in the text."""
        if not text:
            return 0
        
        words = re.findall(r'\b\w+\b', text)
        return len(words)
    
    @staticmethod
    def add_formatting(content: str) -> str:
        """Enhance content formatting."""
        if not content:
            return ""
        
        # Ensure proper spacing around headings
        content = re.sub(r'(#{1,6}\s+.+)', r'\n\1\n', content)
        
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        return content.strip()