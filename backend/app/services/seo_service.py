import re

class SEOService:
 """SEO analysis and scoring."""

 @staticmethod
 def calculate_score(content: str, title: str, keywords: str = None) -> float:
     """Calculate SEO score (0 - 100)."""
     score = 0.0

     # Word count analysis (25 points)
     word_count = len(re.findall(r'\b\w+\b', content))
     if 800 <= word_count <= 2500:
        score += 25
     elif 600 <= word_count < 800 or 2500 < word_count <= 3000:
        score += 18
     elif word_count >= 3000:
        score += 12

     # Title Optimization (15 points)
     if title:
        title_length = len(title)
        if 40 <= title_length <= 70:
           score += 15
        elif 30 <= title_length < 40 or 70 < title_length <= 90:
           score += 10
        elif title_length > 0:
           score += 5

     # Heading structure (20 points)
     h2_count = len(re.findall(r'##\s+', content))
     h3_count = len(re.findall(r'###\s+', content))
     total_headings = h2_count + h3_count

     if 3 <= total_headings <= 8:
        score += 20
     elif 2 <= total_headings <= 10:
        score += 15
     elif total_headings > 0:
        score += 8

    # Keyword optimization (25 points)
     if keywords:
        keyword_list = [k.strip().lower() for k in keywords.split(',') if k.strip()]
        content_lower = content.lower()
        title_lower = title.lower() if title else ""
        keywords_in_content = sum(1 for kw in keyword_list if kw in content_lower)
        keywords_in_title = sum(1 for kw in keyword_list if kw in title_lower)

        # Keywords in content (15 points)
        if keywords_in_content >= len(keyword_list):
           score += 15 
        elif keywords_in_content >= len(keyword_list) * 0.7:
           score += 12
        elif keywords_in_content > 0:
           score += 8

       # Keywords in title (10 points)
        if keywords_in_title > 0:
           score += 10
     else: 
        score += 12

     # Content quality indicators (15 points)
     has_intro = bool(re.search(r'introduction|overview', content.lower()[:500]))
     has_conclusion = bool(re.search(r'(conclusion|summary|final)', content.lower()[-500:]))

     if has_intro:
        score += 7
     if has_conclusion:
        score += 8
     
     return min(round(score, 2), 100.0)
     
 @staticmethod 
 def get_recommendations(score: float) -> list:
    """Get SEO improvement recommendations."""
    recommendations = []
    if score < 50:
       recommendations.append("Consider adding more headings and subheadings")
       recommendations.append("Increase content length to at least 800-2000 words")
       recommendations.append("Include relevant keywords naturally")
    elif score < 75:
       recommendations.append("Optimize title length (40-70 characters)")
       recommendations.append("Add more structured content sections")
    else:
       recommendations.append("Great job! Content is well-optimized.")
    
    return recommendations
 

           

        
