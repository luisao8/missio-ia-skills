"""Pydantic models for Gmail Skill.

Provides data models for Email, Thread, Label, and Attachment.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class Attachment(BaseModel):
    """Model for email attachment."""

    id: Optional[str] = Field(None, description="Attachment ID")
    filename: str = Field(..., description="Attachment filename")
    mime_type: Optional[str] = Field(None, description="MIME type of the attachment")
    size: int = Field(0, description="Size in bytes")


class Label(BaseModel):
    """Model for Gmail label."""

    id: str = Field(..., description="Label ID")
    name: str = Field(..., description="Label name")
    type: str = Field("user", description="Label type: system or user")


class Email(BaseModel):
    """Model for email message."""

    id: str = Field(..., description="Message ID")
    thread_id: Optional[str] = Field(None, description="Thread ID")
    subject: str = Field("", description="Email subject")
    from_email: str = Field("", alias="from", description="Sender email address")
    to: str = Field("", description="Recipient email address(es)")
    cc: Optional[str] = Field(None, description="CC recipients")
    bcc: Optional[str] = Field(None, description="BCC recipients")
    body: Optional[str] = Field(None, description="Plain text body")
    html_body: Optional[str] = Field(None, description="HTML body")
    date: Optional[str] = Field(None, description="Email date")
    snippet: Optional[str] = Field(None, description="Email snippet/preview")
    labels: List[str] = Field(default_factory=list, description="Label IDs")
    attachments: List[Attachment] = Field(
        default_factory=list, description="List of attachments"
    )

    class Config:
        populate_by_name = True


class Thread(BaseModel):
    """Model for email thread."""

    id: str = Field(..., description="Thread ID")
    snippet: Optional[str] = Field(None, description="Thread snippet/preview")
    message_count: int = Field(0, description="Number of messages in thread")
    subject: Optional[str] = Field(None, description="Thread subject")
    from_email: Optional[str] = Field(None, alias="from", description="First sender")
    date: Optional[str] = Field(None, description="Date of first message")
    messages: List[Email] = Field(
        default_factory=list, description="Messages in thread"
    )

    class Config:
        populate_by_name = True


class SendEmailRequest(BaseModel):
    """Request model for sending email."""

    to: str = Field(..., description="Recipient email address(es), comma-separated")
    subject: str = Field(..., description="Email subject")
    body: str = Field(..., description="Email body")
    cc: Optional[str] = Field(None, description="CC recipients, comma-separated")
    bcc: Optional[str] = Field(None, description="BCC recipients, comma-separated")
    html: bool = Field(False, description="If True, body is treated as HTML")
    attachments: Optional[List[str]] = Field(
        None, description="List of file paths to attach"
    )


class SearchEmailsRequest(BaseModel):
    """Request model for searching emails."""

    query: str = Field("", description="Gmail search query")
    max_results: int = Field(10, description="Maximum number of results")
    label: Optional[str] = Field(None, description="Filter by label ID")


class DraftRequest(BaseModel):
    """Request model for creating a draft."""

    to: str = Field(..., description="Recipient email address(es)")
    subject: str = Field(..., description="Email subject")
    body: str = Field(..., description="Email body")
    html: bool = Field(False, description="If True, body is treated as HTML")


class ReplyRequest(BaseModel):
    """Request model for replying to an email."""

    message_id: str = Field(..., description="Message ID to reply to")
    body: str = Field(..., description="Reply body")
    html: bool = Field(False, description="If True, body is treated as HTML")


class AddLabelRequest(BaseModel):
    """Request model for adding a label."""

    message_id: str = Field(..., description="Message ID")
    label_id: str = Field(..., description="Label ID to add")


class GetAttachmentsRequest(BaseModel):
    """Request model for downloading attachments."""

    message_id: str = Field(..., description="Message ID")
    output_dir: str = Field(..., description="Directory to save attachments")
