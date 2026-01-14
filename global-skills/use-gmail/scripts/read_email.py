#!/usr/bin/env python3
"""CLI script to read a specific email from Gmail.

Usage:
    python read_email.py --message-id 18abc123def456
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
        description="Read a specific email from Gmail",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Read an email by its message ID
    python read_email.py --message-id 18abc123def456

    # Get the message ID from search_emails.py first
    python search_emails.py --query "from:boss@company.com" --max-results 1
    # Then use the "id" field from the result

Output includes:
    - id: Message ID
    - threadId: Thread ID
    - subject: Email subject
    - from: Sender
    - to: Recipients
    - cc: CC recipients
    - date: Email date
    - body: Plain text body
    - htmlBody: HTML body (if available)
    - attachments: List of attachments with metadata
        """
    )
    parser.add_argument(
        "--message-id", "-m",
        required=True,
        help="The message ID to read"
    )
    parser.add_argument(
        "--credentials",
        help="Path to credentials.json file (optional)"
    )

    args = parser.parse_args()

    try:
        service = GmailService(credentials_path=args.credentials)
        result = service.read_email(message_id=args.message_id)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
