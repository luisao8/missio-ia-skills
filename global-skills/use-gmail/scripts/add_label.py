#!/usr/bin/env python3
"""CLI script to add a label to a Gmail message.

Usage:
    python add_label.py --message-id 18abc123def456 --label-id STARRED
    python add_label.py --message-id 18abc123def456 --label-id Label_123
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
        description="Add a label to a Gmail message",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Star a message
    python add_label.py --message-id 18abc123def456 --label-id STARRED

    # Mark as important
    python add_label.py --message-id 18abc123def456 --label-id IMPORTANT

    # Add a custom label (use list_labels.py to get label IDs)
    python add_label.py --message-id 18abc123def456 --label-id Label_123

Common system label IDs:
    - STARRED
    - IMPORTANT
    - INBOX
    - TRASH
    - SPAM

Notes:
    - Use list_labels.py to see all available labels and their IDs
    - Use search_emails.py to get message IDs
        """
    )
    parser.add_argument(
        "--message-id", "-m",
        required=True,
        help="The message ID to add the label to"
    )
    parser.add_argument(
        "--label-id", "-l",
        required=True,
        help="The label ID to add (e.g., STARRED, IMPORTANT, or custom label ID)"
    )
    parser.add_argument(
        "--credentials",
        help="Path to credentials.json file (optional)"
    )

    args = parser.parse_args()

    try:
        service = GmailService(credentials_path=args.credentials)
        result = service.add_label(
            message_id=args.message_id,
            label_id=args.label_id,
        )
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
