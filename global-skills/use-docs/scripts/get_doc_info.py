#!/usr/bin/env python3
"""CLI script to get metadata about a Google Doc.

Usage:
    python get_doc_info.py --doc-id "1abc123xyz"
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from docs_service import DocsService, DocsServiceError, output_json, output_error


def main():
    parser = argparse.ArgumentParser(
        description="Get metadata and information about a Google Doc",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python get_doc_info.py --doc-id "1abc123xyz789"

Returns information including:
    - Document title
    - Character count
    - Creation and modification timestamps
    - Web link
    - Document owners

The document ID can be found in the Google Docs URL:
    https://docs.google.com/document/d/DOCUMENT_ID/edit
        """
    )

    parser.add_argument(
        "--doc-id",
        required=True,
        help="ID of the document"
    )
    parser.add_argument(
        "--credentials-path",
        default=None,
        help="Path to credentials directory (optional, uses default if not provided)"
    )

    args = parser.parse_args()

    try:
        service = DocsService(credentials_path=args.credentials_path)
        result = service.get_document_info(doc_id=args.doc_id)
        output_json(result)

    except DocsServiceError as e:
        output_error(str(e))
        sys.exit(1)
    except Exception as e:
        output_error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
