#!/usr/bin/env python3
"""CLI script to update a Google Doc (replaces all content).

Usage:
    python update_doc.py --doc-id "1abc123xyz" --content "New content"
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from docs_service import DocsService, DocsServiceError, output_json, output_error


def main():
    parser = argparse.ArgumentParser(
        description="Update a Google Doc (replaces all content)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python update_doc.py --doc-id "1abc123xyz" --content "New document content"

WARNING: This replaces ALL existing content in the document.
Use append_text.py or insert_text.py to add content without replacing.
        """
    )

    parser.add_argument(
        "--doc-id",
        required=True,
        help="ID of the document to update"
    )
    parser.add_argument(
        "--content",
        required=True,
        help="New content to replace existing content"
    )
    parser.add_argument(
        "--credentials-path",
        default=None,
        help="Path to credentials directory (optional, uses default if not provided)"
    )

    args = parser.parse_args()

    try:
        service = DocsService(credentials_path=args.credentials_path)
        result = service.update_document(
            doc_id=args.doc_id,
            content=args.content
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
