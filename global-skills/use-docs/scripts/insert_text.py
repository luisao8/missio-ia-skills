#!/usr/bin/env python3
"""CLI script to insert text at a specific position in a Google Doc.

Usage:
    python insert_text.py --doc-id "1abc123xyz" --text "Inserted text" --index 1
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from docs_service import DocsService, DocsServiceError, output_json, output_error


def main():
    parser = argparse.ArgumentParser(
        description="Insert text at a specific position in a Google Doc",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Insert at the beginning of the document (index 1)
    python insert_text.py --doc-id "1abc123xyz" --text "Title: " --index 1

    # Insert at a specific position
    python insert_text.py --doc-id "1abc123xyz" --text "[INSERTED]" --index 50

Note: Index 1 is the start of the document. Use read_doc.py to see
current content and determine insertion points.
        """
    )

    parser.add_argument(
        "--doc-id",
        required=True,
        help="ID of the document"
    )
    parser.add_argument(
        "--text",
        required=True,
        help="Text to insert"
    )
    parser.add_argument(
        "--index",
        type=int,
        required=True,
        help="Character index where to insert (1 = start of document)"
    )
    parser.add_argument(
        "--credentials-path",
        default=None,
        help="Path to credentials directory (optional, uses default if not provided)"
    )

    args = parser.parse_args()

    if args.index < 1:
        output_error("Index must be >= 1 (1 is the start of the document)")
        sys.exit(1)

    try:
        service = DocsService(credentials_path=args.credentials_path)
        result = service.insert_text(
            doc_id=args.doc_id,
            text=args.text,
            index=args.index
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
