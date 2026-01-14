#!/usr/bin/env python3
"""
CLI script to move a file to a different folder in Google Drive.

Usage:
    python move_file.py --file-id FILE_ID --new-parent-id FOLDER_ID
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from drive_service import get_drive_service


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Move a file to a different folder in Google Drive",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python move_file.py --file-id 1abc123xyz --new-parent-id 1def456uvw
        """,
    )
    parser.add_argument(
        "--file-id",
        required=True,
        help="ID of the file to move",
    )
    parser.add_argument(
        "--new-parent-id",
        required=True,
        help="ID of the new parent folder",
    )
    parser.add_argument(
        "--credentials-path",
        help="Path to OAuth credentials JSON file",
    )
    parser.add_argument(
        "--token-path",
        help="Path to user token file",
    )

    args = parser.parse_args()

    try:
        service = get_drive_service(
            credentials_path=args.credentials_path,
            token_path=args.token_path,
        )

        result = service.move_file(
            file_id=args.file_id,
            new_parent_id=args.new_parent_id,
        )

        print(json.dumps(result, indent=2, default=str))

    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
