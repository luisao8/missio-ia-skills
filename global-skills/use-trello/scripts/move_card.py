#!/usr/bin/env python3
"""
CLI script to move a Trello card to a different list.

Usage:
    python move_card.py --card-id <card_id> --list-id <list_id>

Output:
    JSON object of moved card
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from trello_service import TrelloService


def main() -> None:
    """Move a Trello card to a different list."""
    parser = argparse.ArgumentParser(
        description="Move a Trello card to a different list"
    )
    parser.add_argument(
        "--card-id",
        required=True,
        help="Trello card ID",
    )
    parser.add_argument(
        "--list-id",
        required=True,
        help="Target Trello list ID",
    )
    args = parser.parse_args()

    try:
        service = TrelloService()
        card = service.move_card(args.card_id, args.list_id)
        print(json.dumps(card, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
