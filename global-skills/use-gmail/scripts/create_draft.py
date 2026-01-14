#!/usr/bin/env python3
"""CLI script to create an email draft in Gmail.

Usage:
    python create_draft.py --to recipient@example.com --subject "Draft Subject" --body "Draft content"
    python create_draft.py --to recipient@example.com --subject "HTML Draft" --body "<h1>Hello</h1>" --html
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
        description="Create an email draft in Gmail",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Create a simple text draft
    python create_draft.py --to user@example.com --subject "Meeting Notes" --body "Here are the notes..."

    # Create an HTML draft
    python create_draft.py --to user@example.com --subject "Report" --body "<h1>Report</h1><p>Details here</p>" --html

Notes:
    - Draft will appear in Gmail's Drafts folder
    - You can edit and send the draft later from Gmail
    - Returns the draft ID and message ID
        """
    )
    parser.add_argument(
        "--to",
        required=True,
        help="Recipient email address(es), comma-separated"
    )
    parser.add_argument(
        "--subject",
        required=True,
        help="Email subject"
    )
    parser.add_argument(
        "--body",
        required=True,
        help="Email body (text or HTML if --html flag is used)"
    )
    parser.add_argument(
        "--html",
        action="store_true",
        help="Treat body as HTML"
    )
    parser.add_argument(
        "--credentials",
        help="Path to credentials.json file (optional)"
    )

    args = parser.parse_args()

    try:
        service = GmailService(credentials_path=args.credentials)
        result = service.create_draft(
            to=args.to,
            subject=args.subject,
            body=args.body,
            html=args.html,
        )
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
