import requests
from typing import Dict
from app.config import Settings
from app.utils.post_processor import PostProcessor
from app.services.seo_service import SEOService

class HuggingFaceService:
    """Hugging Face API integration for blog generation."""
    def __init__(self):
        self.api_url = f"https://api-inference.huggingface.co/models/{settings.HUGGINGFACE_MODEL}"
        self.headers =  {"Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"}
        self.post_processor = PostProcessor()
        self.seo_service = SEOService()

    def generate_blog(self, topic: str, tone: str, length: str, keywords: str = None) -> Dict:
        """Generate complete blog post"""

        # Build prompt 
        prompt = self._build_prompt(topic, tone, length, keywords)

        # Generate content
        raw_content = self._call_api(prompt)

        # Post-process content
        cleaned_content = self.post_processor.clean_content(raw_content)
        title, content = self.post_processor.extract_title_and_content(cleaned_content, topic)
        formatted_content = self.post_processor.add_formatting(content)

        # Calculate metrics
        word_count = self.post_processor.count_words(formatted_content)
        seo_score = self.seo_service.calculate_score(formatted_content, title, keywords)

        return {
            "title": title,
            "content": formatted_content,
            "word_count": word_count,
            "seo_score": seo_score
        }
    def _build_prompt(self, topic: str, tone: str, length: str, keywords: str = None) -> str:
        """Build optimized prompt"""

        tone_mapped = {
            "professional": "authoritative, polished, business-appropriate",
            "casual": "friendly, conversational, and relatable",
            "technical": "detailed, precise, and technically accurate",
            "educational": "informative, clear, and easy to understand"
        }

        length_map = {
            "short": "600-900 words",
            "medium": "1000-1500 words",
            "long": "1800-2500 words"
        }
        tone_desc = tone_map.get(tone, tone_map["professional"])
        length_desc = length_map.get(length, length_map["medium"])
        keywords_instruction = f"\nKeywords to include: {keywords}" if keywords else ""

        prompt = f"""<s>[INST] Write a comprehensive blog post on the following topic.

Topic: {topic}
Tone: {tone_desc}
Target Length: {length_desc}{keywords_instruction}

Requirements:
1. Create an engaging, SEO-friendly title.
2. Write a compelling introduction
3. Organize content with clear subheadings (Use ## for subheadings).and
4. Include practical examples and insights.
5. End with a strong conclusion.

Format your response as:
# [Title]

## [Introduction]

## [Section 1 Title]
[Content]

## [Section 2 Title]
[Content]

## [Section 3 Title]
[Content]

## Conclusion
[Conclusion]

Write the blog post: [/INST]"""
        
        return prompt
    def _call_api(self, prompt: str, max_retries: int = 2) -> str:
        """Call Hugging Face Inference API"""
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 2048,
                "temperature": 0.7,
                "top_p": 0.92,
                "do_sample": True,
                "return_full_text": False
            }
        }

        for attempt in range(max_retries + 1):
            try:
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=120
                )

                if response.status_code == 503:
                    raise Exception("Model is loading, please wait 20-30 seconds and try again.")
                
                response.raise_for_status()
                result = response.json()

                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("generated_text", "")
                elif isinstance(result, dict):
                    return result.get("generated_text", "")
                else:
                    raise Exception("Unexpected API response format.")
            except requests.exceptions.Timeout:
                if attempt < max_retries:
                    continue
                raise Exception("Request timed out. Please try again.")
            except requests.exceptions.RequestException as e:
                if attempt < max_retries:
                    continue
                raise Exception(f"API request error: {str(e)}")
            raise Exception("Failed after multiple retries.")
        
        # Global instance
        hf_service = HuggingFaceService()
              