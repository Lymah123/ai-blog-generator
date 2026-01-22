import requests
import time
from typing import Dict
from app.config import settings
from app.utils.post_processor import PostProcessor
from app.services.seo_service import SEOService

class HuggingFaceService:
    """Hugging Face API integration using the Unified Inference Router."""
    
    def __init__(self):
        self.api_url = "https://router.huggingface.co/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json"
        }
        self.post_processor = PostProcessor()
        self.seo_service = SEOService()

    def generate_blog(self, topic: str, tone: str, length: str, keywords: str = None) -> Dict:
        """Main entry point to generate and process a blog post."""
        
        # Build prompt
        prompt = self._build_prompt(topic, tone, length, keywords)
        
        # Generate content
        raw_content = self._call_api(prompt)
        
        # Validate we got content
        if not raw_content or len(raw_content.strip()) < 100:
            raise Exception("Generated content is too short or empty. Please try again.")
        
        # Process content
        cleaned_content = self.post_processor.clean_content(raw_content)
        title, content = self.post_processor.extract_title_and_content(cleaned_content, topic)
        
        # Validate processed content
        if not content or len(content.strip()) < 50:
            raise Exception("Failed to extract valid content. Please try again.")
        
        formatted_content = self.post_processor.add_formatting(content)
        
        # Calculate metrics
        word_count = self.post_processor.count_words(formatted_content)
        seo_score = self.seo_service.calculate_score(formatted_content, title, keywords)

        return {
            "title": title,
            "content": formatted_content,
            "keywords": keywords,
            "word_count": word_count,
            "seo_score": seo_score 
        }

    def _build_prompt(self, topic: str, tone: str, length: str, keywords: str = None) -> str:
        """Constructs an optimized prompt for blog generation."""
        
        tone_map = {
            "professional": "authoritative, polished, and business-appropriate",
            "casual": "friendly, conversational, and relatable",
            "technical": "detailed, precise, and technically accurate",
            "educational": "clear, informative, and easy to understand"
        }
        
        length_map = {
            "short": {"range": "600-800 words", "sections": 3},
            "medium": {"range": "1000-1500 words", "sections": 5},
            "long": {"range": "1800-2500 words", "sections": 7}
        }
        
        tone_desc = tone_map.get(tone, tone_map["professional"])
        length_info = length_map.get(length, length_map["medium"])
        length_desc = length_info["range"]
        num_sections = length_info["sections"]
        keyword_instruction = f"\n- Include these keywords naturally: {keywords}" if keywords else ""

        return f"""You are an expert blog content writer. Write a comprehensive, well-structured blog post.

**Topic:** {topic}
**Tone:** {tone_desc}
**Target Length:** {length_desc} (STRICT REQUIREMENT - Write at least {length_desc.split('-')[0]} words){keyword_instruction}

**Requirements:**
1. Create an engaging, SEO-friendly title
2. Write a compelling introduction that hooks the reader (150-200 words)
3. Create exactly {num_sections} main sections with clear subheadings (use ## for H2 headings)
4. Each main section should be 150-250 words with detailed examples and insights
5. Include practical examples, statistics, and actionable advice
6. End with a strong conclusion and call-to-action (100-150 words)
7. Make the content informative, engaging, and ready to publish
8. IMPORTANT: The final post MUST be within the {length_desc} range

**Format:**
# [Your SEO-Optimized Title]

[Engaging introduction paragraph]

## [First Main Section]
[Detailed content with examples]

## [Second Main Section]
[Detailed content with examples]

## [Third Main Section]
[Detailed content with examples]

## Conclusion
[Summary and call-to-action]

Write the complete blog post now:"""

    def _call_api(self, prompt: str, max_retries: int = 3) -> str:
        """Calls the HF Router with proper error handling."""
        
        # Model ID extraction
        model_id = settings.HUGGINGFACE_MODEL.split(':')[0].strip()

        payload = {
            "model": model_id,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert blog writer who creates engaging, SEO-optimized content. You always write the exact word count requested."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 4000,
            "temperature": 0.7,
            "top_p": 0.9
        }

        for attempt in range(max_retries):
            try:
                print(f"[Attempt {attempt + 1}/{max_retries}] Calling HF Router with model: {model_id}")
                
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=120
                )

                # Handle model loading
                if response.status_code == 503:
                    print("Model is warming up... waiting 30 seconds")
                    time.sleep(30)
                    continue

                # Handle rate limiting
                if response.status_code == 429:
                    wait_time = int(response.headers.get('Retry-After', 30))
                    print(f"Rate limited. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue

                # Handle errors
                if response.status_code != 200:
                    try:
                        error_detail = response.json()
                    except:
                        error_detail = response.text
                    
                    if response.status_code == 400 and "not a chat model" in str(error_detail):
                        raise Exception(
                            f"Model '{model_id}' is not supported. "
                            f"Update HUGGINGFACE_MODEL in .env to: 'meta-llama/Llama-3.3-70B-Instruct'"
                        )
                    
                    raise Exception(f"HF API Error ({response.status_code}): {error_detail}")

                # Parse successful response
                result = response.json()
                
                if "choices" not in result or len(result["choices"]) == 0:
                    raise Exception(f"Unexpected API response format: {result}")
                
                content = result["choices"][0]["message"]["content"]
                
                if not content or len(content.strip()) < 50:
                    raise Exception("API returned empty or invalid content")
                
                print(f"✓ Successfully generated {len(content)} characters")
                return content

            except requests.exceptions.Timeout:
                print(f"Request timed out")
                if attempt < max_retries - 1:
                    time.sleep(10)
                    continue
                raise Exception("Request timed out after multiple attempts")
                
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(5)
                    continue
                raise Exception(f"Connection error: {str(e)}")

        raise Exception("Failed to generate content after multiple retries")

# Global instance
hf_service = HuggingFaceService()