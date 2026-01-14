"""
Pydantic models for Google Calendar data.

Provides validated data structures for calendar events and time slots.
"""

from typing import Optional

from pydantic import BaseModel, Field


class CalendarEvent(BaseModel):
    """Represents a Google Calendar event."""

    id: str = Field(description="Unique event identifier")
    summary: str = Field(description="Event title/summary")
    start: Optional[str] = Field(default=None, description="Start datetime in ISO format")
    end: Optional[str] = Field(default=None, description="End datetime in ISO format")
    description: Optional[str] = Field(default=None, description="Event description")
    location: Optional[str] = Field(default=None, description="Event location")
    attendees: Optional[list[str]] = Field(default=None, description="List of attendee emails")
    meet_link: Optional[str] = Field(default=None, description="Google Meet link if present")
    html_link: Optional[str] = Field(default=None, description="Link to view event in Google Calendar")

    def to_dict(self) -> dict:
        """Convert to dictionary, excluding None values."""
        return {k: v for k, v in self.model_dump().items() if v is not None}


class TimeSlot(BaseModel):
    """Represents a free time slot in the calendar."""

    start: str = Field(description="Start datetime in ISO format")
    end: str = Field(description="End datetime in ISO format")
    duration_minutes: int = Field(description="Duration of the slot in minutes")

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return self.model_dump()
