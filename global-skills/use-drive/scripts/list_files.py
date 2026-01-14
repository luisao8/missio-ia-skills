#!/usr/bin/env python3
"""
CLI script to list files in a Google Drive folder.

Usage:
    python list_files.py
    python list_files.py --parent-id FOLDER_ID
    python list_files.py --max-results 50
    python list_files.py --mime-type application/pdf
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
        description="List files in a Google Drive folder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python list_files.py
  python list_files.py --parent-id 1abc123xyz
  python list_files.py --max-results 50 --mime-type application/pdf
  python list_files.py --mime-type "application/vnd.google-apps.folder"
        """,
    )
    parser.add_argument(
        "--parent-id",
        help="Parent folder ID (lists all files if not specified)",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=100,
        help="Maximum number of results (1-1000, default: 100)",
    )
    parser.add_argument(
        "--mime-type",
        help="Filter by MIME type",
    )
    parser.add_argument(
        "--order-by",
        default="modifiedTime desc",
        help="Sort order (default: 'modifiedTime desc')",
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

        result = service.list_files(
            parent_id=args.parent_id,
            max_results=args.max_results,
            mime_type=args.mime_type,
            order_by=args.order_by,
        )

        print(json.dumps(result, indent=2, default=str))

    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
