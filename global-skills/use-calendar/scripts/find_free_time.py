#!/usr/bin/env python3
"""
CLI script to find free time slots in the Google Calendar.

Usage:
    python find_free_time.py --duration 30 --start-date "today" --end-date "tomorrow"
"""

import argparse
import json
import sys

from .calendar_service import CalendarService


def main():
    parser = argparse.ArgumentParser(
        description="Find free time slots in Google Calendar",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python find_free_time.py --duration 30
    python find_free_time.py --duration 60 --start-date "today" --end-date "tomorrow"
    python find_free_time.py --duration 120 --start-date "2024-01-15" --end-date "2024-01-20"
        """,
    )

    parser.add_argument(
        "--duration",
        type=int,
        default=30,
        help="Minimum duration of free slot in minutes (default: 30)",
    )
    parser.add_argument(
        "--start-date",
        help="Start date for search: YYYY-MM-DD, 'today', 'tomorrow' (default: now)",
    )
    parser.add_argument(
        "--end-date",
        help="End date for search: YYYY-MM-DD, 'today', 'tomorrow' (default: 7 days from now)",
    )
    parser.add_argument(
        "--work-hours-start",
        type=int,
        default=9,
        help="Start of work day (hour, 0-23, default: 9)",
    )
    parser.add_argument(
        "--work-hours-end",
        type=int,
        default=18,
        help="End of work day (hour, 0-23, default: 18)",
    )

    args = parser.parse_args()

    try:
        # Initialize service
        service = CalendarService()

        # Find free slots
        slots = service.find_free_slots(
            duration_minutes=args.duration,
            start_date=args.start_date,
            end_date=args.end_date,
            work_hours_start=args.work_hours_start,
            work_hours_end=args.work_hours_end,
        )

        # Convert to list of dicts
        slots_list = [slot.to_dict() for slot in slots]

        # Output JSON
        print(json.dumps(slots_list, indent=2, ensure_ascii=False))

    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
