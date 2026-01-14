#!/usr/bin/env python3
"""CLI script to merge a GitHub pull request."""

import argparse
import json
import sys

from github_service import GitHubService


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Merge a pull request in a GitHub repository"
    )
    parser.add_argument(
        "--repo",
        type=str,
        required=True,
        help="Repository full name (owner/repo)"
    )
    parser.add_argument(
        "--pr-number",
        type=int,
        required=True,
        help="Pull request number to merge"
    )
    parser.add_argument(
        "--merge-method",
        type=str,
        choices=["merge", "squash", "rebase"],
        default="merge",
        help="Merge method (default: merge)"
    )

    args = parser.parse_args()

    try:
        service = GitHubService()
        result = service.merge_pr(
            repo_full_name=args.repo,
            pr_number=args.pr_number,
            merge_method=args.merge_method
        )
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
