---
name: use-trello
description: Interact with Trello API to manage boards, lists, and cards
---

# Trello CLI Skill

A collection of Python CLI scripts for interacting with Trello API. Use these scripts to manage boards, lists, and cards directly from the command line.

## When to Use

Use this skill when you need to:
- List Trello boards, lists, or cards
- Create new cards in Trello
- Update existing cards (name, description, due date)
- Move cards between lists
- Add comments or labels to cards
- Archive cards

## Prerequisites

### Environment Variables

Set these environment variables (or add to `.env` file):

```bash
TRELLO_API_KEY=your_api_key
TRELLO_TOKEN=your_token
```

Get your API key and token from: https://trello.com/app-key

### Python Dependencies

```bash
pip install requests pydantic python-dotenv
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

## Available Scripts

All scripts output JSON and are located in the `scripts/` directory.

### list_boards.py - List all boards

List all Trello boards for the authenticated user.

```bash
python scripts/list_boards.py
```

### list_lists.py - List lists in a board

List all lists in a specific board.

```bash
python scripts/list_lists.py --board-id <board_id>
```

### list_cards.py - List cards

List cards from a list or board.

```bash
# List cards from a specific list
python scripts/list_cards.py --list-id <list_id>

# List all cards from a board
python scripts/list_cards.py --board-id <board_id>
```

### get_card.py - Get card details

Get full details of a specific card.

```bash
python scripts/get_card.py --card-id <card_id>
```

### create_card.py - Create a new card

Create a new card in a list.

```bash
# Basic usage
python scripts/create_card.py --list-id <list_id> --name "Card Name"

# With all options
python scripts/create_card.py --list-id <list_id> --name "Card Name" --desc "Description" --due "2024-12-31" --labels "label1_id,label2_id"
```

### update_card.py - Update a card

Update an existing card's properties.

```bash
# Update name
python scripts/update_card.py --card-id <card_id> --name "New Name"

# Update multiple fields
python scripts/update_card.py --card-id <card_id> --name "New Name" --desc "New description" --due "2024-12-31"

# Archive a card
python scripts/update_card.py --card-id <card_id> --closed true
```

### move_card.py - Move a card

Move a card to a different list.

```bash
python scripts/move_card.py --card-id <card_id> --list-id <target_list_id>
```

### add_comment.py - Add a comment

Add a comment to a card.

```bash
python scripts/add_comment.py --card-id <card_id> --text "Your comment here"
```

### add_label.py - Add a label

Add a label to a card.

```bash
python scripts/add_label.py --card-id <card_id> --label-id <label_id>
```

### archive_card.py - Archive a card

Archive (close) a card.

```bash
python scripts/archive_card.py --card-id <card_id>
```

## Error Handling

All scripts return JSON. On error, the output format is:

```json
{"error": "Error message here"}
```

## Examples

### Workflow: Create a task and move it through stages

```bash
# 1. List boards to find your board ID
python scripts/list_boards.py

# 2. List lists to find your "To Do" list ID
python scripts/list_lists.py --board-id abc123

# 3. Create a new card
python scripts/create_card.py --list-id xyz789 --name "New Feature" --desc "Implement the new feature"

# 4. Later, move it to "In Progress" list
python scripts/move_card.py --card-id card123 --list-id inprogress456

# 5. Add a comment with progress update
python scripts/add_comment.py --card-id card123 --text "Started implementation"

# 6. When done, move to "Done" list
python scripts/move_card.py --card-id card123 --list-id done789
```
