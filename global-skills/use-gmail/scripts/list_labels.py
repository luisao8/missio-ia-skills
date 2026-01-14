#!/usr/bin/env python3
"""CLI script to list all Gmail labels.

Usage:
    python list_labels.py
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
        description="List all Gmail labels",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # List all labels
    python list_labels.py

Output includes for each label:
    - id: Label ID (use this with add_label.py)
    - name: Label name
    - type: Label type (system or user)

Common system labels:
    - INBOX
    - SENT
    - DRAFT
    - TRASH
    - SPAM
    - STARRED
    - IMPORTANT
    - CATEGORY_PERSONAL
    - CATEGORY_SOCIAL
    - CATEGORY_PROMOTIONS
    - CATEGORY_UPDATES
    - CATEGORY_FORUMS
        """
    )
    parser.add_argument(
        "--credentials",
        help="Path to credentials.json file (optional)"
    )

    args = parser.parse_args()

    try:
        service = GmailService(credentials_path=args.credentials)
        results = service.list_labels()
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
