"""Pydantic models for Google Docs data structures."""

from typing import Optional
from pydantic import BaseModel, Field


class TextStyle(BaseModel):
    """Style properties for text."""

    bold: bool = False
    italic: bool = False
    underline: bool = False
    strikethrough: bool = False
    font_size: Optional[int] = None
    font_family: Optional[str] = None
    foreground_color: Optional[str] = None
    background_color: Optional[str] = None
    link_url: Optional[str] = None


class TextRun(BaseModel):
    """Represents a run of text within a document."""

    content: str = Field(..., description="The text content")
    start_index: int = Field(..., description="Starting character index in document")
    end_index: int = Field(..., description="Ending character index in document")
    style: Optional[TextStyle] = Field(default=None, description="Text styling properties")

    class Config:
        json_schema_extra = {
            "example": {
                "content": "Hello, World!",
                "start_index": 1,
                "end_index": 14,
                "style": {
                    "bold": True,
                    "font_size": 12
                }
            }
        }


class Document(BaseModel):
    """Represents a Google Docs document."""

    id: str = Field(..., description="The document ID")
    title: str = Field(..., description="The document title")
    body: str = Field(default="", description="The plain text content of the document")
    revision_id: str = Field(default="", description="The revision ID of the document")
    link: Optional[str] = Field(default=None, description="Web view link to the document")
    character_count: int = Field(default=0, description="Number of characters in the document")
    created_time: Optional[str] = Field(default=None, description="ISO timestamp of creation")
    modified_time: Optional[str] = Field(default=None, description="ISO timestamp of last modification")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "1abc123def456",
                "title": "My Document",
                "body": "This is the document content.",
                "revision_id": "ALm37BWkqz...",
                "link": "https://docs.google.com/document/d/1abc123def456/edit",
                "character_count": 29,
                "created_time": "2024-01-15T10:30:00.000Z",
                "modified_time": "2024-01-15T14:45:00.000Z"
            }
        }


class DocumentInfo(BaseModel):
    """Metadata about a Google Docs document."""

    id: str = Field(..., description="The document ID")
    title: str = Field(..., description="The document title")
    character_count: int = Field(default=0, description="Number of characters")
    revision_id: str = Field(default="", description="Current revision ID")
    link: str = Field(default="", description="Web view link")
    created_time: str = Field(default="", description="ISO timestamp of creation")
    modified_time: str = Field(default="", description="ISO timestamp of last modification")
    owners: list[str] = Field(default_factory=list, description="Email addresses of document owners")


class CreateDocumentResult(BaseModel):
    """Result of creating a new document."""

    id: str = Field(..., description="The new document ID")
    title: str = Field(..., description="The document title")
    link: str = Field(default="", description="Web view link")
    content_length: int = Field(default=0, description="Length of initial content")


class UpdateResult(BaseModel):
    """Result of an update operation."""

    id: str = Field(..., description="The document ID")
    success: bool = Field(default=True, description="Whether the operation succeeded")
    characters_added: int = Field(default=0, description="Number of characters added")
    characters_removed: int = Field(default=0, description="Number of characters removed")


class ReplaceResult(BaseModel):
    """Result of a replace operation."""

    id: str = Field(..., description="The document ID")
    find: str = Field(..., description="Text that was searched for")
    replace: str = Field(..., description="Text that was used as replacement")
    occurrences_changed: int = Field(default=0, description="Number of replacements made")


class ExportResult(BaseModel):
    """Result of exporting a document."""

    id: str = Field(..., description="The document ID")
    title: str = Field(..., description="The document title")
    format: str = Field(..., description="Export format (pdf, docx, txt, html)")
    file_path: str = Field(..., description="Path to the exported file")
    exported: bool = Field(default=True, description="Whether export succeeded")
