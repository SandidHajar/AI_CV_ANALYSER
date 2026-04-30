import json
import logging
from typing import Dict, Any, Optional
from openai import AsyncOpenAI
from app.config.settings import get_settings

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        settings = get_settings()
        self.client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            timeout=settings.openai_timeout
        )

    async def analyze_cv(self, cv_text: str) -> Optional[Dict[str, Any]]:
        settings = get_settings()
        if not settings.openai_api_key:
            logger.warning("OpenAI API key missing")
            return None

        prompt = """
        Analyze this CV professionally and return a JSON object with:
        - "summary": A 2-line impactful professional summary.
        - "strengths": A list of exactly 3 professional strengths.
        - "weaknesses": A list of exactly 2 areas for improvement.
        - "role_level": Junior, Mid, or Senior.
        - "score_adjustment": An integer between -10 and 10 based on CV quality, formatting, and impact.
        - "confidence": A float between 0.0 and 1.0 representing analysis reliability.
        - "interpretation": A short sentence about the candidate's market fit.
        """

        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert Senior Technical Recruiter. Always respond in valid JSON format."},
                    {"role": "user", "content": f"{prompt}\n\nCV Text: {cv_text}"}
                ],
                response_format={ "type": "json_object" },
                temperature=0.3, # Lower temperature for more consistent results
                max_tokens=800
            )

            result_content = response.choices[0].message.content
            if not result_content:
                return None
                
            data = json.loads(result_content)
            # Basic validation of keys
            required = ["summary", "strengths", "weaknesses", "role_level", "score_adjustment", "confidence"]
            if all(key in data for key in required):
                return data
            return None

        except Exception as e:
            logger.error(f"Error calling OpenAI API: {str(e)}")
            return None

openai_service = OpenAIService()
