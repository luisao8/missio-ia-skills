"""
Google Drive service class for interacting with Drive API.

Provides methods for file operations: upload, download, list, search,
create folder, move, copy, delete, share, and get file info.
"""

import io
import json
import mimetypes
import os
from pathlib import Path
from typing import Any, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload


# OAuth 2.0 scopes for Google Drive
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive.metadata",
]

# Default credentials path (relative to this file)
DEFAULT_CREDENTIALS_DIR = Path(__file__).parent.parent.parent.parent.parent.parent / "MCP_servers" / "google-credentials"


class DriveService:
    """Service class for Google Drive API operations."""

    def __init__(
        self,
        credentials_path: Optional[str] = None,
        token_path: Optional[str] = None,
    ):
        """
        Initialize DriveService with authentication.

        Args:
            credentials_path: Path to OAuth credentials JSON file.
                            Defaults to MCP_servers/google-credentials/credentials.json
            token_path: Path to store/load user token.
                       Defaults to credentials directory/token-drive.json
        """
        self.credentials_path = Path(
            credentials_path
            or os.environ.get("GOOGLE_CREDENTIALS_PATH")
            or DEFAULT_CREDENTIALS_DIR / "credentials.json"
        )
        self.token_path = Path(
            token_path or self.credentials_path.parent / "token-drive.json"
        )
        self._service = None

    def _get_credentials(self) -> Credentials:
        """Load or create OAuth credentials."""
        creds = None

        # Load existing token
        if self.token_path.exists():
            creds = Credentials.from_authorized_user_file(str(self.token_path), SCOPES)

        # Refresh or create new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not self.credentials_path.exists():
                    raise FileNotFoundError(
                        f"Credentials file not found: {self.credentials_path}"
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.credentials_path), SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save the credentials
            with open(self.token_path, "w") as token:
                token.write(creds.to_json())

        return creds

    @property
    def service(self):
        """Get or create the Drive service."""
        if self._service is None:
            creds = self._get_credentials()
            self._service = build("drive", "v3", credentials=creds)
        return self._service

    def upload_file(
        self,
        file_path: str,
        name: Optional[str] = None,
        parent_id: Optional[str] = None,
        mime_type: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Upload a file to Google Drive.

        Args:
            file_path: Local file path to upload
            name: Name for the file in Drive (defaults to filename)
            parent_id: Parent folder ID (defaults to root)
            mime_type: MIME type (auto-detected if not provided)

        Returns:
            Dictionary with uploaded file info
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Get filename if name not provided
        if not name:
            name = file_path.name

        # Auto-detect MIME type if not provided
        if not mime_type:
            mime_type, _ = mimetypes.guess_type(str(file_path))
            if not mime_type:
                mime_type = "application/octet-stream"

        # Prepare file metadata
        file_metadata: dict[str, Any] = {"name": name}
        if parent_id:
            file_metadata["parents"] = [parent_id]

        # Upload the file
        media = MediaFileUpload(str(file_path), mimetype=mime_type, resumable=True)

        uploaded_file = (
            self.service.files()
            .create(
                body=file_metadata,
                media_body=media,
                fields="id, name, mimeType, size, webViewLink, parents, createdTime, modifiedTime",
            )
            .execute()
        )

        return uploaded_file

    def download_file(
        self,
        file_id: str,
        output_path: str,
    ) -> dict[str, Any]:
        """
        Download a file from Google Drive.

        Args:
            file_id: ID of the file to download
            output_path: Local path to save the file

        Returns:
            Dictionary with download info including output path
        """
        # Get file metadata first
        file_metadata = (
            self.service.files()
            .get(fileId=file_id, fields="name, mimeType, size")
            .execute()
        )

        # Check if it's a Google Workspace file (need to export)
        mime_type = file_metadata.get("mimeType", "")
        if mime_type.startswith("application/vnd.google-apps."):
            # Export Google Docs files
            export_mime = self._get_export_mime_type(mime_type)
            request = self.service.files().export_media(
                fileId=file_id, mimeType=export_mime
            )
        else:
            request = self.service.files().get_media(fileId=file_id)

        # Download the file
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "wb") as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()

        return {
            "file_id": file_id,
            "name": file_metadata["name"],
            "output_path": str(output_path),
            "size": file_metadata.get("size"),
            "mime_type": file_metadata.get("mimeType"),
        }

    def _get_export_mime_type(self, google_mime: str) -> str:
        """Get export MIME type for Google Workspace files."""
        export_types = {
            "application/vnd.google-apps.document": "application/pdf",
            "application/vnd.google-apps.spreadsheet": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/vnd.google-apps.presentation": "application/pdf",
            "application/vnd.google-apps.drawing": "image/png",
        }
        return export_types.get(google_mime, "application/pdf")

    def list_files(
        self,
        parent_id: Optional[str] = None,
        max_results: int = 100,
        mime_type: Optional[str] = None,
        order_by: str = "modifiedTime desc",
    ) -> list[dict[str, Any]]:
        """
        List files in a folder.

        Args:
            parent_id: Parent folder ID (defaults to all files)
            max_results: Maximum number of results (1-1000)
            mime_type: Filter by MIME type
            order_by: Sort order (default: modifiedTime desc)

        Returns:
            List of file dictionaries
        """
        query_parts = []
        if parent_id:
            query_parts.append(f"'{parent_id}' in parents")
        if mime_type:
            query_parts.append(f"mimeType='{mime_type}'")

        query = " and ".join(query_parts) if query_parts else None

        results = (
            self.service.files()
            .list(
                q=query,
                pageSize=min(max_results, 1000),
                orderBy=order_by,
                fields="files(id, name, mimeType, size, modifiedTime, createdTime, parents, webViewLink)",
            )
            .execute()
        )

        return results.get("files", [])

    def search_files(
        self,
        query: str,
        max_results: int = 100,
    ) -> list[dict[str, Any]]:
        """
        Search for files using Drive query syntax.

        Args:
            query: Search query (supports Drive search operators)
            max_results: Maximum number of results

        Returns:
            List of matching files
        """
        results = (
            self.service.files()
            .list(
                q=query,
                pageSize=min(max_results, 1000),
                orderBy="modifiedTime desc",
                fields="files(id, name, mimeType, size, modifiedTime, createdTime, parents, webViewLink)",
            )
            .execute()
        )

        return results.get("files", [])

    def create_folder(
        self,
        name: str,
        parent_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Create a folder in Google Drive.

        Args:
            name: Name of the folder
            parent_id: Parent folder ID (defaults to root)

        Returns:
            Dictionary with created folder info
        """
        file_metadata: dict[str, Any] = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
        }

        if parent_id:
            file_metadata["parents"] = [parent_id]

        folder = (
            self.service.files()
            .create(body=file_metadata, fields="id, name, webViewLink, parents")
            .execute()
        )

        return folder

    def move_file(
        self,
        file_id: str,
        new_parent_id: str,
    ) -> dict[str, Any]:
        """
        Move a file to a different folder.

        Args:
            file_id: ID of the file to move
            new_parent_id: ID of the new parent folder

        Returns:
            Dictionary with updated file info
        """
        # Get current parents
        file = self.service.files().get(fileId=file_id, fields="parents, name").execute()
        previous_parents = ",".join(file.get("parents", []))

        # Move file
        updated_file = (
            self.service.files()
            .update(
                fileId=file_id,
                addParents=new_parent_id,
                removeParents=previous_parents,
                fields="id, name, parents, webViewLink",
            )
            .execute()
        )

        return updated_file

    def copy_file(
        self,
        file_id: str,
        new_name: Optional[str] = None,
        parent_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Copy a file.

        Args:
            file_id: ID of the file to copy
            new_name: Name for the copy (defaults to "Copy of [original]")
            parent_id: Parent folder for the copy

        Returns:
            Dictionary with copied file info
        """
        body: dict[str, Any] = {}
        if new_name:
            body["name"] = new_name
        if parent_id:
            body["parents"] = [parent_id]

        copied_file = (
            self.service.files()
            .copy(
                fileId=file_id,
                body=body,
                fields="id, name, mimeType, size, webViewLink, parents, createdTime",
            )
            .execute()
        )

        return copied_file

    def delete_file(
        self,
        file_id: str,
    ) -> dict[str, Any]:
        """
        Delete a file (moves to trash).

        Args:
            file_id: ID of the file to delete

        Returns:
            Dictionary with deletion status
        """
        # Get file name before deleting
        file = self.service.files().get(fileId=file_id, fields="name").execute()

        # Delete (moves to trash)
        self.service.files().delete(fileId=file_id).execute()

        return {
            "status": "deleted",
            "file_id": file_id,
            "name": file["name"],
        }

    def share_file(
        self,
        file_id: str,
        email: Optional[str] = None,
        role: str = "reader",
        share_type: str = "user",
    ) -> dict[str, Any]:
        """
        Share a file with permissions.

        Args:
            file_id: ID of the file to share
            email: Email address (required for user/group type)
            role: Permission role (reader, writer, commenter, owner)
            share_type: Permission type (user, group, domain, anyone)

        Returns:
            Dictionary with permission info
        """
        permission: dict[str, Any] = {
            "type": share_type,
            "role": role,
        }

        if email:
            permission["emailAddress"] = email

        # Create permission
        created_permission = (
            self.service.permissions()
            .create(fileId=file_id, body=permission, fields="id, type, role, emailAddress")
            .execute()
        )

        # Get file info including webViewLink
        file = (
            self.service.files()
            .get(fileId=file_id, fields="name, webViewLink")
            .execute()
        )

        return {
            "permission": created_permission,
            "file": file,
        }

    def get_file_info(
        self,
        file_id: str,
        fields: str = "*",
    ) -> dict[str, Any]:
        """
        Get detailed information about a file.

        Args:
            file_id: ID of the file
            fields: Comma-separated fields to retrieve (default: all)

        Returns:
            Dictionary with file metadata
        """
        file = self.service.files().get(fileId=file_id, fields=fields).execute()
        return file


def get_drive_service(
    credentials_path: Optional[str] = None,
    token_path: Optional[str] = None,
) -> DriveService:
    """
    Factory function to create a DriveService instance.

    Args:
        credentials_path: Path to OAuth credentials JSON file
        token_path: Path to store/load user token

    Returns:
        DriveService instance
    """
    return DriveService(credentials_path=credentials_path, token_path=token_path)
