#!/usr/bin/env python3
"""
CLI script to get information about a file in Google Drive.

Usage:
    python get_file_info.py --file-id FILE_ID
    python get_file_info.py --file-id FILE_ID --fields "id,name,size,mimeType"
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
        description="Get information about a file in Google Drive",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python get_file_info.py --file-id 1abc123xyz
  python get_file_info.py --file-id 1abc123xyz --fields "id,name,size,mimeType"

Common fields:
  id, name, mimeType, size, createdTime, modifiedTime,
  parents, webViewLink, webContentLink, owners, shared,
  permissions, description, starred, trashed
        """,
    )
    parser.add_argument(
        "--file-id",
        required=True,
        help="ID of the file to get info for",
    )
    parser.add_argument(
        "--fields",
        default="*",
        help="Comma-separated fields to retrieve (default: all)",
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

        result = service.get_file_info(
            file_id=args.file_id,
            fields=args.fields,
        )

        print(json.dumps(result, indent=2, default=str))

    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
