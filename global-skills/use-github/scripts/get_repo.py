#!/usr/bin/env python3
"""CLI script to get GitHub repository info."""

import argparse
import json
import sys

from github_service import GitHubService


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Get info for a GitHub repository"
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
        repo = service.get_repo(args.repo)
        print(json.dumps(repo.model_dump(), indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
