#!/usr/bin/env python3
"""
CLI script to add a label to a Trello card.

Usage:
    python add_label.py --card-id <card_id> --label-id <label_id>

Output:
    JSON with result (list of label IDs on card)
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from trello_service import TrelloService


def main() -> None:
    """Add a label to a Trello card."""
    parser = argparse.ArgumentParser(
        description="Add a label to a Trello card"
    )
    parser.add_argument(
        "--card-id",
        required=True,
        help="Trello card ID",
    )
    parser.add_argument(
        "--label-id",
        required=True,
        help="Trello label ID",
    )
    args = parser.parse_args()

    try:
        service = TrelloService()
        result = service.add_label(args.card_id, args.label_id)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
