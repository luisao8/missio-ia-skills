#!/usr/bin/env python3
"""
CLI script to update an existing Google Calendar event.

Usage:
    python update_event.py --event-id "abc123xyz" --title "New Title"
    python update_event.py --event-id "abc123xyz" --description "Updated description" --location "New Office"
"""

import argparse
import json
import sys
from datetime import datetime

from .calendar_service import CalendarService


def parse_datetime(dt_str: str, tz) -> datetime:
    """Parse a datetime string."""
    dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = tz.localize(dt)
    return dt


def main():
    parser = argparse.ArgumentParser(
        description="Update an existing Google Calendar event",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python update_event.py --event-id "abc123xyz" --title "New Meeting Title"
    python update_event.py --event-id "abc123xyz" --description "Updated description"
    python update_event.py --event-id "abc123xyz" --start "2024-01-20T15:00:00" --end "2024-01-20T16:00:00"
    python update_event.py --event-id "abc123xyz" --attendees "user1@example.com,user2@example.com"
        """,
    )

    parser.add_argument(
        "--event-id",
        required=True,
        help="Event ID to update (required)",
    )
    parser.add_argument(
        "--title",
        help="New event title",
    )
    parser.add_argument(
        "--description",
        help="New event description",
    )
    parser.add_argument(
        "--location",
        help="New event location",
    )
    parser.add_argument(
        "--start",
        help="New start datetime in ISO format (e.g., 2024-01-20T10:00:00)",
    )
    parser.add_argument(
        "--end",
        help="New end datetime in ISO format (e.g., 2024-01-20T11:00:00)",
    )
    parser.add_argument(
        "--attendees",
        help="Comma-separated list of attendee email addresses (replaces existing)",
    )

    args = parser.parse_args()

    try:
        # Initialize service
        service = CalendarService()
        tz = service.timezone

        # Parse datetime arguments if provided
        start = None
        end = None
        if args.start:
            start = parse_datetime(args.start, tz)
        if args.end:
            end = parse_datetime(args.end, tz)

        # Parse attendees if provided
        attendees = None
        if args.attendees:
            attendees = [email.strip() for email in args.attendees.split(",")]

        # Update event
        event = service.update_event(
            event_id=args.event_id,
            title=args.title,
            description=args.description,
            location=args.location,
            start=start,
            end=end,
            attendees=attendees,
        )

        # Output JSON
        print(json.dumps(event.to_dict(), indent=2, ensure_ascii=False))

    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
