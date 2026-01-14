#!/usr/bin/env python3
"""
CLI script to list cards from a Trello list or board.

Usage:
    python list_cards.py --list-id <list_id>
    python list_cards.py --board-id <board_id>

Output:
    JSON array of card objects
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from trello_service import TrelloService


def main() -> None:
    """List cards from a Trello list or board."""
    parser = argparse.ArgumentParser(
        description="List cards from a Trello list or board"
    )
    parser.add_argument(
        "--list-id",
        help="Trello list ID",
    )
    parser.add_argument(
        "--board-id",
        help="Trello board ID",
    )
    args = parser.parse_args()

    if not args.list_id and not args.board_id:
        print(json.dumps({"error": "Either --list-id or --board-id must be provided"}))
        sys.exit(1)

    try:
        service = TrelloService()
        cards = service.get_cards(list_id=args.list_id, board_id=args.board_id)
        print(json.dumps(cards, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
