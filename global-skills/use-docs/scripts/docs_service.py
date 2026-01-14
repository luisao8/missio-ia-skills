"""Google Docs Service.

This module provides a DocsService class for interacting with Google Docs API.
It handles OAuth authentication and provides methods for creating, reading,
updating, and exporting documents.
"""

import json
import os
from pathlib import Path
from typing import Any, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# OAuth 2.0 scopes for Google Docs
SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive.file",
]

# Default credentials path (relative to this file)
DEFAULT_CREDENTIALS_PATH = Path(__file__).parent.parent.parent.parent.parent / "MCP_servers" / "google-credentials"


class DocsServiceError(Exception):
    """Custom exception for DocsService errors."""
    pass


class DocsService:
    """Service class for interacting with Google Docs API."""

    def __init__(self, credentials_path: Optional[str] = None):
        """Initialize DocsService with optional credentials path.

        Args:
            credentials_path: Path to the directory containing credentials.json
                            and token files. Defaults to MCP_servers/google-credentials/
        """
        if credentials_path:
            self.credentials_dir = Path(credentials_path)
        else:
            self.credentials_dir = DEFAULT_CREDENTIALS_PATH

        self._docs_service = None
        self._drive_service = None

    def _get_credentials(self) -> Credentials:
        """Authenticate and return Google credentials."""
        creds = None
        credentials_file = self.credentials_dir / "credentials.json"
        token_file = self.credentials_dir / "token-docs.json"

        if not credentials_file.exists():
            raise DocsServiceError(
                f"Credentials file not found: {credentials_file}\n"
                "Please set up OAuth credentials for Google Docs."
            )

        # Load existing token
        if token_file.exists():
            creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)

        # Refresh or create new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(credentials_file), SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save the credentials
            with open(token_file, "w") as token:
                token.write(creds.to_json())

        return creds

    @property
    def docs_service(self):
        """Get or create the Google Docs service."""
        if self._docs_service is None:
            creds = self._get_credentials()
            self._docs_service = build("docs", "v1", credentials=creds)
        return self._docs_service

    @property
    def drive_service(self):
        """Get or create the Google Drive service."""
        if self._drive_service is None:
            creds = self._get_credentials()
            self._drive_service = build("drive", "v3", credentials=creds)
        return self._drive_service

    def create_document(
        self,
        title: str,
        content: Optional[str] = None,
        folder_id: Optional[str] = None
    ) -> dict[str, Any]:
        """Create a new Google Doc.

        Args:
            title: Title of the document
            content: Optional initial text content
            folder_id: Optional folder ID to create document in

        Returns:
            Dictionary with document info (id, title, link)
        """
        try:
            # Create document
            document = self.docs_service.documents().create(
                body={"title": title}
            ).execute()

            doc_id = document["documentId"]
            doc_title = document["title"]

            # Add initial content if provided
            if content:
                requests = [
                    {
                        "insertText": {
                            "location": {"index": 1},
                            "text": content,
                        }
                    }
                ]
                self.docs_service.documents().batchUpdate(
                    documentId=doc_id,
                    body={"requests": requests}
                ).execute()

            # Move to folder if specified
            if folder_id:
                self.drive_service.files().update(
                    fileId=doc_id,
                    addParents=folder_id,
                    fields="id, parents"
                ).execute()

            # Get Drive link
            file = self.drive_service.files().get(
                fileId=doc_id,
                fields="webViewLink"
            ).execute()

            return {
                "id": doc_id,
                "title": doc_title,
                "link": file.get("webViewLink", ""),
                "content_length": len(content) if content else 0
            }

        except HttpError as e:
            raise DocsServiceError(f"Failed to create document: {e}")

    def read_document(self, doc_id: str) -> dict[str, Any]:
        """Read the content of a Google Doc.

        Args:
            doc_id: Document ID

        Returns:
            Dictionary with document info and content
        """
        try:
            document = self.docs_service.documents().get(documentId=doc_id).execute()

            # Extract text from document
            content = document.get("body", {}).get("content", [])
            text_parts = []

            for element in content:
                if "paragraph" in element:
                    paragraph = element["paragraph"]
                    for text_run in paragraph.get("elements", []):
                        if "textRun" in text_run:
                            text_parts.append(text_run["textRun"]["content"])

            full_text = "".join(text_parts)

            return {
                "id": doc_id,
                "title": document.get("title", "Untitled"),
                "content": full_text,
                "content_length": len(full_text),
                "revision_id": document.get("revisionId", "")
            }

        except HttpError as e:
            raise DocsServiceError(f"Failed to read document: {e}")

    def update_document(self, doc_id: str, content: str) -> dict[str, Any]:
        """Update document content (replaces all content).

        Args:
            doc_id: Document ID
            content: New content to replace existing content

        Returns:
            Dictionary with update result
        """
        try:
            # First, get current document to find content range
            document = self.docs_service.documents().get(documentId=doc_id).execute()
            body_content = document.get("body", {}).get("content", [])

            # Find end index (excluding final newline)
            end_index = 1
            if body_content:
                last_element = body_content[-1]
                end_index = last_element.get("endIndex", 1)

            # Delete existing content and insert new
            requests = []

            # Delete existing content if any (index 1 to end-1)
            if end_index > 2:
                requests.append({
                    "deleteContentRange": {
                        "range": {
                            "startIndex": 1,
                            "endIndex": end_index - 1
                        }
                    }
                })

            # Insert new content
            requests.append({
                "insertText": {
                    "location": {"index": 1},
                    "text": content,
                }
            })

            self.docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={"requests": requests}
            ).execute()

            return {
                "id": doc_id,
                "title": document.get("title", "Untitled"),
                "content_length": len(content),
                "updated": True
            }

        except HttpError as e:
            raise DocsServiceError(f"Failed to update document: {e}")

    def append_text(self, doc_id: str, text: str) -> dict[str, Any]:
        """Append text to the end of a document.

        Args:
            doc_id: Document ID
            text: Text to append

        Returns:
            Dictionary with result
        """
        try:
            # Get document to find end index
            document = self.docs_service.documents().get(documentId=doc_id).execute()
            body_content = document.get("body", {}).get("content", [])

            end_index = 1
            if body_content:
                last_element = body_content[-1]
                end_index = last_element.get("endIndex", 1)

            # Insert text at end
            requests = [
                {
                    "insertText": {
                        "location": {"index": end_index - 1},
                        "text": text,
                    }
                }
            ]

            self.docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={"requests": requests}
            ).execute()

            return {
                "id": doc_id,
                "characters_added": len(text),
                "appended": True
            }

        except HttpError as e:
            raise DocsServiceError(f"Failed to append text: {e}")

    def insert_text(self, doc_id: str, text: str, index: int) -> dict[str, Any]:
        """Insert text at a specific position in the document.

        Args:
            doc_id: Document ID
            text: Text to insert
            index: Character index where to insert (1 = start of document)

        Returns:
            Dictionary with result
        """
        try:
            requests = [
                {
                    "insertText": {
                        "location": {"index": index},
                        "text": text,
                    }
                }
            ]

            self.docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={"requests": requests}
            ).execute()

            return {
                "id": doc_id,
                "characters_added": len(text),
                "insert_index": index,
                "inserted": True
            }

        except HttpError as e:
            raise DocsServiceError(f"Failed to insert text: {e}")

    def replace_text(
        self,
        doc_id: str,
        find: str,
        replace: str,
        match_case: bool = False
    ) -> dict[str, Any]:
        """Replace all occurrences of text in the document.

        Args:
            doc_id: Document ID
            find: Text to find
            replace: Text to replace with
            match_case: Whether to match case (default False)

        Returns:
            Dictionary with number of replacements
        """
        try:
            requests = [
                {
                    "replaceAllText": {
                        "containsText": {
                            "text": find,
                            "matchCase": match_case,
                        },
                        "replaceText": replace,
                    }
                }
            ]

            result = self.docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={"requests": requests}
            ).execute()

            # Count replacements
            occurrences = 0
            for reply in result.get("replies", []):
                if "replaceAllText" in reply:
                    occurrences = reply["replaceAllText"].get("occurrencesChanged", 0)

            return {
                "id": doc_id,
                "find": find,
                "replace": replace,
                "occurrences_changed": occurrences
            }

        except HttpError as e:
            raise DocsServiceError(f"Failed to replace text: {e}")

    def export_document(
        self,
        doc_id: str,
        format: str,
        output_path: Optional[str] = None
    ) -> dict[str, Any]:
        """Export document to various formats.

        Args:
            doc_id: Document ID
            format: Export format (pdf, docx, txt, html)
            output_path: Optional path to save file (uses title if not provided)

        Returns:
            Dictionary with export result and file path
        """
        # Map format to MIME type
        mime_types = {
            "pdf": "application/pdf",
            "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "txt": "text/plain",
            "html": "text/html",
        }

        format_lower = format.lower()
        if format_lower not in mime_types:
            raise DocsServiceError(
                f"Unsupported format: {format}. "
                f"Supported formats: {', '.join(mime_types.keys())}"
            )

        try:
            # Get document title for filename
            document = self.docs_service.documents().get(documentId=doc_id).execute()
            title = document.get("title", "document")

            # Clean title for filename
            safe_title = "".join(c for c in title if c.isalnum() or c in " -_").strip()
            safe_title = safe_title or "document"

            # Determine output path
            if output_path:
                file_path = Path(output_path)
            else:
                file_path = Path.cwd() / f"{safe_title}.{format_lower}"

            # Export document
            content = self.drive_service.files().export(
                fileId=doc_id,
                mimeType=mime_types[format_lower]
            ).execute()

            # Write to file
            mode = "wb" if format_lower in ["pdf", "docx"] else "w"
            encoding = None if format_lower in ["pdf", "docx"] else "utf-8"

            with open(file_path, mode, encoding=encoding) as f:
                if isinstance(content, bytes):
                    f.write(content)
                else:
                    f.write(content)

            return {
                "id": doc_id,
                "title": title,
                "format": format_lower,
                "file_path": str(file_path),
                "exported": True
            }

        except HttpError as e:
            raise DocsServiceError(f"Failed to export document: {e}")

    def get_document_info(self, doc_id: str) -> dict[str, Any]:
        """Get metadata about a document.

        Args:
            doc_id: Document ID

        Returns:
            Dictionary with document info
        """
        try:
            # Get document from Docs API
            document = self.docs_service.documents().get(documentId=doc_id).execute()

            # Count characters
            content = document.get("body", {}).get("content", [])
            char_count = 0
            for element in content:
                if "paragraph" in element:
                    paragraph = element["paragraph"]
                    for text_run in paragraph.get("elements", []):
                        if "textRun" in text_run:
                            char_count += len(text_run["textRun"]["content"])

            # Get Drive metadata
            file = self.drive_service.files().get(
                fileId=doc_id,
                fields="webViewLink, modifiedTime, createdTime, owners"
            ).execute()

            return {
                "id": doc_id,
                "title": document.get("title", "Untitled"),
                "character_count": char_count,
                "revision_id": document.get("revisionId", ""),
                "link": file.get("webViewLink", ""),
                "created_time": file.get("createdTime", ""),
                "modified_time": file.get("modifiedTime", ""),
                "owners": [owner.get("emailAddress", "") for owner in file.get("owners", [])]
            }

        except HttpError as e:
            raise DocsServiceError(f"Failed to get document info: {e}")


def output_json(data: dict[str, Any]) -> None:
    """Output data as formatted JSON to stdout."""
    print(json.dumps(data, indent=2, ensure_ascii=False))


def output_error(message: str) -> None:
    """Output error as JSON to stdout."""
    output_json({"error": message})
