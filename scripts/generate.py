#!/usr/bin/env python3
"""
CLI script to generate news digests.
"""

import argparse
import logging
from datetime import datetime
import sys

from newsroom.generator import NewsDigestGenerator

def setup_logging(verbose: bool = False) -> None:
    """Configure logging with appropriate level and format.
    
    Args:
        verbose: Whether to enable debug logging
    """
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def parse_date(date_str: str) -> datetime:
    """Parse date string into datetime object.
    
    Args:
        date_str: Date string in YYYY-MM-DD format
        
    Returns:
        datetime object
        
    Raises:
        ValueError: If date format is invalid
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")

def main():
    """Main entry point for the generator CLI."""
    parser = argparse.ArgumentParser(
        description="Generate a daily news digest with optional AI-powered summarization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate digest with default settings (GPT-4o summarization)
  python scripts/generate.py
  
  # Generate digest without AI summarization
  python scripts/generate.py --no-llm
  
  # Use a different OpenAI model
  python scripts/generate.py --model gpt-3.5-turbo
  
  # Generate digest for a specific date
  python scripts/generate.py --date 2025-06-07
  
  # Customize output directory
  python scripts/generate.py --output-dir src/content/digests
  
  # Adjust model temperature
  python scripts/generate.py --temperature 0.7
"""
    )
    
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Force regeneration even if digest exists"
    )
    parser.add_argument(
        "--date", "-d",
        help="Generate digest for specific date (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--stories", "-n",
        type=int,
        default=10,
        help="Maximum number of stories to include (default: 10)"
    )
    parser.add_argument(
        "--no-llm",
        action="store_true",
        help="Disable AI-powered summarization"
    )
    parser.add_argument(
        "--model",
        default="gpt-4o",
        help="OpenAI model to use for summarization (default: gpt-4o, ignored if --no-llm is set)"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.5,
        help="Model temperature (default: 0.5, ignored if --no-llm is set)"
    )
    parser.add_argument(
        "--output-dir",
        default="content",
        help="Directory for output files (default: content)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Configure logging
    setup_logging(args.verbose)
    
    # Parse date if provided
    target_date = None
    if args.date:
        try:
            target_date = parse_date(args.date)
        except ValueError as e:
            logging.error(str(e))
            sys.exit(1)
    
    # Log configuration
    if args.verbose:
        logging.debug("Configuration:")
        logging.debug(f"  Date: {args.date or 'today'}")
        logging.debug(f"  Stories: {args.stories}")
        logging.debug(f"  Output Directory: {args.output_dir}")
        logging.debug(f"  LLM Enabled: {not args.no_llm}")
        if not args.no_llm:
            logging.debug(f"  Model: {args.model}")
            logging.debug(f"  Temperature: {args.temperature}")
    
    try:
        # Generate digest
        generator = NewsDigestGenerator(
            max_stories=args.stories,
            use_llm=not args.no_llm,
            llm_model=args.model,
            llm_temperature=args.temperature,
            output_dir=args.output_dir
        )
        success = generator.generate_digest(
            date=target_date,
            force=args.force
        )
        
        sys.exit(0 if success else 1)
        
    except Exception as e:
        logging.error(f"Failed to generate digest: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 