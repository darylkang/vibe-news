"""
Google News scraper for newsroom.

This module handles scraping top stories from Google News.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from datetime import datetime
import logging

from .base import NewsSource

logger = logging.getLogger(__name__)

class GoogleNewsScraper(NewsSource):
    """Scrapes top stories from Google News."""
    
    BASE_URL = "https://news.google.com/rss"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    def __init__(self, max_stories: int = 10):
        """Initialize the scraper.
        
        Args:
            max_stories: Maximum number of stories to fetch (default: 10)
        """
        self.max_stories = max_stories

    def _parse_story_item(self, item) -> Optional[Dict[str, str]]:
        """Parse a single RSS item into a story dictionary.
        
        Args:
            item: BeautifulSoup item tag
            
        Returns:
            Story dictionary or None if parsing fails
        """
        try:
            # Extract source from the title format "Title - Source"
            title_parts = item.title.text.split(' - ')
            source = title_parts[-1] if len(title_parts) > 1 else "Unknown Source"
            title = ' - '.join(title_parts[:-1]) if len(title_parts) > 1 else title_parts[0]
            
            # Parse and format the publication date
            pub_date = datetime.strptime(
                item.pubDate.text, 
                '%a, %d %b %Y %H:%M:%S %Z'
            )
            
            return {
                'title': title.strip(),
                'url': item.link.text,
                'source': source.strip(),
                'published': pub_date.strftime('%Y-%m-%d %H:%M:%S'),
                'summary': item.description.text if item.description else None
            }
            
        except (AttributeError, ValueError) as e:
            logger.warning(
                "Failed to parse story item: %s. Error: %s",
                item.get_text(strip=True)[:100], str(e)
            )
            return None

    def fetch_top_stories(self) -> List[Dict[str, str]]:
        """Fetch top stories from Google News.
        
        Returns:
            List of story dictionaries
        """
        try:
            response = requests.get(self.BASE_URL, headers=self.HEADERS)
            response.raise_for_status()
            
            # Parse RSS feed with lxml-xml parser
            soup = BeautifulSoup(response.content, "lxml-xml")
            items = soup.find_all('item', limit=self.max_stories)
            
            if not items:
                logger.warning(
                    "No <item> tags found in Google News RSS feed. "
                    "Response content length: %d bytes. "
                    "Response status code: %d",
                    len(response.content), response.status_code
                )
                return []
            
            stories = []
            for item in items:
                story = self._parse_story_item(item)
                if story:
                    stories.append(story)
            
            if not stories:
                logger.warning(
                    "Successfully parsed RSS feed but no valid stories were extracted. "
                    "Check the feed format and item structure."
                )
            
            return stories
            
        except requests.RequestException as e:
            logger.error("Failed to fetch Google News RSS feed: %s", str(e))
            return []
        except Exception as e:
            logger.error(
                "Unexpected error while processing Google News feed: %s. "
                "This might indicate a change in the feed format.",
                str(e)
            )
            return []

    def get_stories(self) -> List[Dict[str, str]]:
        """Public method to get formatted stories.
        
        Returns:
            List of story dictionaries ready for markdown generation.
        """
        return self.fetch_top_stories() 