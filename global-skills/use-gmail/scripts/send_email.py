#!/usr/bin/env python3
"""CLI script to send emails via Gmail.

Usage:
    python send_email.py --to recipient@example.com --subject "Hello" --body "Message body"
    python send_email.py --to recipient@example.com --subject "Hello" --body "<h1>HTML</h1>" --html
    python send_email.py --to recipient@example.com --subject "Hello" --body "See attached" --attachments file1.pdf file2.jpg
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
        description="Send an email via Gmail",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Send a simple text email
    python send_email.py --to user@example.com --subject "Hello" --body "Hi there!"

    # Send with CC and BCC
    python send_email.py --to user@example.com --cc other@example.com --subject "Meeting" --body "Let's meet"

    # Send HTML email
    python send_email.py --to user@example.com --subject "Newsletter" --body "<h1>Title</h1><p>Content</p>" --html

    # Send with attachments
    python send_email.py --to user@example.com --subject "Files" --body "See attached" --attachments report.pdf image.png
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
        "--cc",
        help="CC recipients, comma-separated"
    )
    parser.add_argument(
        "--bcc",
        help="BCC recipients, comma-separated"
    )
    parser.add_argument(
        "--html",
        action="store_true",
        help="Treat body as HTML"
    )
    parser.add_argument(
        "--attachments",
        nargs="+",
        help="File paths to attach"
    )
    parser.add_argument(
        "--credentials",
        help="Path to credentials.json file (optional)"
    )

    args = parser.parse_args()

    try:
        service = GmailService(credentials_path=args.credentials)
        result = service.send_email(
            to=args.to,
            subject=args.subject,
            body=args.body,
            cc=args.cc,
            bcc=args.bcc,
            html=args.html,
            attachments=args.attachments,
        )
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
