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
            "short": {"range": "600-800 words", "min": 600, "sections": 3, "section_words": 200},
            "medium": {"range": "1000-1500 words", "min": 1000, "sections": 5, "section_words": 250},
            "long": {"range": "1800-2500 words", "min": 1800, "sections": 7, "section_words": 300}
        }
        
        tone_desc = tone_map.get(tone, tone_map["professional"])
        length_info = length_map.get(length, length_map["medium"])
        length_desc = length_info["range"]
        min_words = length_info["min"]
        num_sections = length_info["sections"]
        section_words = length_info["section_words"]
        keyword_instruction = f"\n- Include these keywords naturally throughout the content: {keywords}" if keywords else ""

        return f"""You are an expert blog content writer specializing in long-form, comprehensive content.

**CRITICAL INSTRUCTION:** You MUST write AT LEAST {min_words} words. Count as you write to ensure you meet this requirement.

**Topic:** {topic}
**Tone:** {tone_desc}
**Target Length:** {length_desc} (MINIMUM {min_words} words - DO NOT STOP UNTIL YOU REACH THIS){keyword_instruction}

**Detailed Structure (FOLLOW EXACTLY):**

1. **Introduction (200-250 words):**
   - Hook the reader with an interesting fact or question
   - Provide context and background
   - State what the article will cover
   - Explain why this topic matters

2. **Main Content ({num_sections} sections, EACH section must be {section_words}+ words):**
   - Create {num_sections} distinct main sections with ## headings
   - Each section needs multiple paragraphs
   - Include specific examples, case studies, or data points
   - Add subsections with ### headings where appropriate
   - Use bullet points or numbered lists for clarity
   - Explain concepts thoroughly - don't rush

3. **Conclusion (150-200 words):**
   - Summarize key takeaways
   - Provide actionable next steps
   - Include a compelling call-to-action
   - End with a thought-provoking statement

**WRITING GUIDELINES:**
- Write in-depth, detailed paragraphs (4-6 sentences each)
- Expand on every point with examples and explanations
- Include relevant statistics, facts, or expert opinions
- Use transitions between sections
- Make every section substantial and informative
- DO NOT write short, superficial content
- Keep writing until you've provided {min_words}+ words of valuable content

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