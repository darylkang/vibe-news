"""
Base class for news sources.
"""

from abc import ABC, abstractmethod
from typing import List, Dict

class NewsSource(ABC):
    """Abstract base class for news sources."""
    
    @abstractmethod
    def get_stories(self) -> List[Dict[str, str]]:
        """Fetch stories from the news source.
        
        Returns:
            List of dictionaries containing story information:
            {
                'title': str,
                'url': str,
                'source': str,
                'published': str,
                'summary': Optional[str]
            }
        """
        pass 