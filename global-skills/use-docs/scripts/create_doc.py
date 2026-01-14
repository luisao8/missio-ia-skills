#!/usr/bin/env python3
"""CLI script to create a new Google Doc.

Usage:
    python create_doc.py --title "My Document"
    python create_doc.py --title "My Document" --content "Initial content"
    python create_doc.py --title "My Document" --folder-id "abc123"
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from docs_service import DocsService, DocsServiceError, output_json, output_error


def main():
    parser = argparse.ArgumentParser(
        description="Create a new Google Doc",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python create_doc.py --title "Meeting Notes"
    python create_doc.py --title "Report" --content "# Quarterly Report"
    python create_doc.py --title "Project Doc" --folder-id "1abc123xyz"
        """
    )

    parser.add_argument(
        "--title",
        required=True,
        help="Title of the document"
    )
    parser.add_argument(
        "--content",
        default=None,
        help="Initial text content (optional)"
    )
    parser.add_argument(
        "--folder-id",
        default=None,
        help="Google Drive folder ID to create document in (optional)"
    )
    parser.add_argument(
        "--credentials-path",
        default=None,
        help="Path to credentials directory (optional, uses default if not provided)"
    )

    args = parser.parse_args()

    try:
        service = DocsService(credentials_path=args.credentials_path)
        result = service.create_document(
            title=args.title,
            content=args.content,
            folder_id=args.folder_id
        )
        output_json(result)

    except DocsServiceError as e:
        output_error(str(e))
        sys.exit(1)
    except Exception as e:
        output_error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
