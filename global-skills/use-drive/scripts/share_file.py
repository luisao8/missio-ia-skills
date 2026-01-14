#!/usr/bin/env python3
"""
CLI script to share a file in Google Drive.

Usage:
    python share_file.py --file-id FILE_ID --email user@example.com --role reader
    python share_file.py --file-id FILE_ID --role reader --type anyone
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
        description="Share a file in Google Drive",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Share with a specific user
  python share_file.py --file-id 1abc123xyz --email user@example.com --role reader
  python share_file.py --file-id 1abc123xyz --email user@example.com --role writer

  # Share with anyone (public link)
  python share_file.py --file-id 1abc123xyz --role reader --type anyone

Roles:
  reader    - Can view
  writer    - Can edit
  commenter - Can comment
  owner     - Full ownership (use with caution)

Types:
  user    - Share with specific email (default)
  group   - Share with Google Group
  domain  - Share with domain
  anyone  - Public link
        """,
    )
    parser.add_argument(
        "--file-id",
        required=True,
        help="ID of the file to share",
    )
    parser.add_argument(
        "--email",
        help="Email address to share with (required for user/group type)",
    )
    parser.add_argument(
        "--role",
        required=True,
        choices=["reader", "writer", "commenter", "owner"],
        help="Permission role",
    )
    parser.add_argument(
        "--type",
        default="user",
        choices=["user", "group", "domain", "anyone"],
        help="Permission type (default: user)",
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

    # Validate: email required for user/group type
    if args.type in ["user", "group"] and not args.email:
        print(json.dumps({"error": f"--email is required for type '{args.type}'"}))
        sys.exit(1)

    try:
        service = get_drive_service(
            credentials_path=args.credentials_path,
            token_path=args.token_path,
        )

        result = service.share_file(
            file_id=args.file_id,
            email=args.email,
            role=args.role,
            share_type=args.type,
        )

        # Format output
        output = {
            "permission": result["permission"],
            "file_name": result["file"]["name"],
            "web_link": result["file"].get("webViewLink"),
        }

        print(json.dumps(output, indent=2, default=str))

    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
