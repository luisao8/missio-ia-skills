#!/usr/bin/env python3
"""CLI script to get GitHub file content."""

import argparse
import json
import sys

from github_service import GitHubService


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Get file content from a GitHub repository"
    )
    parser.add_argument(
        "--repo",
        type=str,
        required=True,
        help="Repository full name (owner/repo)"
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="File path in the repository"
    )
    parser.add_argument(
        "--ref",
        type=str,
        default=None,
        help="Branch, tag, or commit SHA (optional)"
    )

    args = parser.parse_args()

    try:
        service = GitHubService()
        file_content = service.get_file(
            repo_full_name=args.repo,
            path=args.path,
            ref=args.ref
        )
        print(json.dumps(file_content.model_dump(), indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
