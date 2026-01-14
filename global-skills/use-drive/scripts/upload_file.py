#!/usr/bin/env python3
"""
CLI script to upload a file to Google Drive.

Usage:
    python upload_file.py --file-path /path/to/file.pdf
    python upload_file.py --file-path /path/to/file.pdf --name "My Document.pdf"
    python upload_file.py --file-path /path/to/file.pdf --parent-id FOLDER_ID
    python upload_file.py --file-path /path/to/file.pdf --mime-type application/pdf
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
        description="Upload a file to Google Drive",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python upload_file.py --file-path /path/to/file.pdf
  python upload_file.py --file-path /path/to/file.pdf --name "Renamed.pdf"
  python upload_file.py --file-path /path/to/file.pdf --parent-id 1abc123xyz
        """,
    )
    parser.add_argument(
        "--file-path",
        required=True,
        help="Local file path to upload",
    )
    parser.add_argument(
        "--name",
        help="Name for the file in Drive (defaults to filename)",
    )
    parser.add_argument(
        "--parent-id",
        help="Parent folder ID (defaults to root)",
    )
    parser.add_argument(
        "--mime-type",
        help="MIME type of the file (auto-detected if not provided)",
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

        result = service.upload_file(
            file_path=args.file_path,
            name=args.name,
            parent_id=args.parent_id,
            mime_type=args.mime_type,
        )

        print(json.dumps(result, indent=2, default=str))

    except FileNotFoundError as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
