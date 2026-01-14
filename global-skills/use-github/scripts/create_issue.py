#!/usr/bin/env python3
"""CLI script to create a GitHub issue."""

import argparse
import json
import sys

from github_service import GitHubService


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Create a new issue in a GitHub repository"
    )
    parser.add_argument(
        "--repo",
        type=str,
        required=True,
        help="Repository full name (owner/repo)"
    )
    parser.add_argument(
        "--title",
        type=str,
        required=True,
        help="Issue title"
    )
    parser.add_argument(
        "--body",
        type=str,
        default=None,
        help="Issue body/description"
    )
    parser.add_argument(
        "--labels",
        type=str,
        default=None,
        help="Comma-separated list of labels"
    )
    parser.add_argument(
        "--assignees",
        type=str,
        default=None,
        help="Comma-separated list of assignees"
    )

    args = parser.parse_args()

    labels = args.labels.split(",") if args.labels else None
    assignees = args.assignees.split(",") if args.assignees else None

    try:
        service = GitHubService()
        issue = service.create_issue(
            repo_full_name=args.repo,
            title=args.title,
            body=args.body,
            labels=labels,
            assignees=assignees
        )
        print(json.dumps(issue.model_dump(), indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
