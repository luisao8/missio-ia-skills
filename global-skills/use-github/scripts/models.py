"""Pydantic models for GitHub API responses."""

from typing import Optional
from pydantic import BaseModel


class Repository(BaseModel):
    """GitHub repository model."""

    id: int
    name: str
    full_name: str
    description: str
    url: str
    default_branch: str
    private: bool


class Issue(BaseModel):
    """GitHub issue model."""

    id: int
    number: int
    title: str
    body: str
    state: str
    labels: list[str]
    assignees: list[str]
    created_at: str


class PullRequest(BaseModel):
    """GitHub pull request model."""

    id: int
    number: int
    title: str
    body: str
    state: str
    head: str
    base: str
    mergeable: Optional[bool] = None


class Branch(BaseModel):
    """GitHub branch model."""

    name: str
    sha: str
    protected: bool


class FileContent(BaseModel):
    """GitHub file content model."""

    name: str
    path: str
    content: str
    sha: str
