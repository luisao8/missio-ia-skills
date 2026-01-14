"""
Trello API Service class for interacting with Trello REST API.
"""

import os
from typing import Any

import requests
from dotenv import load_dotenv


class TrelloService:
    """Service class for Trello API operations."""

    BASE_URL = "https://api.trello.com/1"

    def __init__(self) -> None:
        """Initialize TrelloService with API credentials from environment."""
        load_dotenv()

        self.api_key = os.getenv("TRELLO_API_KEY")
        self.token = os.getenv("TRELLO_TOKEN")

        if not self.api_key or not self.token:
            raise ValueError(
                "TRELLO_API_KEY and TRELLO_TOKEN must be set in environment or .env file"
            )

    def _request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """Make an authenticated request to Trello API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (e.g., /members/me/boards)
            params: Query parameters
            data: Request body data

        Returns:
            JSON response from API

        Raises:
            requests.HTTPError: If request fails
        """
        url = f"{self.BASE_URL}{endpoint}"

        # Add authentication to params
        auth_params = {"key": self.api_key, "token": self.token}
        if params:
            auth_params.update(params)

        response = requests.request(
            method=method,
            url=url,
            params=auth_params,
            json=data,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def get_boards(self) -> list[dict[str, Any]]:
        """Get all boards for the authenticated user.

        Returns:
            List of board objects
        """
        return self._request("GET", "/members/me/boards")  # type: ignore[return-value]

    def get_lists(self, board_id: str) -> list[dict[str, Any]]:
        """Get all lists in a board.

        Args:
            board_id: Trello board ID

        Returns:
            List of list objects
        """
        return self._request("GET", f"/boards/{board_id}/lists")  # type: ignore[return-value]

    def get_cards(
        self, list_id: str | None = None, board_id: str | None = None
    ) -> list[dict[str, Any]]:
        """Get cards from a list or board.

        Args:
            list_id: Trello list ID (optional)
            board_id: Trello board ID (optional)

        Returns:
            List of card objects

        Raises:
            ValueError: If neither list_id nor board_id is provided
        """
        if list_id:
            return self._request("GET", f"/lists/{list_id}/cards")  # type: ignore[return-value]
        elif board_id:
            return self._request("GET", f"/boards/{board_id}/cards")  # type: ignore[return-value]
        else:
            raise ValueError("Either list_id or board_id must be provided")

    def get_card(self, card_id: str) -> dict[str, Any]:
        """Get a single card by ID.

        Args:
            card_id: Trello card ID

        Returns:
            Card object with full details
        """
        return self._request(  # type: ignore[return-value]
            "GET",
            f"/cards/{card_id}",
            params={"members": "true", "labels": "true", "attachments": "true"},
        )

    def create_card(
        self,
        list_id: str,
        name: str,
        desc: str | None = None,
        due: str | None = None,
        labels: list[str] | None = None,
    ) -> dict[str, Any]:
        """Create a new card in a list.

        Args:
            list_id: Target list ID
            name: Card name
            desc: Card description (optional)
            due: Due date in ISO format (optional)
            labels: List of label IDs (optional)

        Returns:
            Created card object
        """
        params: dict[str, Any] = {"idList": list_id, "name": name}

        if desc:
            params["desc"] = desc
        if due:
            params["due"] = due
        if labels:
            params["idLabels"] = ",".join(labels)

        return self._request("POST", "/cards", params=params)  # type: ignore[return-value]

    def update_card(self, card_id: str, **kwargs: Any) -> dict[str, Any]:
        """Update a card's properties.

        Args:
            card_id: Trello card ID
            **kwargs: Card properties to update (name, desc, due, closed, etc.)

        Returns:
            Updated card object
        """
        return self._request("PUT", f"/cards/{card_id}", params=kwargs)  # type: ignore[return-value]

    def move_card(self, card_id: str, list_id: str) -> dict[str, Any]:
        """Move a card to a different list.

        Args:
            card_id: Trello card ID
            list_id: Target list ID

        Returns:
            Updated card object
        """
        return self._request("PUT", f"/cards/{card_id}", params={"idList": list_id})  # type: ignore[return-value]

    def add_comment(self, card_id: str, text: str) -> dict[str, Any]:
        """Add a comment to a card.

        Args:
            card_id: Trello card ID
            text: Comment text

        Returns:
            Created comment object
        """
        return self._request(  # type: ignore[return-value]
            "POST", f"/cards/{card_id}/actions/comments", params={"text": text}
        )

    def add_label(self, card_id: str, label_id: str) -> dict[str, Any]:
        """Add a label to a card.

        Args:
            card_id: Trello card ID
            label_id: Label ID to add

        Returns:
            List of label IDs on the card
        """
        return self._request(  # type: ignore[return-value]
            "POST", f"/cards/{card_id}/idLabels", params={"value": label_id}
        )

    def archive_card(self, card_id: str) -> dict[str, Any]:
        """Archive (close) a card.

        Args:
            card_id: Trello card ID

        Returns:
            Updated card object
        """
        return self._request("PUT", f"/cards/{card_id}", params={"closed": "true"})  # type: ignore[return-value]
