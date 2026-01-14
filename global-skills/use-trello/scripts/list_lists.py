#!/usr/bin/env python3
"""
CLI script to list all lists in a Trello board.

Usage:
    python list_lists.py --board-id <board_id>

Output:
    JSON array of list objects
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from trello_service import TrelloService


def main() -> None:
    """List all lists in a Trello board."""
    parser = argparse.ArgumentParser(
        description="List all lists in a Trello board"
    )
    parser.add_argument(
        "--board-id",
        required=True,
        help="Trello board ID",
    )
    args = parser.parse_args()

    try:
        service = TrelloService()
        lists = service.get_lists(args.board_id)
        print(json.dumps(lists, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
