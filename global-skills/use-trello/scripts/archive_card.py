#!/usr/bin/env python3
"""
CLI script to archive (close) a Trello card.

Usage:
    python archive_card.py --card-id <card_id>

Output:
    JSON object of archived card
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from trello_service import TrelloService


def main() -> None:
    """Archive a Trello card."""
    parser = argparse.ArgumentParser(
        description="Archive (close) a Trello card"
    )
    parser.add_argument(
        "--card-id",
        required=True,
        help="Trello card ID",
    )
    args = parser.parse_args()

    try:
        service = TrelloService()
        card = service.archive_card(args.card_id)
        print(json.dumps(card, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
