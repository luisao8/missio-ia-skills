#!/usr/bin/env python3
"""CLI script to export a Google Doc to various formats.

Usage:
    python export_doc.py --doc-id "1abc123xyz" --format pdf
    python export_doc.py --doc-id "1abc123xyz" --format docx --output-path ./report.docx
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from docs_service import DocsService, DocsServiceError, output_json, output_error


SUPPORTED_FORMATS = ["pdf", "docx", "txt", "html"]


def main():
    parser = argparse.ArgumentParser(
        description="Export a Google Doc to PDF, DOCX, TXT, or HTML format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Export to PDF (uses document title as filename)
    python export_doc.py --doc-id "1abc123xyz" --format pdf

    # Export to DOCX with custom output path
    python export_doc.py --doc-id "1abc123xyz" --format docx --output-path ./report.docx

    # Export to plain text
    python export_doc.py --doc-id "1abc123xyz" --format txt

Supported formats: pdf, docx, txt, html
        """
    )

    parser.add_argument(
        "--doc-id",
        required=True,
        help="ID of the document to export"
    )
    parser.add_argument(
        "--format",
        required=True,
        choices=SUPPORTED_FORMATS,
        help=f"Export format: {', '.join(SUPPORTED_FORMATS)}"
    )
    parser.add_argument(
        "--output-path",
        default=None,
        help="Output file path (optional, uses document title if not provided)"
    )
    parser.add_argument(
        "--credentials-path",
        default=None,
        help="Path to credentials directory (optional, uses default if not provided)"
    )

    args = parser.parse_args()

    try:
        service = DocsService(credentials_path=args.credentials_path)
        result = service.export_document(
            doc_id=args.doc_id,
            format=args.format,
            output_path=args.output_path
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
