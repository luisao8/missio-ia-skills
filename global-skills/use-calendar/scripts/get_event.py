#!/usr/bin/env python3
"""
CLI script to get details of a specific Google Calendar event.

Usage:
    python get_event.py --event-id "abc123xyz"
"""

import argparse
import json
import sys

from .calendar_service import CalendarService


def main():
    parser = argparse.ArgumentParser(
        description="Get details of a specific Google Calendar event",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python get_event.py --event-id "abc123xyz"
        """,
    )

    parser.add_argument(
        "--event-id",
        required=True,
        help="Event ID (obtained from search or list operations)",
    )

    args = parser.parse_args()

    try:
        # Initialize service
        service = CalendarService()

        # Get event
        event = service.get_event(args.event_id)

        # Output JSON
        print(json.dumps(event.to_dict(), indent=2, ensure_ascii=False))

    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
