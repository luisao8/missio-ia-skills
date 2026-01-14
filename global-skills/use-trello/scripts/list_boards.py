#!/usr/bin/env python3
"""
CLI script to list all Trello boards for the authenticated user.

Usage:
    python list_boards.py

Output:
    JSON array of board objects
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from trello_service import TrelloService


def main() -> None:
    """List all Trello boards."""
    parser = argparse.ArgumentParser(
        description="List all Trello boards for the authenticated user"
    )
    parser.parse_args()

    try:
        service = TrelloService()
        boards = service.get_boards()
        print(json.dumps(boards, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
