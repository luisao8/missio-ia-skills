#!/usr/bin/env python3
"""
CLI script to get all Google Calendar events for today.

Usage:
    python get_today.py
"""

import argparse
import json
import sys

from .calendar_service import CalendarService


def main():
    parser = argparse.ArgumentParser(
        description="Get all Google Calendar events for today",
    )

    # No required arguments, just parse for --help
    parser.parse_args()

    try:
        # Initialize service
        service = CalendarService()

        # Get today's events
        events = service.get_today_events()

        # Convert to list of dicts
        events_list = [event.to_dict() for event in events]

        # Output JSON
        print(json.dumps(events_list, indent=2, ensure_ascii=False))

    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
