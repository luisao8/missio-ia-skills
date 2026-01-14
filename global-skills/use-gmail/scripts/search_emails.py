#!/usr/bin/env python3
"""CLI script to search emails in Gmail.

Usage:
    python search_emails.py --query "from:user@example.com"
    python search_emails.py --query "is:unread" --max-results 20
    python search_emails.py --label INBOX --max-results 5
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
        description="Search for emails in Gmail",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Gmail Query Examples:
    from:user@example.com       - Emails from a specific sender
    to:user@example.com         - Emails to a specific recipient
    subject:meeting             - Emails with "meeting" in subject
    is:unread                   - Unread emails
    is:starred                  - Starred emails
    has:attachment              - Emails with attachments
    after:2024/01/01            - Emails after a date
    before:2024/12/31           - Emails before a date
    newer_than:7d               - Emails from the last 7 days
    older_than:1m               - Emails older than 1 month
    larger:5M                   - Emails larger than 5MB
    "exact phrase"              - Emails containing exact phrase

Examples:
    python search_emails.py --query "from:boss@company.com is:unread"
    python search_emails.py --query "subject:invoice has:attachment" --max-results 20
    python search_emails.py --label INBOX --query "is:unread"
        """
    )
    parser.add_argument(
        "--query", "-q",
        default="",
        help="Gmail search query (e.g., 'from:user@example.com is:unread')"
    )
    parser.add_argument(
        "--max-results", "-n",
        type=int,
        default=10,
        help="Maximum number of results to return (default: 10)"
    )
    parser.add_argument(
        "--label", "-l",
        help="Filter by label (e.g., INBOX, SENT, DRAFT)"
    )
    parser.add_argument(
        "--credentials",
        help="Path to credentials.json file (optional)"
    )

    args = parser.parse_args()

    try:
        service = GmailService(credentials_path=args.credentials)
        results = service.search_emails(
            query=args.query,
            max_results=args.max_results,
            label=args.label,
        )
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
