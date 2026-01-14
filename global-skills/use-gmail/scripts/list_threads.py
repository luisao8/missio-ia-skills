#!/usr/bin/env python3
"""CLI script to list email threads in Gmail.

Usage:
    python list_threads.py
    python list_threads.py --query "from:user@example.com"
    python list_threads.py --max-results 20
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from gmail_service import GmailService


def main():
    parser = argparse.ArgumentParser(
        description="List email threads in Gmail",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # List recent threads
    python list_threads.py

    # List threads from a specific sender
    python list_threads.py --query "from:boss@company.com"

    # List more threads
    python list_threads.py --max-results 25

    # List unread threads
    python list_threads.py --query "is:unread"

Output includes for each thread:
    - id: Thread ID
    - snippet: Preview of the thread
    - messageCount: Number of messages in thread
    - subject: Thread subject
    - from: First sender
    - date: Date of first message
        """
    )
    parser.add_argument(
        "--query", "-q",
        default="",
        help="Gmail search query to filter threads"
    )
    parser.add_argument(
        "--max-results", "-n",
        type=int,
        default=10,
        help="Maximum number of threads to return (default: 10)"
    )
    parser.add_argument(
        "--credentials",
        help="Path to credentials.json file (optional)"
    )

    args = parser.parse_args()

    try:
        service = GmailService(credentials_path=args.credentials)
        results = service.list_threads(
            query=args.query,
            max_results=args.max_results,
        )
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
