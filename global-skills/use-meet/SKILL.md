---
name: use-meet
description: Interact with Google Meet API. Create meeting spaces, get meeting info, end meetings, list recordings, and get transcripts. Use when user mentions meet, reunión, videollamada, videoconference, meeting link, enlace meet.
version: 1.0.0
---

# Google Meet Skill

## Overview
This skill provides tools to interact with Google Meet API, allowing you to create and manage meeting spaces, access recordings, and retrieve transcripts.

**Keywords**: meet, reunión, videollamada, videoconference, meeting link, enlace meet, google meet, video call

## Quick Start

### Requirements
- Python 3.11+
- Google API credentials at `MCP_servers/google-credentials/credentials.json`
- Required scopes:
  - `https://www.googleapis.com/auth/meetings.space.created`
  - `https://www.googleapis.com/auth/meetings.space.readonly`

### Basic Usage
```bash
# Create a new meeting space
python .claude/skills/use-meet/scripts/create_space.py

# Get information about a meeting space
python .claude/skills/use-meet/scripts/get_space.py --space-name "spaces/abc123"

# End an active meeting
python .claude/skills/use-meet/scripts/end_meeting.py --space-name "spaces/abc123"
```

## Available Scripts

| Script | Description | Arguments |
|--------|-------------|-----------|
| `create_space.py` | Create a new Google Meet space | `--config` (optional): space type |
| `get_space.py` | Get info about a meeting space | `--space-name` (required) |
| `end_meeting.py` | End an active conference | `--space-name` (required) |
| `list_recordings.py` | List recordings for a space | `--space-name` (required) |
| `get_transcript.py` | Get transcript from recording | `--recording-name` (required) |

## Script Details

### create_space.py
Creates a new Google Meet space and returns the meeting URL.

**Output (JSON):**
```json
{
  "name": "spaces/abc123",
  "meetingUri": "https://meet.google.com/xxx-xxxx-xxx",
  "meetingCode": "xxx-xxxx-xxx"
}
```

### get_space.py
Retrieves information about an existing meeting space.

**Arguments:**
- `--space-name`: The space identifier (e.g., "spaces/abc123")

### end_meeting.py
Terminates an active conference in the specified space.

**Arguments:**
- `--space-name`: The space identifier

### list_recordings.py
Lists all recordings available for a meeting space.

**Output (JSON):**
```json
{
  "recordings": [
    {
      "name": "recordings/xyz789",
      "startTime": "2024-01-15T10:00:00Z",
      "endTime": "2024-01-15T11:00:00Z"
    }
  ]
}
```

### get_transcript.py
Retrieves the transcript for a specific recording.

**Arguments:**
- `--recording-name`: The recording identifier

## Examples

### Create a quick meeting
```bash
# Create a meeting and share the link
python .claude/skills/use-meet/scripts/create_space.py
# Returns: {"meetingUri": "https://meet.google.com/xxx-xxxx-xxx", ...}
```

### Check meeting status
```bash
# Get details of an existing space
python .claude/skills/use-meet/scripts/get_space.py --space-name "spaces/abc123"
```

### Get recordings from a meeting
```bash
# List all recordings
python .claude/skills/use-meet/scripts/list_recordings.py --space-name "spaces/abc123"

# Get transcript from a specific recording
python .claude/skills/use-meet/scripts/get_transcript.py --recording-name "recordings/xyz789"
```

### End a meeting remotely
```bash
# Terminate an active conference
python .claude/skills/use-meet/scripts/end_meeting.py --space-name "spaces/abc123"
```

## Error Handling

All scripts return JSON with an `error` key when something goes wrong:

```json
{
  "error": "Authentication failed. Please check your credentials."
}
```

Common errors:
- **Authentication failed**: Check `credentials.json` exists and is valid
- **Space not found**: Verify the space name is correct
- **No active conference**: The meeting has already ended
- **Permission denied**: Verify your OAuth scopes include required permissions

## Authentication

On first use, the skill will open a browser window for OAuth authentication. The token is cached at `MCP_servers/google-credentials/token_meet.pickle` for future requests.

## Instructions

When the user wants to work with Google Meet:

1. **Create a meeting**: Use `create_space.py` to generate a new meeting link
2. **Share meeting info**: Extract `meetingUri` from the response
3. **Manage meetings**: Use `get_space.py` or `end_meeting.py` as needed
4. **Access recordings**: Use `list_recordings.py` then `get_transcript.py`

Always return the meeting URL prominently when creating a space, as this is typically what users need to share with participants.
