import pytest
from app.services.seo_service import SEOService


class TestSEOService:
    """Unit tests for SEO scoring algorithm"""

    def test_calculate_score_optimal_word_count(self):
        """Test SEO score with optimal word count"""
        content = " ".join(["word"] * 1000)  # 1000 words
        title = "Test Title That Is Perfect Length"
        
        score = SEOService.calculate_score(content, title, None)
        
        assert score > 0
        assert score <= 100

    def test_calculate_score_with_keywords(self):
        """Test SEO score increases with keyword usage"""
        content = "python fastapi testing " * 100
        title = "Python FastAPI Testing Guide"
        keywords = "python, fastapi, testing"
        
        score_with_keywords = SEOService.calculate_score(content, title, keywords)
        score_without_keywords = SEOService.calculate_score(content, title, None)
        
        assert score_with_keywords > score_without_keywords

    def test_calculate_score_heading_structure(self):
        """Test SEO score accounts for heading structure"""
        content_with_headings = """
        ## Introduction
        Content here
        ## Main Section
        More content
        ## Conclusion
        Final content
        """
        content_without_headings = "Content without any structure"
        
        title = "Test Title"
        
        score_with = SEOService.calculate_score(content_with_headings, title, None)
        score_without = SEOService.calculate_score(content_without_headings, title, None)
        
        assert score_with > score_without

    def test_calculate_score_title_optimization(self):
        """Test SEO score for title length optimization"""
        content = "Test content " * 100
        
        # Optimal title (40-70 chars)
        optimal_title = "This Is An Optimal Length Title For SEO"
        # Too short title
        short_title = "Short"
        
        score_optimal = SEOService.calculate_score(content, optimal_title, None)
        score_short = SEOService.calculate_score(content, short_title, None)
        
        assert score_optimal > score_short

    def test_calculate_score_max_value(self):
        """Test that SEO score never exceeds 100"""
        # Perfect content
        content = "python fastapi testing " * 500  # Optimal word count
        content += "\n## Introduction\n"
        content += "\n## Section 1\n"
        content += "\n## Section 2\n"
        content += "\n## Conclusion\n"
        
        title = "Perfect SEO Title Length For Testing Python FastAPI"
        keywords = "python, fastapi, testing"
        
        score = SEOService.calculate_score(content, title, keywords)
        
        assert score <= 100

    def test_get_recommendations_low_score(self):
        """Test recommendations for low SEO scores"""
        recommendations = SEOService.get_recommendations(40)
        
        assert len(recommendations) > 0
        assert any("headings" in rec.lower() for rec in recommendations)

    def test_get_recommendations_high_score(self):
        """Test recommendations for high SEO scores"""
        recommendations = SEOService.get_recommendations(85)
        
        assert len(recommendations) > 0
        assert any("great" in rec.lower() for rec in recommendations)