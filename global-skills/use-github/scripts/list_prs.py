#!/usr/bin/env python3
"""CLI script to list GitHub pull requests."""

import argparse
import json
import sys

from github_service import GitHubService


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="List pull requests for a GitHub repository"
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
        help="PR state filter (default: open)"
    )

    args = parser.parse_args()

    try:
        service = GitHubService()
        prs = service.get_prs(repo_full_name=args.repo, state=args.state)
        print(json.dumps([pr.model_dump() for pr in prs], indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
