#!/usr/bin/env python3
"""
CLI script to create a new card in a Trello list.

Usage:
    python create_card.py --list-id <list_id> --name "Card Name" [--desc "Description"] [--due "2024-12-31"] [--labels "label1,label2"]

Output:
    JSON object of created card
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from trello_service import TrelloService


def main() -> None:
    """Create a new card in a Trello list."""
    parser = argparse.ArgumentParser(
        description="Create a new card in a Trello list"
    )
    parser.add_argument(
        "--list-id",
        required=True,
        help="Target Trello list ID",
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Card name",
    )
    parser.add_argument(
        "--desc",
        help="Card description",
    )
    parser.add_argument(
        "--due",
        help="Due date in ISO format (e.g., 2024-12-31)",
    )
    parser.add_argument(
        "--labels",
        help="Comma-separated label IDs",
    )
    args = parser.parse_args()

    # Parse labels if provided
    labels = args.labels.split(",") if args.labels else None

    try:
        service = TrelloService()
        card = service.create_card(
            list_id=args.list_id,
            name=args.name,
            desc=args.desc,
            due=args.due,
            labels=labels,
        )
        print(json.dumps(card, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
