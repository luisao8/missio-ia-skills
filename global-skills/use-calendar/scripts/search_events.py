#!/usr/bin/env python3
"""
CLI script to search for Google Calendar events.

Usage:
    python search_events.py --query "meeting" --start-date "2024-01-15" --end-date "2024-01-20"
    python search_events.py --start-date "today" --end-date "tomorrow"
"""

import argparse
import json
import sys

from .calendar_service import CalendarService


def main():
    parser = argparse.ArgumentParser(
        description="Search for Google Calendar events",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python search_events.py --query "team" --start-date "2024-01-01" --end-date "2024-01-31"
    python search_events.py --start-date "today" --end-date "tomorrow"
    python search_events.py --query "standup"
        """,
    )

    parser.add_argument(
        "--query",
        help="Search query for event title/description",
    )
    parser.add_argument(
        "--start-date",
        help="Start date: YYYY-MM-DD, 'today', 'tomorrow', or 'yesterday' (default: today)",
    )
    parser.add_argument(
        "--end-date",
        help="End date: YYYY-MM-DD, 'today', 'tomorrow', or 'yesterday'",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=100,
        help="Maximum number of events to return (default: 100)",
    )

    args = parser.parse_args()

    try:
        # Initialize service
        service = CalendarService()

        # Get events
        events = service.get_events(
            start_date=args.start_date,
            end_date=args.end_date,
            query=args.query,
            max_results=args.max_results,
        )

        # Convert to list of dicts
        events_list = [event.to_dict() for event in events]

        # Output JSON
        print(json.dumps(events_list, indent=2, ensure_ascii=False))

    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
