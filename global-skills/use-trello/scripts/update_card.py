#!/usr/bin/env python3
"""
CLI script to update an existing Trello card.

Usage:
    python update_card.py --card-id <card_id> [--name "New Name"] [--desc "New Desc"] [--due "2024-12-31"] [--closed true/false]

Output:
    JSON object of updated card
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from trello_service import TrelloService


def main() -> None:
    """Update an existing Trello card."""
    parser = argparse.ArgumentParser(
        description="Update an existing Trello card"
    )
    parser.add_argument(
        "--card-id",
        required=True,
        help="Trello card ID",
    )
    parser.add_argument(
        "--name",
        help="New card name",
    )
    parser.add_argument(
        "--desc",
        help="New card description",
    )
    parser.add_argument(
        "--due",
        help="New due date in ISO format (e.g., 2024-12-31)",
    )
    parser.add_argument(
        "--closed",
        choices=["true", "false"],
        help="Set card archived status",
    )
    args = parser.parse_args()

    # Build update kwargs
    update_kwargs = {}
    if args.name:
        update_kwargs["name"] = args.name
    if args.desc:
        update_kwargs["desc"] = args.desc
    if args.due:
        update_kwargs["due"] = args.due
    if args.closed:
        update_kwargs["closed"] = args.closed

    if not update_kwargs:
        print(json.dumps({"error": "At least one update field must be provided"}))
        sys.exit(1)

    try:
        service = TrelloService()
        card = service.update_card(args.card_id, **update_kwargs)
        print(json.dumps(card, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
