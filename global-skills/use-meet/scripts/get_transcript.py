#!/usr/bin/env python3
"""
CLI script to get transcript from a Google Meet recording.
"""

import argparse
import json
import sys

from service import MeetService


def format_readable(result: dict) -> str:
    """Format transcript entries in a human-readable format."""
    if 'error' in result:
        return f"Error: {result['error']}"

    lines = []
    lines.append("=" * 60)
    lines.append("MEETING TRANSCRIPT")
    lines.append("=" * 60)
    lines.append(f"Transcript: {result.get('transcriptName', 'N/A')}")
    lines.append(f"Start: {result.get('startTime', 'N/A')}")
    lines.append(f"End: {result.get('endTime', 'N/A')}")
    lines.append("-" * 60)
    lines.append("")

    entries = result.get('entries', [])
    for entry in entries:
        start_time = entry.get('startTime', '')
        # Extract just the time portion if ISO format
        if 'T' in start_time:
            time_part = start_time.split('T')[1][:8]
        else:
            time_part = start_time[:8] if start_time else 'N/A'

        participant = entry.get('participant', 'Unknown')
        # Extract participant ID from full path
        if '/' in participant:
            participant = participant.split('/')[-1]

        text = entry.get('text', '')

        lines.append(f"[{time_part}] {participant}:")
        lines.append(f"  {text}")
        lines.append("")

    lines.append("=" * 60)
    lines.append(f"Total entries: {len(entries)}")
    lines.append("=" * 60)

    return '\n'.join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Get transcript from a Google Meet recording'
    )
    parser.add_argument(
        '--recording-name',
        type=str,
        required=True,
        help='The recording identifier (e.g., "conferenceRecords/{id}/recordings/{id}")'
    )
    parser.add_argument(
        '--format',
        type=str,
        choices=['json', 'readable'],
        default='json',
        help='Output format: json (default) or readable'
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
        result = service.get_transcript(args.recording_name)

        if args.format == 'readable':
            print(format_readable(result))
        else:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        if 'error' in result:
            sys.exit(1)

    except Exception as e:
        print(json.dumps({'error': str(e)}))
        sys.exit(1)


if __name__ == '__main__':
    main()
