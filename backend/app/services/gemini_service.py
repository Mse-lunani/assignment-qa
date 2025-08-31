import os
import google.generativeai as genai
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
    async def generate_response(self, query: str) -> str:
        try:
            # Create a specialized prompt for Kenyan leaders
            prompt = f"""
            You are a knowledgeable assistant specializing in Kenyan political leadership and government structure. 
            Please provide accurate, up-to-date information about Kenyan leaders including governors, senators, MCAs, 
            MPs, and other political positions.
            
            User Question: {query}
            
            Please provide a clear, informative response. If you don't have current information, 
            please indicate that the information might be outdated and suggest checking official sources.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating response with Gemini: {str(e)}")
            raise Exception(f"Failed to generate response: {str(e)}")

# Initialize service instance
gemini_service = GeminiService()