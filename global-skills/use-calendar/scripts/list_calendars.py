#!/usr/bin/env python3
"""
CLI script to list all available Google Calendars.

Usage:
    python list_calendars.py
"""

import argparse
import json
import sys

from .calendar_service import CalendarService


def main():
    parser = argparse.ArgumentParser(
        description="List all available Google Calendars",
    )

    # No required arguments, just parse for --help
    parser.parse_args()

    try:
        # Initialize service
        service = CalendarService()

        # List calendars
        calendars = service.list_calendars()

        # Output JSON
        print(json.dumps(calendars, indent=2, ensure_ascii=False))

    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
