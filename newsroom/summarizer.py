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
    
    # Default prompts for summarization
    ARTICLE_PROMPT = (
        "You are a news summarizer. Create concise, factual summaries "
        "in 2-3 sentences. Focus on key information and maintain "
        "journalistic neutrality."
    )
    
    DAILY_PROMPT = (
        "You are a news editor creating daily briefings. Synthesize "
        "multiple stories into a concise overview that captures the "
        "most significant developments of the day. Be factual and "
        "objective."
    )
    
    def __init__(
        self,
        model: str = "gpt-4o",
        article_max_tokens: int = 150,
        daily_max_tokens: int = 200,
        temperature: float = 0.5
    ):
        """Initialize the summarizer.
        
        Args:
            model: OpenAI model to use (default: gpt-4o)
            article_max_tokens: Max tokens for article summaries (default: 150)
            daily_max_tokens: Max tokens for daily overview (default: 200)
            temperature: Model temperature (default: 0.5)
        """
        # Load environment variables
        load_dotenv()
        
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
            
        self.model = model
        self.article_max_tokens = article_max_tokens
        self.daily_max_tokens = daily_max_tokens
        self.temperature = temperature
        
        try:
            self.client = OpenAI(api_key=self.api_key)
        except Exception as e:
            raise ValueError(f"Failed to initialize OpenAI client: {str(e)}")
            
    def _generate_completion(
        self,
        prompt: str,
        content: str,
        max_tokens: int
    ) -> Optional[str]:
        """Generate a completion using OpenAI's API.
        
        Args:
            prompt: System prompt for the model
            content: User content to process
            max_tokens: Maximum tokens in response
            
        Returns:
            Generated text or None if generation fails
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": content}
                ],
                max_tokens=max_tokens,
                temperature=self.temperature
            )
            return response.choices[0].message.content.strip()
            
        except OpenAIError as e:
            logger.warning(f"OpenAI API error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during completion: {str(e)}")
            return None
            
    def summarize_article(self, content: str) -> Optional[str]:
        """Generate a concise summary of a news article.
        
        Args:
            content: The article text to summarize
            
        Returns:
            A 2-3 sentence summary, or None if summarization fails
        """
        return self._generate_completion(
            prompt=self.ARTICLE_PROMPT,
            content=f"Summarize this news article:\n\n{content}",
            max_tokens=self.article_max_tokens
        )
            
    def summarize_day(self, summaries: List[str]) -> Optional[str]:
        """Generate a daily overview from multiple article summaries.
        
        Args:
            summaries: List of article summaries to synthesize
            
        Returns:
            A concise overview of the day's news, or None if summarization fails
        """
        if not summaries:
            return None
            
        # Combine summaries into a single text
        combined = "\n\n".join([f"- {s}" for s in summaries if s])
        
        return self._generate_completion(
            prompt=self.DAILY_PROMPT,
            content=f"Create a brief overview of today's top stories based on these summaries:\n\n{combined}",
            max_tokens=self.daily_max_tokens
        ) 