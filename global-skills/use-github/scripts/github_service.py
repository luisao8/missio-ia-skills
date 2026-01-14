"""GitHub API Service using PyGithub."""

import os
from typing import Optional

from github import Github, Auth
from github.GithubException import GithubException

from .models import Repository, Issue, PullRequest, Branch, FileContent


class GitHubService:
    """Service class for interacting with GitHub API."""

    def __init__(self, token: Optional[str] = None):
        """Initialize GitHub service with authentication.

        Args:
            token: GitHub personal access token. If not provided,
                   reads from GITHUB_TOKEN environment variable.
        """
        self.token = token or os.environ.get("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GITHUB_TOKEN environment variable not set")

        auth = Auth.Token(self.token)
        self.github = Github(auth=auth)

    def get_repos(
        self,
        user: Optional[str] = None,
        repo_type: str = "all"
    ) -> list[Repository]:
        """Get repositories for a user.

        Args:
            user: Username to get repos for. If None, uses authenticated user.
            repo_type: Type of repos to return (all, owner, member).

        Returns:
            List of Repository objects.
        """
        try:
            if user:
                github_user = self.github.get_user(user)
                repos = github_user.get_repos()
            else:
                repos = self.github.get_user().get_repos(type=repo_type)

            return [
                Repository(
                    id=repo.id,
                    name=repo.name,
                    full_name=repo.full_name,
                    description=repo.description or "",
                    url=repo.html_url,
                    default_branch=repo.default_branch,
                    private=repo.private
                )
                for repo in repos
            ]
        except GithubException as e:
            raise RuntimeError(f"GitHub API error: {e.data.get('message', str(e))}")

    def get_repo(self, repo_full_name: str) -> Repository:
        """Get a specific repository.

        Args:
            repo_full_name: Full repository name (owner/repo).

        Returns:
            Repository object.
        """
        try:
            repo = self.github.get_repo(repo_full_name)
            return Repository(
                id=repo.id,
                name=repo.name,
                full_name=repo.full_name,
                description=repo.description or "",
                url=repo.html_url,
                default_branch=repo.default_branch,
                private=repo.private
            )
        except GithubException as e:
            raise RuntimeError(f"GitHub API error: {e.data.get('message', str(e))}")

    def get_issues(
        self,
        repo_full_name: str,
        state: str = "open",
        labels: Optional[list[str]] = None
    ) -> list[Issue]:
        """Get issues for a repository.

        Args:
            repo_full_name: Full repository name (owner/repo).
            state: Issue state (open, closed, all).
            labels: List of label names to filter by.

        Returns:
            List of Issue objects.
        """
        try:
            repo = self.github.get_repo(repo_full_name)

            kwargs: dict = {"state": state}
            if labels:
                kwargs["labels"] = [repo.get_label(label) for label in labels]

            issues = repo.get_issues(**kwargs)

            return [
                Issue(
                    id=issue.id,
                    number=issue.number,
                    title=issue.title,
                    body=issue.body or "",
                    state=issue.state,
                    labels=[label.name for label in issue.labels],
                    assignees=[assignee.login for assignee in issue.assignees],
                    created_at=issue.created_at.isoformat() if issue.created_at else ""
                )
                for issue in issues
                if issue.pull_request is None  # Exclude PRs
            ]
        except GithubException as e:
            raise RuntimeError(f"GitHub API error: {e.data.get('message', str(e))}")

    def create_issue(
        self,
        repo_full_name: str,
        title: str,
        body: Optional[str] = None,
        labels: Optional[list[str]] = None,
        assignees: Optional[list[str]] = None
    ) -> Issue:
        """Create an issue in a repository.

        Args:
            repo_full_name: Full repository name (owner/repo).
            title: Issue title.
            body: Issue body/description.
            labels: List of label names.
            assignees: List of usernames to assign.

        Returns:
            Created Issue object.
        """
        try:
            repo = self.github.get_repo(repo_full_name)

            kwargs: dict = {"title": title}
            if body:
                kwargs["body"] = body
            if labels:
                kwargs["labels"] = labels
            if assignees:
                kwargs["assignees"] = assignees

            issue = repo.create_issue(**kwargs)

            return Issue(
                id=issue.id,
                number=issue.number,
                title=issue.title,
                body=issue.body or "",
                state=issue.state,
                labels=[label.name for label in issue.labels],
                assignees=[assignee.login for assignee in issue.assignees],
                created_at=issue.created_at.isoformat() if issue.created_at else ""
            )
        except GithubException as e:
            raise RuntimeError(f"GitHub API error: {e.data.get('message', str(e))}")

    def update_issue(
        self,
        repo_full_name: str,
        issue_number: int,
        title: Optional[str] = None,
        body: Optional[str] = None,
        state: Optional[str] = None,
        labels: Optional[list[str]] = None
    ) -> Issue:
        """Update an existing issue.

        Args:
            repo_full_name: Full repository name (owner/repo).
            issue_number: Issue number to update.
            title: New title (optional).
            body: New body (optional).
            state: New state - open/closed (optional).
            labels: New labels (optional).

        Returns:
            Updated Issue object.
        """
        try:
            repo = self.github.get_repo(repo_full_name)
            issue = repo.get_issue(issue_number)

            kwargs: dict = {}
            if title:
                kwargs["title"] = title
            if body:
                kwargs["body"] = body
            if state:
                kwargs["state"] = state
            if labels is not None:
                kwargs["labels"] = labels

            if kwargs:
                issue.edit(**kwargs)

            return Issue(
                id=issue.id,
                number=issue.number,
                title=issue.title,
                body=issue.body or "",
                state=issue.state,
                labels=[label.name for label in issue.labels],
                assignees=[assignee.login for assignee in issue.assignees],
                created_at=issue.created_at.isoformat() if issue.created_at else ""
            )
        except GithubException as e:
            raise RuntimeError(f"GitHub API error: {e.data.get('message', str(e))}")

    def get_prs(
        self,
        repo_full_name: str,
        state: str = "open"
    ) -> list[PullRequest]:
        """Get pull requests for a repository.

        Args:
            repo_full_name: Full repository name (owner/repo).
            state: PR state (open, closed, all).

        Returns:
            List of PullRequest objects.
        """
        try:
            repo = self.github.get_repo(repo_full_name)
            prs = repo.get_pulls(state=state)

            return [
                PullRequest(
                    id=pr.id,
                    number=pr.number,
                    title=pr.title,
                    body=pr.body or "",
                    state=pr.state,
                    head=pr.head.ref,
                    base=pr.base.ref,
                    mergeable=pr.mergeable
                )
                for pr in prs
            ]
        except GithubException as e:
            raise RuntimeError(f"GitHub API error: {e.data.get('message', str(e))}")

    def create_pr(
        self,
        repo_full_name: str,
        title: str,
        head: str,
        base: str,
        body: Optional[str] = None
    ) -> PullRequest:
        """Create a pull request.

        Args:
            repo_full_name: Full repository name (owner/repo).
            title: PR title.
            head: Branch with changes.
            base: Branch to merge into.
            body: PR description (optional).

        Returns:
            Created PullRequest object.
        """
        try:
            repo = self.github.get_repo(repo_full_name)

            kwargs: dict = {"title": title, "head": head, "base": base}
            if body:
                kwargs["body"] = body

            pr = repo.create_pull(**kwargs)

            return PullRequest(
                id=pr.id,
                number=pr.number,
                title=pr.title,
                body=pr.body or "",
                state=pr.state,
                head=pr.head.ref,
                base=pr.base.ref,
                mergeable=pr.mergeable
            )
        except GithubException as e:
            raise RuntimeError(f"GitHub API error: {e.data.get('message', str(e))}")

    def merge_pr(
        self,
        repo_full_name: str,
        pr_number: int,
        merge_method: str = "merge"
    ) -> dict:
        """Merge a pull request.

        Args:
            repo_full_name: Full repository name (owner/repo).
            pr_number: PR number to merge.
            merge_method: Merge method (merge, squash, rebase).

        Returns:
            Dict with merge result.
        """
        try:
            repo = self.github.get_repo(repo_full_name)
            pr = repo.get_pull(pr_number)

            result = pr.merge(merge_method=merge_method)

            return {
                "merged": result.merged,
                "message": result.message,
                "sha": result.sha
            }
        except GithubException as e:
            raise RuntimeError(f"GitHub API error: {e.data.get('message', str(e))}")

    def get_branches(self, repo_full_name: str) -> list[Branch]:
        """Get branches for a repository.

        Args:
            repo_full_name: Full repository name (owner/repo).

        Returns:
            List of Branch objects.
        """
        try:
            repo = self.github.get_repo(repo_full_name)
            branches = repo.get_branches()

            return [
                Branch(
                    name=branch.name,
                    sha=branch.commit.sha,
                    protected=branch.protected
                )
                for branch in branches
            ]
        except GithubException as e:
            raise RuntimeError(f"GitHub API error: {e.data.get('message', str(e))}")

    def get_file(
        self,
        repo_full_name: str,
        path: str,
        ref: Optional[str] = None
    ) -> FileContent:
        """Get file content from a repository.

        Args:
            repo_full_name: Full repository name (owner/repo).
            path: File path in the repository.
            ref: Branch, tag, or commit SHA (optional).

        Returns:
            FileContent object.
        """
        try:
            repo = self.github.get_repo(repo_full_name)

            kwargs: dict = {}
            if ref:
                kwargs["ref"] = ref

            content = repo.get_contents(path, **kwargs)

            # Handle single file (not directory)
            if isinstance(content, list):
                raise RuntimeError(f"Path {path} is a directory, not a file")

            return FileContent(
                name=content.name,
                path=content.path,
                content=content.decoded_content.decode("utf-8") if content.content else "",
                sha=content.sha
            )
        except GithubException as e:
            raise RuntimeError(f"GitHub API error: {e.data.get('message', str(e))}")

    def search_code(
        self,
        query: str,
        repo_full_name: Optional[str] = None
    ) -> list[dict]:
        """Search for code in repositories.

        Args:
            query: Search query.
            repo_full_name: Limit search to specific repo (optional).

        Returns:
            List of search results.
        """
        try:
            search_query = query
            if repo_full_name:
                search_query = f"{query} repo:{repo_full_name}"

            results = self.github.search_code(search_query)

            return [
                {
                    "name": result.name,
                    "path": result.path,
                    "repository": result.repository.full_name,
                    "url": result.html_url,
                    "sha": result.sha
                }
                for result in results[:50]  # Limit results
            ]
        except GithubException as e:
            raise RuntimeError(f"GitHub API error: {e.data.get('message', str(e))}")
