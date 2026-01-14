#!/usr/bin/env python3
"""
CLI script to add a comment to a Trello card.

Usage:
    python add_comment.py --card-id <card_id> --text "Comment text"

Output:
    JSON object of created comment
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from trello_service import TrelloService


def main() -> None:
    """Add a comment to a Trello card."""
    parser = argparse.ArgumentParser(
        description="Add a comment to a Trello card"
    )
    parser.add_argument(
        "--card-id",
        required=True,
        help="Trello card ID",
    )
    parser.add_argument(
        "--text",
        required=True,
        help="Comment text",
    )
    args = parser.parse_args()

    try:
        service = TrelloService()
        comment = service.add_comment(args.card_id, args.text)
        print(json.dumps(comment, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
