#!/usr/bin/env python3
"""CLI script to list GitHub branches."""

import argparse
import json
import sys

from github_service import GitHubService


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="List branches for a GitHub repository"
    )
    parser.add_argument(
        "--repo",
        type=str,
        required=True,
        help="Repository full name (owner/repo)"
    )

    args = parser.parse_args()

    try:
        service = GitHubService()
        branches = service.get_branches(repo_full_name=args.repo)
        print(json.dumps([branch.model_dump() for branch in branches], indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
