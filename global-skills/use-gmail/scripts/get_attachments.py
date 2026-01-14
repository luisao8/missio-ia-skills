#!/usr/bin/env python3
"""CLI script to download attachments from a Gmail message.

Usage:
    python get_attachments.py --message-id 18abc123def456 --output-dir ./downloads
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
        description="Download attachments from a Gmail message",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Download attachments to current directory
    python get_attachments.py --message-id 18abc123def456 --output-dir .

    # Download to a specific folder
    python get_attachments.py --message-id 18abc123def456 --output-dir ~/Downloads/email-attachments

    # Find emails with attachments first
    python search_emails.py --query "has:attachment from:sender@example.com"

Output includes for each downloaded file:
    - filename: Name of the file
    - path: Full path where file was saved
    - size: Size in bytes
    - mimeType: MIME type of the file

Notes:
    - Output directory will be created if it doesn't exist
    - Existing files with same name will be overwritten
    - Use search_emails.py with "has:attachment" to find emails with attachments
        """
    )
    parser.add_argument(
        "--message-id", "-m",
        required=True,
        help="The message ID to download attachments from"
    )
    parser.add_argument(
        "--output-dir", "-o",
        required=True,
        help="Directory to save attachments"
    )
    parser.add_argument(
        "--credentials",
        help="Path to credentials.json file (optional)"
    )

    args = parser.parse_args()

    try:
        service = GmailService(credentials_path=args.credentials)
        results = service.get_attachments(
            message_id=args.message_id,
            output_dir=args.output_dir,
        )

        if not results:
            print(json.dumps({"message": "No attachments found in this email"}))
        else:
            print(json.dumps(results, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
