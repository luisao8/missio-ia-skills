#!/usr/bin/env python3
"""
CLI script to get information about a Google Meet space.
"""

import argparse
import json
import sys

from service import MeetService


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Get information about a Google Meet space'
    )
    parser.add_argument(
        '--space-name',
        type=str,
        required=True,
        help='The space identifier (e.g., "spaces/abc123")'
    )
    parser.add_argument(
        '--creds-file',
        type=str,
        default=None,
        help='Path to OAuth credentials JSON file (optional)'
    )
    parser.add_argument(
        '--token-file',
        type=str,
        default=None,
        help='Path to token pickle file (optional)'
    )

    args = parser.parse_args()

    try:
        service = MeetService(
            creds_file_path=args.creds_file,
            token_path=args.token_file
        )
        result = service.get_space(args.space_name)
        print(json.dumps(result, indent=2, ensure_ascii=False))

        if 'error' in result:
            sys.exit(1)

    except Exception as e:
        print(json.dumps({'error': str(e)}))
        sys.exit(1)


if __name__ == '__main__':
    main()
