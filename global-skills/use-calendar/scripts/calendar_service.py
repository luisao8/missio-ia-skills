"""
Google Calendar Service.

Main class for interacting with Google Calendar API.
Handles OAuth authentication and provides methods for all calendar operations.
"""

import os
import pickle
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import pytz
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .models import CalendarEvent, TimeSlot

# OAuth 2.0 scopes for Google Calendar
SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
]

# Default paths relative to this file
DEFAULT_CREDENTIALS_DIR = Path(__file__).parent.parent.parent.parent.parent / "MCP_servers" / "google-credentials"
DEFAULT_TIMEZONE = "Europe/Madrid"


class CalendarService:
    """Google Calendar Service for managing calendar events."""

    def __init__(
        self,
        credentials_path: Optional[str] = None,
        token_path: Optional[str] = None,
        timezone: Optional[str] = None,
        calendar_id: str = "primary",
    ):
        """
        Initialize Calendar Service.

        Args:
            credentials_path: Path to OAuth client credentials JSON file.
                             Defaults to MCP_servers/google-credentials/credentials.json
            token_path: Path to store/load the user token pickle file.
                       Defaults to MCP_servers/google-credentials/calendar_token.pickle
            timezone: Timezone for date operations. Defaults to Europe/Madrid.
            calendar_id: Calendar ID to use. Defaults to "primary".
        """
        # Set up credentials paths
        creds_dir = Path(os.environ.get("GOOGLE_CREDENTIALS_PATH", str(DEFAULT_CREDENTIALS_DIR)))
        if credentials_path:
            self.credentials_path = Path(credentials_path)
        else:
            self.credentials_path = creds_dir / "credentials.json"

        if token_path:
            self.token_path = Path(token_path)
        else:
            self.token_path = creds_dir / "calendar_token.pickle"

        # Set timezone
        self.timezone = pytz.timezone(timezone or os.environ.get("CALENDAR_TIMEZONE", DEFAULT_TIMEZONE))
        self.calendar_id = calendar_id

        # Initialize service lazily
        self._service = None

    @property
    def service(self):
        """Get or create the Google Calendar API service."""
        if self._service is None:
            self._service = self._authenticate()
        return self._service

    def _authenticate(self):
        """Authenticate with Google Calendar API and return service."""
        creds = None

        # Load existing token
        if self.token_path.exists():
            with open(self.token_path, "rb") as token:
                creds = pickle.load(token)

        # Refresh or create new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not self.credentials_path.exists():
                    raise FileNotFoundError(
                        f"Credentials file not found: {self.credentials_path}. "
                        "Please ensure OAuth client credentials are set up."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.credentials_path), SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save the credentials for next time
            with open(self.token_path, "wb") as token:
                pickle.dump(creds, token)

        return build("calendar", "v3", credentials=creds)

    def _parse_date(self, date_str: str) -> datetime:
        """
        Parse a date string into a datetime object.

        Accepts: ISO format, "today", "tomorrow", "yesterday"
        """
        date_str = date_str.strip().lower()
        now = datetime.now(self.timezone)

        if date_str == "today":
            return now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif date_str == "tomorrow":
            return (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        elif date_str == "yesterday":
            return (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            # Try parsing as ISO format
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = self.timezone.localize(dt)
            return dt

    def _event_to_model(self, event: dict) -> CalendarEvent:
        """Convert Google Calendar API event to CalendarEvent model."""
        # Extract start/end times
        start = event.get("start", {})
        end = event.get("end", {})

        start_dt = start.get("dateTime") or start.get("date")
        end_dt = end.get("dateTime") or end.get("date")

        # Extract attendees
        attendees = []
        for att in event.get("attendees", []):
            attendees.append(att.get("email", ""))

        # Extract meet link
        meet_link = None
        conference_data = event.get("conferenceData", {})
        for entry_point in conference_data.get("entryPoints", []):
            if entry_point.get("entryPointType") == "video":
                meet_link = entry_point.get("uri")
                break

        return CalendarEvent(
            id=event.get("id", ""),
            summary=event.get("summary", ""),
            start=start_dt,
            end=end_dt,
            description=event.get("description"),
            location=event.get("location"),
            attendees=attendees if attendees else None,
            meet_link=meet_link,
            html_link=event.get("htmlLink"),
        )

    def get_today_events(self) -> list[CalendarEvent]:
        """Get all events for today."""
        now = datetime.now(self.timezone)
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)

        return self.get_events(
            start_date=start_of_day.isoformat(),
            end_date=end_of_day.isoformat(),
        )

    def get_events(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        query: Optional[str] = None,
        max_results: int = 100,
    ) -> list[CalendarEvent]:
        """
        Get calendar events within a date range.

        Args:
            start_date: Start date (ISO format or "today"/"tomorrow"/"yesterday")
            end_date: End date
            query: Search query for event summary/description
            max_results: Maximum number of events to return

        Returns:
            List of CalendarEvent objects
        """
        now = datetime.now(self.timezone)

        # Default to today if no dates provided
        if start_date:
            time_min = self._parse_date(start_date)
        else:
            time_min = now.replace(hour=0, minute=0, second=0, microsecond=0)

        if end_date:
            time_max = self._parse_date(end_date)
            # Ensure end date includes the full day
            if time_max.hour == 0 and time_max.minute == 0:
                time_max = time_max.replace(hour=23, minute=59, second=59)
        else:
            time_max = time_min.replace(hour=23, minute=59, second=59)

        try:
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=time_min.isoformat(),
                timeMax=time_max.isoformat(),
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
                q=query,
            ).execute()

            events = events_result.get("items", [])
            return [self._event_to_model(e) for e in events]

        except HttpError as e:
            raise RuntimeError(f"Failed to get events: {e}")

    def get_event(self, event_id: str) -> CalendarEvent:
        """
        Get a specific event by ID.

        Args:
            event_id: The event ID

        Returns:
            CalendarEvent object
        """
        try:
            event = self.service.events().get(
                calendarId=self.calendar_id,
                eventId=event_id,
            ).execute()
            return self._event_to_model(event)

        except HttpError as e:
            raise RuntimeError(f"Failed to get event: {e}")

    def create_event(
        self,
        title: str,
        start: datetime,
        end: datetime,
        description: Optional[str] = None,
        location: Optional[str] = None,
        attendees: Optional[list[str]] = None,
        add_meet: bool = False,
    ) -> CalendarEvent:
        """
        Create a new calendar event.

        Args:
            title: Event title/summary
            start: Start datetime
            end: End datetime
            description: Event description
            location: Event location
            attendees: List of attendee email addresses
            add_meet: Whether to add a Google Meet link

        Returns:
            Created CalendarEvent object
        """
        event_body = {
            "summary": title,
            "start": {
                "dateTime": start.isoformat(),
                "timeZone": str(self.timezone),
            },
            "end": {
                "dateTime": end.isoformat(),
                "timeZone": str(self.timezone),
            },
        }

        if description:
            event_body["description"] = description

        if location:
            event_body["location"] = location

        if attendees:
            event_body["attendees"] = [{"email": email} for email in attendees]

        if add_meet:
            event_body["conferenceData"] = {
                "createRequest": {
                    "requestId": f"meet-{datetime.now().timestamp()}",
                    "conferenceSolutionKey": {"type": "hangoutsMeet"},
                }
            }

        try:
            conference_version = 1 if add_meet else 0
            event = self.service.events().insert(
                calendarId=self.calendar_id,
                body=event_body,
                conferenceDataVersion=conference_version,
            ).execute()
            return self._event_to_model(event)

        except HttpError as e:
            raise RuntimeError(f"Failed to create event: {e}")

    def update_event(
        self,
        event_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        location: Optional[str] = None,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        attendees: Optional[list[str]] = None,
    ) -> CalendarEvent:
        """
        Update an existing calendar event.

        Args:
            event_id: The event ID to update
            title: New title (optional)
            description: New description (optional)
            location: New location (optional)
            start: New start datetime (optional)
            end: New end datetime (optional)
            attendees: New list of attendee emails (optional)

        Returns:
            Updated CalendarEvent object
        """
        try:
            # Get existing event
            event = self.service.events().get(
                calendarId=self.calendar_id,
                eventId=event_id,
            ).execute()

            # Update fields if provided
            if title is not None:
                event["summary"] = title

            if description is not None:
                event["description"] = description

            if location is not None:
                event["location"] = location

            if start is not None:
                event["start"] = {
                    "dateTime": start.isoformat(),
                    "timeZone": str(self.timezone),
                }

            if end is not None:
                event["end"] = {
                    "dateTime": end.isoformat(),
                    "timeZone": str(self.timezone),
                }

            if attendees is not None:
                event["attendees"] = [{"email": email} for email in attendees]

            updated_event = self.service.events().update(
                calendarId=self.calendar_id,
                eventId=event_id,
                body=event,
            ).execute()

            return self._event_to_model(updated_event)

        except HttpError as e:
            raise RuntimeError(f"Failed to update event: {e}")

    def delete_event(self, event_id: str) -> dict:
        """
        Delete a calendar event.

        Args:
            event_id: The event ID to delete

        Returns:
            Dict with status of deletion
        """
        try:
            self.service.events().delete(
                calendarId=self.calendar_id,
                eventId=event_id,
            ).execute()
            return {"status": "deleted", "event_id": event_id}

        except HttpError as e:
            raise RuntimeError(f"Failed to delete event: {e}")

    def find_free_slots(
        self,
        duration_minutes: int = 30,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        work_hours_start: int = 9,
        work_hours_end: int = 18,
    ) -> list[TimeSlot]:
        """
        Find free time slots in the calendar.

        Args:
            duration_minutes: Minimum duration of free slot
            start_date: Start date for search
            end_date: End date for search
            work_hours_start: Start of work day (hour)
            work_hours_end: End of work day (hour)

        Returns:
            List of TimeSlot objects representing free time
        """
        now = datetime.now(self.timezone)

        if start_date:
            search_start = self._parse_date(start_date)
        else:
            search_start = now

        if end_date:
            search_end = self._parse_date(end_date)
            if search_end.hour == 0 and search_end.minute == 0:
                search_end = search_end.replace(hour=23, minute=59, second=59)
        else:
            search_end = (search_start + timedelta(days=7)).replace(hour=23, minute=59, second=59)

        # Get all events in the range
        events = self.get_events(
            start_date=search_start.isoformat(),
            end_date=search_end.isoformat(),
        )

        # Build list of busy times
        busy_times = []
        for event in events:
            if event.start and event.end:
                event_start = datetime.fromisoformat(event.start.replace("Z", "+00:00"))
                event_end = datetime.fromisoformat(event.end.replace("Z", "+00:00"))
                busy_times.append((event_start, event_end))

        # Sort by start time
        busy_times.sort(key=lambda x: x[0])

        # Find free slots
        free_slots = []
        current_date = search_start.date()
        end_date_obj = search_end.date()

        while current_date <= end_date_obj:
            # Work hours for this day
            day_start = self.timezone.localize(
                datetime.combine(current_date, datetime.min.time().replace(hour=work_hours_start))
            )
            day_end = self.timezone.localize(
                datetime.combine(current_date, datetime.min.time().replace(hour=work_hours_end))
            )

            # Skip if day_start is in the past
            if day_end < now:
                current_date += timedelta(days=1)
                continue

            # Start from now if today
            if current_date == now.date() and day_start < now:
                day_start = now

            # Find gaps in busy times for this day
            current_time = day_start
            for busy_start, busy_end in busy_times:
                if busy_start.date() != current_date:
                    continue

                if busy_start > current_time:
                    # There's a gap
                    gap_duration = (busy_start - current_time).total_seconds() / 60
                    if gap_duration >= duration_minutes:
                        free_slots.append(TimeSlot(
                            start=current_time.isoformat(),
                            end=busy_start.isoformat(),
                            duration_minutes=int(gap_duration),
                        ))

                current_time = max(current_time, busy_end)

            # Check for gap at end of day
            if current_time < day_end:
                gap_duration = (day_end - current_time).total_seconds() / 60
                if gap_duration >= duration_minutes:
                    free_slots.append(TimeSlot(
                        start=current_time.isoformat(),
                        end=day_end.isoformat(),
                        duration_minutes=int(gap_duration),
                    ))

            current_date += timedelta(days=1)

        return free_slots

    def list_calendars(self) -> list[dict]:
        """
        List all calendars available to the user.

        Returns:
            List of dicts with calendar id and name
        """
        try:
            calendar_list = self.service.calendarList().list().execute()
            calendars = calendar_list.get("items", [])

            return [
                {
                    "id": cal.get("id"),
                    "name": cal.get("summary"),
                    "primary": cal.get("primary", False),
                }
                for cal in calendars
            ]

        except HttpError as e:
            raise RuntimeError(f"Failed to list calendars: {e}")
