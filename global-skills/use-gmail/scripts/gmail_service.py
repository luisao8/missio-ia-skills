"""Gmail Service for Claude Code Skill.

Provides authentication and methods for interacting with Gmail API.
"""

import base64
import os
import pickle
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import Optional, List, Dict, Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from bs4 import BeautifulSoup


# OAuth 2.0 scopes for Gmail
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.labels",
]

# Default credentials path (relative to this file)
DEFAULT_CREDENTIALS_DIR = Path(__file__).parent.parent.parent.parent.parent / "MCP_servers" / "google-credentials"


class GmailService:
    """Service class for Gmail API operations."""

    def __init__(self, credentials_path: Optional[str] = None):
        """Initialize Gmail service.

        Args:
            credentials_path: Path to OAuth credentials.json file.
                            If not provided, uses default path.
        """
        if credentials_path:
            self.credentials_path = Path(credentials_path)
        else:
            self.credentials_path = DEFAULT_CREDENTIALS_DIR / "credentials.json"

        self.credentials_dir = self.credentials_path.parent
        self.token_path = self.credentials_dir / "gmail_token.pickle"
        self._service = None

    def _get_service(self):
        """Authenticate and return Gmail service."""
        if self._service:
            return self._service

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
                        f"Credentials file not found at {self.credentials_path}. "
                        "Please ensure credentials.json exists."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.credentials_path), SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save the credentials
            with open(self.token_path, "wb") as token:
                pickle.dump(creds, token)

        self._service = build("gmail", "v1", credentials=creds)
        return self._service

    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
        html: bool = False,
        attachments: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Send an email.

        Args:
            to: Recipient email address(es), comma-separated
            subject: Email subject
            body: Email body (text or HTML)
            cc: CC recipients, comma-separated
            bcc: BCC recipients, comma-separated
            html: If True, body is treated as HTML
            attachments: List of file paths to attach

        Returns:
            Dict with sent message details
        """
        service = self._get_service()

        if attachments:
            message = MIMEMultipart()
            if html:
                message.attach(MIMEText(body, "html"))
            else:
                message.attach(MIMEText(body, "plain"))

            for file_path in attachments:
                path = Path(file_path)
                if not path.exists():
                    raise FileNotFoundError(f"Attachment not found: {file_path}")

                with open(path, "rb") as f:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename={path.name}"
                    )
                    message.attach(part)
        else:
            if html:
                message = MIMEText(body, "html")
            else:
                message = MIMEText(body, "plain")

        message["to"] = to
        message["subject"] = subject
        if cc:
            message["cc"] = cc
        if bcc:
            message["bcc"] = bcc

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        result = service.users().messages().send(
            userId="me", body={"raw": raw}
        ).execute()

        return {
            "id": result["id"],
            "threadId": result.get("threadId"),
            "labelIds": result.get("labelIds", []),
        }

    def search_emails(
        self,
        query: str = "",
        max_results: int = 10,
        label: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Search for emails using Gmail query syntax.

        Args:
            query: Gmail search query (e.g., "from:user@example.com")
            max_results: Maximum number of results to return
            label: Filter by label ID

        Returns:
            List of email dicts
        """
        service = self._get_service()

        if label:
            if query:
                query = f"label:{label} {query}"
            else:
                query = f"label:{label}"

        results = service.users().messages().list(
            userId="me",
            q=query,
            maxResults=max_results,
        ).execute()

        messages = results.get("messages", [])
        emails = []

        for msg in messages:
            email_data = self._get_message_details(msg["id"])
            emails.append(email_data)

        return emails

    def read_email(self, message_id: str) -> Dict[str, Any]:
        """Read a specific email by ID.

        Args:
            message_id: The message ID

        Returns:
            Dict with full email details
        """
        return self._get_message_details(message_id, full_body=True)

    def _get_message_details(
        self, message_id: str, full_body: bool = False
    ) -> Dict[str, Any]:
        """Get message details.

        Args:
            message_id: The message ID
            full_body: If True, include full body content

        Returns:
            Dict with message details
        """
        service = self._get_service()

        msg = service.users().messages().get(
            userId="me",
            id=message_id,
            format="full",
        ).execute()

        headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}

        # Extract body
        body = ""
        html_body = ""

        def extract_body(payload):
            nonlocal body, html_body
            if "body" in payload and payload["body"].get("data"):
                data = base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8")
                if payload.get("mimeType") == "text/html":
                    html_body = data
                    if not body:
                        soup = BeautifulSoup(data, "html.parser")
                        body = soup.get_text()
                else:
                    body = data
            if "parts" in payload:
                for part in payload["parts"]:
                    extract_body(part)

        extract_body(msg["payload"])

        # Extract attachments info
        attachments = []
        if "parts" in msg["payload"]:
            for part in msg["payload"]["parts"]:
                if part.get("filename"):
                    attachments.append({
                        "id": part["body"].get("attachmentId"),
                        "filename": part["filename"],
                        "mimeType": part.get("mimeType"),
                        "size": part["body"].get("size", 0),
                    })

        result = {
            "id": msg["id"],
            "threadId": msg["threadId"],
            "subject": headers.get("Subject", ""),
            "from": headers.get("From", ""),
            "to": headers.get("To", ""),
            "cc": headers.get("Cc", ""),
            "date": headers.get("Date", ""),
            "snippet": msg.get("snippet", ""),
            "labelIds": msg.get("labelIds", []),
            "attachments": attachments,
        }

        if full_body:
            result["body"] = body
            result["htmlBody"] = html_body

        return result

    def reply_email(
        self,
        message_id: str,
        body: str,
        html: bool = False,
    ) -> Dict[str, Any]:
        """Reply to an email.

        Args:
            message_id: The message ID to reply to
            body: Reply body
            html: If True, body is treated as HTML

        Returns:
            Dict with sent reply details
        """
        service = self._get_service()

        # Get original message
        original = service.users().messages().get(
            userId="me",
            id=message_id,
            format="metadata",
            metadataHeaders=["Subject", "From", "To", "Message-ID", "References"],
        ).execute()

        headers = {h["name"]: h["value"] for h in original["payload"]["headers"]}

        # Create reply
        if html:
            message = MIMEText(body, "html")
        else:
            message = MIMEText(body, "plain")

        # Set reply headers
        subject = headers.get("Subject", "")
        if not subject.lower().startswith("re:"):
            subject = f"Re: {subject}"

        message["to"] = headers.get("From", "")
        message["subject"] = subject
        message["In-Reply-To"] = headers.get("Message-ID", "")

        # Build References header
        references = headers.get("References", "")
        if headers.get("Message-ID"):
            if references:
                references = f"{references} {headers['Message-ID']}"
            else:
                references = headers["Message-ID"]
        message["References"] = references

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        result = service.users().messages().send(
            userId="me",
            body={
                "raw": raw,
                "threadId": original["threadId"],
            }
        ).execute()

        return {
            "id": result["id"],
            "threadId": result.get("threadId"),
            "labelIds": result.get("labelIds", []),
        }

    def create_draft(
        self,
        to: str,
        subject: str,
        body: str,
        html: bool = False,
    ) -> Dict[str, Any]:
        """Create an email draft.

        Args:
            to: Recipient email address(es)
            subject: Email subject
            body: Email body
            html: If True, body is treated as HTML

        Returns:
            Dict with draft details
        """
        service = self._get_service()

        if html:
            message = MIMEText(body, "html")
        else:
            message = MIMEText(body, "plain")

        message["to"] = to
        message["subject"] = subject

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        draft = service.users().drafts().create(
            userId="me",
            body={"message": {"raw": raw}}
        ).execute()

        return {
            "id": draft["id"],
            "messageId": draft["message"]["id"],
        }

    def list_threads(
        self,
        query: str = "",
        max_results: int = 10,
    ) -> List[Dict[str, Any]]:
        """List email threads.

        Args:
            query: Gmail search query
            max_results: Maximum number of results

        Returns:
            List of thread dicts
        """
        service = self._get_service()

        results = service.users().threads().list(
            userId="me",
            q=query if query else None,
            maxResults=max_results,
        ).execute()

        threads = results.get("threads", [])
        thread_list = []

        for thread in threads:
            thread_data = service.users().threads().get(
                userId="me",
                id=thread["id"],
                format="metadata",
                metadataHeaders=["Subject", "From", "Date"],
            ).execute()

            messages = thread_data.get("messages", [])
            first_msg = messages[0] if messages else {}
            headers = {
                h["name"]: h["value"]
                for h in first_msg.get("payload", {}).get("headers", [])
            }

            thread_list.append({
                "id": thread["id"],
                "snippet": thread_data.get("snippet", ""),
                "messageCount": len(messages),
                "subject": headers.get("Subject", ""),
                "from": headers.get("From", ""),
                "date": headers.get("Date", ""),
            })

        return thread_list

    def list_labels(self) -> List[Dict[str, Any]]:
        """List all Gmail labels.

        Returns:
            List of label dicts
        """
        service = self._get_service()

        results = service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])

        label_list = []
        for label in labels:
            label_list.append({
                "id": label["id"],
                "name": label["name"],
                "type": label.get("type", "user"),
            })

        return label_list

    def add_label(self, message_id: str, label_id: str) -> Dict[str, Any]:
        """Add a label to a message.

        Args:
            message_id: The message ID
            label_id: The label ID to add

        Returns:
            Dict with updated message details
        """
        service = self._get_service()

        result = service.users().messages().modify(
            userId="me",
            id=message_id,
            body={"addLabelIds": [label_id]}
        ).execute()

        return {
            "id": result["id"],
            "threadId": result.get("threadId"),
            "labelIds": result.get("labelIds", []),
        }

    def get_attachments(
        self,
        message_id: str,
        output_dir: str,
    ) -> List[Dict[str, Any]]:
        """Download attachments from an email.

        Args:
            message_id: The message ID
            output_dir: Directory to save attachments

        Returns:
            List of downloaded file dicts
        """
        service = self._get_service()
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        msg = service.users().messages().get(
            userId="me",
            id=message_id,
            format="full",
        ).execute()

        downloaded = []

        def download_attachments(payload):
            if "parts" in payload:
                for part in payload["parts"]:
                    if part.get("filename") and part["body"].get("attachmentId"):
                        attachment = service.users().messages().attachments().get(
                            userId="me",
                            messageId=message_id,
                            id=part["body"]["attachmentId"]
                        ).execute()

                        data = base64.urlsafe_b64decode(attachment["data"])
                        file_path = output_path / part["filename"]

                        with open(file_path, "wb") as f:
                            f.write(data)

                        downloaded.append({
                            "filename": part["filename"],
                            "path": str(file_path),
                            "size": len(data),
                            "mimeType": part.get("mimeType"),
                        })

                    download_attachments(part)

        download_attachments(msg["payload"])

        return downloaded
