#!/usr/bin/env python3
"""CLI script to list GitHub repositories."""

import argparse
import json
import sys

from github_service import GitHubService


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="List GitHub repositories for a user"
    )
    parser.add_argument(
        "--user",
        type=str,
        default=None,
        help="Username to get repos for (default: authenticated user)"
    )
    parser.add_argument(
        "--type",
        type=str,
        choices=["all", "owner", "member"],
        default="all",
        help="Type of repos to return (default: all)"
    )

    args = parser.parse_args()

    try:
        service = GitHubService()
        repos = service.get_repos(user=args.user, repo_type=args.type)
        print(json.dumps([repo.model_dump() for repo in repos], indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
