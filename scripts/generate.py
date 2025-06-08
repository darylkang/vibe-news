#!/usr/bin/env python3
"""
CLI script to generate news digests.
"""

import argparse
import logging
from datetime import datetime
import sys

from newsroom.generator import NewsDigestGenerator

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
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Parse date if provided
    target_date = None
    if args.date:
        try:
            target_date = datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError:
            logging.error("Invalid date format. Use YYYY-MM-DD")
            sys.exit(1)
    
    # Log configuration
    if args.verbose:
        logging.debug("Configuration:")
        logging.debug(f"  Date: {args.date or 'today'}")
        logging.debug(f"  Stories: {args.stories}")
        logging.debug(f"  LLM Enabled: {not args.no_llm}")
        if not args.no_llm:
            logging.debug(f"  Model: {args.model}")
    
    # Generate digest
    generator = NewsDigestGenerator(
        max_stories=args.stories,
        use_llm=not args.no_llm,
        llm_model=args.model
    )
    success = generator.generate_digest(
        date=target_date,
        force=args.force
    )
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 