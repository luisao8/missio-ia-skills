# Google Meet Skill - Usage Examples

## Example 1: Create a Quick Meeting

Create a new Google Meet space and get the meeting link to share.

```bash
# Simple meeting creation
python .claude/skills/use-meet/scripts/create_space.py
```

**Expected Output:**
```json
{
  "name": "spaces/abc123xyz",
  "meetingUri": "https://meet.google.com/abc-defg-hij",
  "meetingCode": "abc-defg-hij"
}
```

**Use Case:** When a user needs to quickly start a video call and share the link with participants.

---

## Example 2: Create Meeting for Calendar Event

Create a meeting with custom configuration for a scheduled event.

```bash
# Create with auto-transcription enabled (default)
python .claude/skills/use-meet/scripts/create_space.py

# Create with custom config
python .claude/skills/use-meet/scripts/create_space.py --config '{"accessType": "TRUSTED"}'
```

**Use Case:** When scheduling a meeting that will be added to a Google Calendar event.

**Integration with Calendar:**
```python
from service import MeetService

# Create meeting space
service = MeetService()
result = service.create_space()

# Use the meetingUri when creating calendar events
meeting_link = result.get('meetingUri')
# Add meeting_link to your calendar event creation
```

---

## Example 3: Get Transcript from Last Meeting

Retrieve the transcript from a recent meeting for notes or follow-up.

```bash
# Step 1: List recordings from a space to find the conference ID
python .claude/skills/use-meet/scripts/list_recordings.py --space-name "spaces/abc123"

# Step 2: Get transcript using the recording name from step 1
python .claude/skills/use-meet/scripts/get_transcript.py \
  --recording-name "conferenceRecords/xyz789/recordings/rec123" \
  --format readable
```

**Expected Output (readable format):**
```
============================================================
MEETING TRANSCRIPT
============================================================
Transcript: conferenceRecords/xyz789/transcripts/t123
Start: 2024-01-15T10:00:00Z
End: 2024-01-15T11:00:00Z
------------------------------------------------------------

[10:00:15] participant123:
  Hello everyone, let's get started.

[10:00:30] participant456:
  Thanks for joining. Today we'll discuss...

============================================================
Total entries: 45
============================================================
```

**Use Case:** Creating meeting notes, summarizing discussions, or documenting decisions.

---

## Example 4: List All Recordings from a Meeting Space

Get a complete list of all recordings associated with a meeting space.

```bash
python .claude/skills/use-meet/scripts/list_recordings.py --space-name "spaces/abc123"
```

**Expected Output:**
```json
{
  "recordings": [
    {
      "name": "conferenceRecords/conf1/recordings/rec1",
      "startTime": "2024-01-15T10:00:00Z",
      "endTime": "2024-01-15T11:00:00Z",
      "state": "ENDED",
      "driveDestination": {
        "file": "https://drive.google.com/file/d/xxx",
        "exportUri": "https://..."
      }
    },
    {
      "name": "conferenceRecords/conf2/recordings/rec2",
      "startTime": "2024-01-16T14:00:00Z",
      "endTime": "2024-01-16T15:30:00Z",
      "state": "ENDED",
      "driveDestination": {}
    }
  ]
}
```

**Use Case:** Archiving meeting recordings, finding specific meeting content, or auditing meeting history.

---

## Example 5: Check Meeting Space Status

Get information about an existing meeting space.

```bash
python .claude/skills/use-meet/scripts/get_space.py --space-name "spaces/abc123"
```

**Expected Output:**
```json
{
  "name": "spaces/abc123",
  "meetingUri": "https://meet.google.com/abc-defg-hij",
  "meetingCode": "abc-defg-hij",
  "config": {
    "accessType": "OPEN",
    "artifactConfig": {
      "transcriptionConfig": {
        "autoTranscriptionGeneration": "ON"
      }
    }
  }
}
```

---

## Example 6: End an Active Meeting

Terminate an ongoing conference in a space.

```bash
python .claude/skills/use-meet/scripts/end_meeting.py --space-name "spaces/abc123"
```

**Expected Output (success):**
```json
{
  "success": true,
  "message": "Conference ended: conferenceRecords/xyz789"
}
```

**Expected Output (no active meeting):**
```json
{
  "error": "No active conference found in this space"
}
```

---

## Python API Usage

For programmatic access, import and use MeetService directly:

```python
from .claude.skills.use_meet.scripts.service import MeetService

# Initialize service (uses default credential paths)
service = MeetService()

# Create a meeting
result = service.create_space()
print(f"Join at: {result['meetingUri']}")

# Get space info
info = service.get_space("spaces/abc123")

# List recordings
recordings = service.list_recordings("spaces/abc123")

# Get transcript
transcript = service.get_transcript("conferenceRecords/xyz/recordings/abc")
```
