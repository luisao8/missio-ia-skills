#!/usr/bin/env python3
"""CLI script to create a GitHub pull request."""

import argparse
import json
import sys

from github_service import GitHubService


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Create a pull request in a GitHub repository"
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
        help="Pull request title"
    )
    parser.add_argument(
        "--head",
        type=str,
        required=True,
        help="Branch with changes"
    )
    parser.add_argument(
        "--base",
        type=str,
        required=True,
        help="Branch to merge into"
    )
    parser.add_argument(
        "--body",
        type=str,
        default=None,
        help="Pull request description"
    )

    args = parser.parse_args()

    try:
        service = GitHubService()
        pr = service.create_pr(
            repo_full_name=args.repo,
            title=args.title,
            head=args.head,
            base=args.base,
            body=args.body
        )
        print(json.dumps(pr.model_dump(), indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
