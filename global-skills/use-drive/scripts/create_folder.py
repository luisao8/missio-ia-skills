#!/usr/bin/env python3
"""
CLI script to create a folder in Google Drive.

Usage:
    python create_folder.py --name "My New Folder"
    python create_folder.py --name "Subfolder" --parent-id FOLDER_ID
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
        description="Create a folder in Google Drive",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python create_folder.py --name "My New Folder"
  python create_folder.py --name "Subfolder" --parent-id 1abc123xyz
        """,
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Name of the folder to create",
    )
    parser.add_argument(
        "--parent-id",
        help="Parent folder ID (defaults to root)",
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

        result = service.create_folder(
            name=args.name,
            parent_id=args.parent_id,
        )

        print(json.dumps(result, indent=2, default=str))

    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
