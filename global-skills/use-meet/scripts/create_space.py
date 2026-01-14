#!/usr/bin/env python3
"""
CLI script to create a new Google Meet space.
"""

import argparse
import json
import sys
from typing import Optional

from service import MeetService


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Create a new Google Meet space'
    )
    parser.add_argument(
        '--config',
        type=str,
        default=None,
        help='Space configuration as JSON string (optional)'
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

    # Parse config if provided
    config: Optional[dict] = None
    if args.config:
        try:
            config = json.loads(args.config)
        except json.JSONDecodeError as e:
            print(json.dumps({'error': f'Invalid config JSON: {e}'}))
            sys.exit(1)

    try:
        service = MeetService(
            creds_file_path=args.creds_file,
            token_path=args.token_file
        )
        result = service.create_space(config=config)
        print(json.dumps(result, indent=2, ensure_ascii=False))

        if 'error' in result:
            sys.exit(1)

    except Exception as e:
        print(json.dumps({'error': str(e)}))
        sys.exit(1)


if __name__ == '__main__':
    main()
