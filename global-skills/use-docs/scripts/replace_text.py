#!/usr/bin/env python3
"""CLI script to find and replace text in a Google Doc.

Usage:
    python replace_text.py --doc-id "1abc123xyz" --find "old" --replace "new"
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from docs_service import DocsService, DocsServiceError, output_json, output_error


def main():
    parser = argparse.ArgumentParser(
        description="Find and replace text in a Google Doc",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Replace all occurrences (case-insensitive by default)
    python replace_text.py --doc-id "1abc123xyz" --find "TODO" --replace "DONE"

    # Case-sensitive replacement
    python replace_text.py --doc-id "1abc123xyz" --find "Name" --replace "Title" --match-case

Note: This replaces ALL occurrences of the text in the document.
        """
    )

    parser.add_argument(
        "--doc-id",
        required=True,
        help="ID of the document"
    )
    parser.add_argument(
        "--find",
        required=True,
        help="Text to find"
    )
    parser.add_argument(
        "--replace",
        required=True,
        help="Text to replace with"
    )
    parser.add_argument(
        "--match-case",
        action="store_true",
        default=False,
        help="Match case when searching (default: case-insensitive)"
    )
    parser.add_argument(
        "--credentials-path",
        default=None,
        help="Path to credentials directory (optional, uses default if not provided)"
    )

    args = parser.parse_args()

    try:
        service = DocsService(credentials_path=args.credentials_path)
        result = service.replace_text(
            doc_id=args.doc_id,
            find=args.find,
            replace=args.replace,
            match_case=args.match_case
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
