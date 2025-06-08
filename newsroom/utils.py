"""
Utility functions for the newsroom package.
"""

import os
from datetime import datetime
from typing import Optional
import re

def format_date_for_title(date: Optional[datetime] = None) -> str:
    """Format a date for use in the markdown title.
    
    Args:
        date: datetime object (defaults to today if None)
    
    Returns:
        Formatted date string like "June 7, 2025"
    """
    date = date or datetime.now()
    return date.strftime("%B %-d, %Y")

def get_file_path(date: Optional[datetime] = None) -> str:
    """Get the file path for a given date's digest.
    
    Args:
        date: datetime object (defaults to today if None)
    
    Returns:
        Path to the markdown file (e.g., "content/2025-06-07.md")
    """
    date = date or datetime.now()
    return os.path.join("content", f"{date.strftime('%Y-%m-%d')}.md")

def ensure_content_dir() -> None:
    """Ensure the content directory exists."""
    os.makedirs("content", exist_ok=True)

def slugify(text: str) -> str:
    """Convert text to URL-friendly slug.
    
    Args:
        text: String to convert
    
    Returns:
        URL-friendly version of the text
    """
    # Convert to lowercase and replace spaces with hyphens
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text

def time_ago(timestamp: str) -> str:
    """Convert timestamp to "time ago" format.
    
    Args:
        timestamp: ISO format timestamp string
    
    Returns:
        String like "5h ago" or "2d ago"
        
    Raises:
        ValueError: If timestamp is invalid
    """
    try:
        now = datetime.now()
        then = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        delta = now - then
        
        hours = delta.total_seconds() / 3600
        if hours < 24:
            return f"{int(hours)}h ago"
        days = int(hours / 24)
        return f"{days}d ago"
    except ValueError as e:
        raise ValueError(f"Invalid timestamp format: {str(e)}") 