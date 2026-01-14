#!/usr/bin/env python3
"""CLI script to search GitHub code."""

import argparse
import json
import sys

from github_service import GitHubService


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Search for code in GitHub repositories"
    )
    parser.add_argument(
        "--query",
        type=str,
        required=True,
        help="Search query"
    )
    parser.add_argument(
        "--repo",
        type=str,
        default=None,
        help="Limit search to specific repository (owner/repo)"
    )

    args = parser.parse_args()

    try:
        service = GitHubService()
        results = service.search_code(query=args.query, repo_full_name=args.repo)
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
