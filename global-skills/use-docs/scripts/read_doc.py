#!/usr/bin/env python3
"""CLI script to read a Google Doc.

Usage:
    python read_doc.py --doc-id "1abc123xyz"
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from docs_service import DocsService, DocsServiceError, output_json, output_error


def main():
    parser = argparse.ArgumentParser(
        description="Read the content of a Google Doc",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python read_doc.py --doc-id "1abc123xyz789"

The document ID can be found in the Google Docs URL:
    https://docs.google.com/document/d/DOCUMENT_ID/edit
        """
    )

    parser.add_argument(
        "--doc-id",
        required=True,
        help="ID of the document to read"
    )
    parser.add_argument(
        "--credentials-path",
        default=None,
        help="Path to credentials directory (optional, uses default if not provided)"
    )

    args = parser.parse_args()

    try:
        service = DocsService(credentials_path=args.credentials_path)
        result = service.read_document(doc_id=args.doc_id)
        output_json(result)

    except DocsServiceError as e:
        output_error(str(e))
        sys.exit(1)
    except Exception as e:
        output_error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
