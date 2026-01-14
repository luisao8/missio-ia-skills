#!/usr/bin/env python3
"""
CLI script to search for files in Google Drive.

Usage:
    python search_files.py --query "name contains 'report'"
    python search_files.py --query "mimeType='application/pdf'"
    python search_files.py --query "fullText contains 'budget'" --max-results 50
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
        description="Search for files in Google Drive",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Drive Search Query Examples:
  --query "name contains 'report'"
  --query "mimeType='application/pdf'"
  --query "fullText contains 'budget'"
  --query "'FOLDER_ID' in parents"
  --query "modifiedTime > '2024-01-01'"
  --query "name contains 'report' and mimeType='application/pdf'"
  --query "trashed = false"

Common MIME types:
  application/vnd.google-apps.folder     (folder)
  application/vnd.google-apps.document   (Google Doc)
  application/vnd.google-apps.spreadsheet (Google Sheet)
  application/pdf                        (PDF file)
        """,
    )
    parser.add_argument(
        "--query",
        required=True,
        help="Search query using Drive search operators",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=100,
        help="Maximum number of results (1-1000, default: 100)",
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

        result = service.search_files(
            query=args.query,
            max_results=args.max_results,
        )

        print(json.dumps(result, indent=2, default=str))

    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
