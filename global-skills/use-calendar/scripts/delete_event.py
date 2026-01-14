#!/usr/bin/env python3
"""
CLI script to delete a Google Calendar event.

Usage:
    python delete_event.py --event-id "abc123xyz"
"""

import argparse
import json
import sys

from .calendar_service import CalendarService


def main():
    parser = argparse.ArgumentParser(
        description="Delete a Google Calendar event",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python delete_event.py --event-id "abc123xyz"
        """,
    )

    parser.add_argument(
        "--event-id",
        required=True,
        help="Event ID to delete (required)",
    )

    args = parser.parse_args()

    try:
        # Initialize service
        service = CalendarService()

        # Delete event
        result = service.delete_event(args.event_id)

        # Output JSON
        print(json.dumps(result, indent=2, ensure_ascii=False))

    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
