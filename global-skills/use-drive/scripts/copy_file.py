#!/usr/bin/env python3
"""
CLI script to copy a file in Google Drive.

Usage:
    python copy_file.py --file-id FILE_ID
    python copy_file.py --file-id FILE_ID --new-name "Copy of Document.pdf"
    python copy_file.py --file-id FILE_ID --parent-id FOLDER_ID
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
        description="Copy a file in Google Drive",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python copy_file.py --file-id 1abc123xyz
  python copy_file.py --file-id 1abc123xyz --new-name "Copy of Document.pdf"
  python copy_file.py --file-id 1abc123xyz --parent-id 1def456uvw
  python copy_file.py --file-id 1abc123xyz --new-name "Backup.pdf" --parent-id 1def456uvw
        """,
    )
    parser.add_argument(
        "--file-id",
        required=True,
        help="ID of the file to copy",
    )
    parser.add_argument(
        "--new-name",
        help="Name for the copy (defaults to 'Copy of [original]')",
    )
    parser.add_argument(
        "--parent-id",
        help="Parent folder for the copy",
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

        result = service.copy_file(
            file_id=args.file_id,
            new_name=args.new_name,
            parent_id=args.parent_id,
        )

        print(json.dumps(result, indent=2, default=str))

    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
