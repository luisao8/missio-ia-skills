#!/usr/bin/env python3
"""CLI script to update a GitHub issue."""

import argparse
import json
import sys

from github_service import GitHubService


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Update an existing issue in a GitHub repository"
    )
    parser.add_argument(
        "--repo",
        type=str,
        required=True,
        help="Repository full name (owner/repo)"
    )
    parser.add_argument(
        "--issue-number",
        type=int,
        required=True,
        help="Issue number to update"
    )
    parser.add_argument(
        "--title",
        type=str,
        default=None,
        help="New issue title"
    )
    parser.add_argument(
        "--body",
        type=str,
        default=None,
        help="New issue body/description"
    )
    parser.add_argument(
        "--state",
        type=str,
        choices=["open", "closed"],
        default=None,
        help="New issue state"
    )
    parser.add_argument(
        "--labels",
        type=str,
        default=None,
        help="Comma-separated list of labels (replaces existing)"
    )

    args = parser.parse_args()

    labels = args.labels.split(",") if args.labels else None

    try:
        service = GitHubService()
        issue = service.update_issue(
            repo_full_name=args.repo,
            issue_number=args.issue_number,
            title=args.title,
            body=args.body,
            state=args.state,
            labels=labels
        )
        print(json.dumps(issue.model_dump(), indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
