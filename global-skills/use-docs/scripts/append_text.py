#!/usr/bin/env python3
"""CLI script to append text to the end of a Google Doc.

Usage:
    python append_text.py --doc-id "1abc123xyz" --text "Text to append"
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from docs_service import DocsService, DocsServiceError, output_json, output_error


def main():
    parser = argparse.ArgumentParser(
        description="Append text to the end of a Google Doc",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python append_text.py --doc-id "1abc123xyz" --text "New paragraph at the end"
    python append_text.py --doc-id "1abc123xyz" --text "\\n\\nNew section"
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
        help="Text to append to the end of the document"
    )
    parser.add_argument(
        "--credentials-path",
        default=None,
        help="Path to credentials directory (optional, uses default if not provided)"
    )

    args = parser.parse_args()

    try:
        service = DocsService(credentials_path=args.credentials_path)
        result = service.append_text(
            doc_id=args.doc_id,
            text=args.text
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
