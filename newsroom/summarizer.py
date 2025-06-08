"""
LLM-based summarization using OpenAI's API.
"""

import os
import logging
from typing import List, Optional
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

logger = logging.getLogger(__name__)

class LLMSummarizer:
    """Handles article and daily digest summarization using OpenAI."""
    
    def __init__(self, model: str = "gpt-4o"):
        """Initialize the summarizer.
        
        Args:
            model: OpenAI model to use (default: gpt-4o)
        """
        # Load environment variables
        load_dotenv()
        
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
            
        self.model = model
        self.client = OpenAI(api_key=self.api_key)
        
    def summarize_article(self, content: str) -> Optional[str]:
        """Generate a concise summary of a news article.
        
        Args:
            content: The article text to summarize
            
        Returns:
            A 2-3 sentence summary, or None if summarization fails
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": (
                        "You are a news summarizer. Create concise, factual summaries "
                        "in 2-3 sentences. Focus on key information and maintain "
                        "journalistic neutrality."
                    )},
                    {"role": "user", "content": f"Summarize this news article:\n\n{content}"}
                ],
                max_tokens=150,
                temperature=0.5
            )
            return response.choices[0].message.content.strip()
            
        except OpenAIError as e:
            logger.warning(f"Failed to summarize article: {str(e)}")
            return None
            
    def summarize_day(self, summaries: List[str]) -> Optional[str]:
        """Generate a daily overview from multiple article summaries.
        
        Args:
            summaries: List of article summaries to synthesize
            
        Returns:
            A concise overview of the day's news, or None if summarization fails
        """
        if not summaries:
            return None
            
        try:
            # Combine summaries into a single text
            combined = "\n\n".join([f"- {s}" for s in summaries if s])
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": (
                        "You are a news editor creating daily briefings. Synthesize "
                        "multiple stories into a concise overview that captures the "
                        "most significant developments of the day. Be factual and "
                        "objective."
                    )},
                    {"role": "user", "content": (
                        f"Create a brief overview of today's top stories based on "
                        f"these summaries:\n\n{combined}"
                    )}
                ],
                max_tokens=200,
                temperature=0.5
            )
            return response.choices[0].message.content.strip()
            
        except OpenAIError as e:
            logger.warning(f"Failed to generate daily overview: {str(e)}")
            return None 