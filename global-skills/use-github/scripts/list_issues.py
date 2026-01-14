#!/usr/bin/env python3
"""CLI script to list GitHub issues."""

import argparse
import json
import sys

from github_service import GitHubService


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="List issues for a GitHub repository"
    )
    parser.add_argument(
        "--repo",
        type=str,
        required=True,
        help="Repository full name (owner/repo)"
    )
    parser.add_argument(
        "--state",
        type=str,
        choices=["open", "closed", "all"],
        default="open",
        help="Issue state filter (default: open)"
    )
    parser.add_argument(
        "--labels",
        type=str,
        default=None,
        help="Comma-separated list of labels to filter by"
    )

    args = parser.parse_args()

    labels = args.labels.split(",") if args.labels else None

    try:
        service = GitHubService()
        issues = service.get_issues(
            repo_full_name=args.repo,
            state=args.state,
            labels=labels
        )
        print(json.dumps([issue.model_dump() for issue in issues], indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
