#!/usr/bin/env python3
"""CLI script to reply to an email in Gmail.

Usage:
    python reply_email.py --message-id 18abc123def456 --body "Thanks for your email!"
    python reply_email.py --message-id 18abc123def456 --body "<p>HTML reply</p>" --html
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
        description="Reply to an email in Gmail",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Reply with plain text
    python reply_email.py --message-id 18abc123def456 --body "Thanks for your message!"

    # Reply with HTML
    python reply_email.py --message-id 18abc123def456 --body "<p>Thanks!</p>" --html

Notes:
    - The reply will be sent to the original sender
    - Subject will automatically have "Re:" prefix
    - Reply will be threaded with the original conversation
    - Use read_email.py to get the message ID
        """
    )
    parser.add_argument(
        "--message-id", "-m",
        required=True,
        help="The message ID to reply to"
    )
    parser.add_argument(
        "--body", "-b",
        required=True,
        help="Reply body (text or HTML if --html flag is used)"
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
        result = service.reply_email(
            message_id=args.message_id,
            body=args.body,
            html=args.html,
        )
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
