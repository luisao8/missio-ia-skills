#!/usr/bin/env python3
"""
CLI script to create a new Google Calendar event.

Usage:
    python create_event.py --title "Meeting" --date "2024-01-20" --time "10:00" --duration 60
    python create_event.py --title "Call" --date "tomorrow" --time "14:00" --add-meet
"""

import argparse
import json
import sys
from datetime import datetime, timedelta

import pytz

from .calendar_service import CalendarService, DEFAULT_TIMEZONE


def parse_date(date_str: str, tz) -> datetime:
    """Parse a date string into a datetime object."""
    date_str = date_str.strip().lower()
    now = datetime.now(tz)

    if date_str == "today":
        return now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif date_str == "tomorrow":
        return (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    elif date_str == "yesterday":
        return (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        # Parse as date
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return tz.localize(dt)
        except ValueError:
            # Try ISO format
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = tz.localize(dt)
            return dt


def main():
    parser = argparse.ArgumentParser(
        description="Create a new Google Calendar event",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python create_event.py --title "Team Meeting" --date "2024-01-20" --time "10:00" --duration 60
    python create_event.py --title "Quick Call" --date "tomorrow" --time "14:30" --add-meet
    python create_event.py --title "Lunch" --date "today" --time "13:00" --duration 60 --location "Restaurant"
        """,
    )

    parser.add_argument("--title", required=True, help="Event title (required)")
    parser.add_argument(
        "--date",
        required=True,
        help="Event date: YYYY-MM-DD, 'today', 'tomorrow', or 'yesterday'",
    )
    parser.add_argument("--time", required=True, help="Start time in HH:MM format")
    parser.add_argument(
        "--duration",
        type=int,
        default=60,
        help="Duration in minutes (default: 60)",
    )
    parser.add_argument("--description", help="Event description")
    parser.add_argument("--location", help="Event location")
    parser.add_argument(
        "--attendees",
        help="Comma-separated list of attendee email addresses",
    )
    parser.add_argument(
        "--add-meet",
        action="store_true",
        help="Add Google Meet link to the event",
    )

    args = parser.parse_args()

    try:
        # Initialize service
        service = CalendarService()
        tz = service.timezone

        # Parse date and time
        event_date = parse_date(args.date, tz)
        time_parts = args.time.split(":")
        hour = int(time_parts[0])
        minute = int(time_parts[1]) if len(time_parts) > 1 else 0

        start = event_date.replace(hour=hour, minute=minute)
        end = start + timedelta(minutes=args.duration)

        # Parse attendees
        attendees = None
        if args.attendees:
            attendees = [email.strip() for email in args.attendees.split(",")]

        # Create event
        event = service.create_event(
            title=args.title,
            start=start,
            end=end,
            description=args.description,
            location=args.location,
            attendees=attendees,
            add_meet=args.add_meet,
        )

        # Output JSON
        print(json.dumps(event.to_dict(), indent=2, ensure_ascii=False))

    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
