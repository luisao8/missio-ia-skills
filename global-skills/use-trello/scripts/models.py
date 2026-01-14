"""
Pydantic models for Trello API entities.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class Label(BaseModel):
    """Trello label model."""

    id: str
    name: str = ""
    color: str | None = None


class Comment(BaseModel):
    """Trello comment model."""

    id: str
    text: str = Field(alias="data.text", default="")
    date: datetime | None = None
    member: str | None = Field(alias="memberCreator.fullName", default=None)

    class Config:
        populate_by_name = True


class Card(BaseModel):
    """Trello card model."""

    id: str
    name: str
    desc: str = ""
    due: datetime | None = None
    labels: list[Label] = []
    list_id: str = Field(alias="idList", default="")
    url: str = ""
    closed: bool = False

    class Config:
        populate_by_name = True


class TrelloList(BaseModel):
    """Trello list model (renamed to avoid conflict with Python list)."""

    id: str
    name: str
    cards: list[Card] = []
    closed: bool = False


class Board(BaseModel):
    """Trello board model."""

    id: str
    name: str
    url: str = ""
    lists: list[TrelloList] = []
    closed: bool = False
