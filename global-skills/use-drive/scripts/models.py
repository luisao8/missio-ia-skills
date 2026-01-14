"""
Pydantic models for Google Drive entities.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DriveFile(BaseModel):
    """Represents a file in Google Drive."""

    id: str = Field(..., description="Unique file ID")
    name: str = Field(..., description="File name")
    mime_type: Optional[str] = Field(None, alias="mimeType", description="MIME type")
    size: Optional[int] = Field(None, description="File size in bytes")
    created_time: Optional[datetime] = Field(
        None, alias="createdTime", description="Creation timestamp"
    )
    modified_time: Optional[datetime] = Field(
        None, alias="modifiedTime", description="Last modification timestamp"
    )
    parents: Optional[list[str]] = Field(None, description="Parent folder IDs")
    web_link: Optional[str] = Field(
        None, alias="webViewLink", description="Web view URL"
    )

    class Config:
        populate_by_name = True


class DriveFolder(BaseModel):
    """Represents a folder in Google Drive."""

    id: str = Field(..., description="Unique folder ID")
    name: str = Field(..., description="Folder name")
    parents: Optional[list[str]] = Field(None, description="Parent folder IDs")
    web_link: Optional[str] = Field(
        None, alias="webViewLink", description="Web view URL"
    )

    class Config:
        populate_by_name = True


class Permission(BaseModel):
    """Represents a permission on a file or folder."""

    id: str = Field(..., description="Permission ID")
    type: str = Field(..., description="Permission type (user, group, domain, anyone)")
    role: str = Field(..., description="Permission role (reader, writer, commenter, owner)")
    email: Optional[str] = Field(
        None, alias="emailAddress", description="Email address (for user/group)"
    )
    display_name: Optional[str] = Field(
        None, alias="displayName", description="Display name"
    )

    class Config:
        populate_by_name = True


class UploadResult(BaseModel):
    """Result of a file upload operation."""

    id: str = Field(..., description="Uploaded file ID")
    name: str = Field(..., description="File name")
    mime_type: Optional[str] = Field(None, alias="mimeType", description="MIME type")
    size: Optional[int] = Field(None, description="File size in bytes")
    web_link: Optional[str] = Field(
        None, alias="webViewLink", description="Web view URL"
    )
    parents: Optional[list[str]] = Field(None, description="Parent folder IDs")

    class Config:
        populate_by_name = True


class DownloadResult(BaseModel):
    """Result of a file download operation."""

    file_id: str = Field(..., description="Downloaded file ID")
    name: str = Field(..., description="File name")
    output_path: str = Field(..., description="Local output path")
    size: Optional[int] = Field(None, description="File size in bytes")
    mime_type: Optional[str] = Field(None, description="MIME type")


class DeleteResult(BaseModel):
    """Result of a file deletion operation."""

    status: str = Field(..., description="Deletion status")
    file_id: str = Field(..., description="Deleted file ID")
    name: str = Field(..., description="Deleted file name")


class ShareResult(BaseModel):
    """Result of a file share operation."""

    permission: Permission = Field(..., description="Created permission")
    file_name: str = Field(..., description="Shared file name")
    web_link: Optional[str] = Field(None, description="Shareable link")
