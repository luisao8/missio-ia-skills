#!/usr/bin/env python3
"""
Google Meet API Service - Handles authentication and API operations.
"""

import json
import os
import pickle
from pathlib import Path
from typing import Any, Dict, List, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class MeetService:
    """Service class for Google Meet API operations."""

    SCOPES = [
        'https://www.googleapis.com/auth/meetings.space.created',
        'https://www.googleapis.com/auth/meetings.space.readonly',
    ]

    # Default paths relative to project root
    DEFAULT_CREDS_PATH = 'MCP_servers/google-credentials/credentials.json'
    DEFAULT_TOKEN_PATH = 'MCP_servers/google-credentials/token_meet.pickle'

    def __init__(
        self,
        creds_file_path: Optional[str] = None,
        token_path: Optional[str] = None
    ):
        """
        Initialize MeetService with authentication.

        Args:
            creds_file_path: Path to OAuth credentials JSON file.
            token_path: Path to store/retrieve pickle token.
        """
        # Find project root (go up from scripts directory)
        project_root = Path(__file__).parent.parent.parent.parent.parent

        self.creds_file_path = creds_file_path or str(
            project_root / self.DEFAULT_CREDS_PATH
        )
        self.token_path = token_path or str(
            project_root / self.DEFAULT_TOKEN_PATH
        )

        self._credentials: Optional[Credentials] = None
        self._service: Optional[Any] = None

    def _get_credentials(self) -> Credentials:
        """Get or refresh Google API credentials using pickle cache."""
        if self._credentials and self._credentials.valid:
            return self._credentials

        creds = None

        # Load from pickle if exists
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token_file:
                creds = pickle.load(token_file)

        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.creds_file_path):
                    raise FileNotFoundError(
                        f"Credentials file not found: {self.creds_file_path}"
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.creds_file_path, self.SCOPES
                )
                creds = flow.run_local_server(
                    port=0,
                    prompt='select_account',
                    success_message='Authentication successful! You can close this window.'
                )

            # Save to pickle
            with open(self.token_path, 'wb') as token_file:
                pickle.dump(creds, token_file)

        self._credentials = creds
        return creds

    def _get_service(self) -> Any:
        """Get or create Google Meet API service."""
        if self._service:
            return self._service

        try:
            creds = self._get_credentials()
            self._service = build('meet', 'v2', credentials=creds)
            return self._service
        except HttpError as error:
            raise RuntimeError(f"Failed to build Meet service: {error}")

    def create_space(self, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a new Google Meet space.

        Args:
            config: Optional configuration for the space.

        Returns:
            Dictionary with name, meetingUri, and meetingCode.
        """
        try:
            service = self._get_service()

            body = {}
            if config:
                body['config'] = config
            else:
                # Default: enable auto-transcription
                body['config'] = {
                    'artifactConfig': {
                        'transcriptionConfig': {
                            'autoTranscriptionGeneration': 'ON'
                        }
                    }
                }

            space = service.spaces().create(body=body).execute()

            return {
                'name': space.get('name', ''),
                'meetingUri': space.get('meetingUri', ''),
                'meetingCode': space.get('meetingCode', ''),
            }
        except HttpError as error:
            return {'error': f"Failed to create space: {error}"}
        except Exception as e:
            return {'error': str(e)}

    def get_space(self, space_name: str) -> Dict[str, Any]:
        """
        Get information about a meeting space.

        Args:
            space_name: The space identifier (e.g., "spaces/abc123").

        Returns:
            Dictionary with space details.
        """
        try:
            service = self._get_service()
            space = service.spaces().get(name=space_name).execute()

            return {
                'name': space.get('name', ''),
                'meetingUri': space.get('meetingUri', ''),
                'meetingCode': space.get('meetingCode', ''),
                'config': space.get('config', {}),
            }
        except HttpError as error:
            return {'error': f"Failed to get space: {error}"}
        except Exception as e:
            return {'error': str(e)}

    def end_active_conference(self, space_name: str) -> Dict[str, Any]:
        """
        End an active conference in a space.

        Args:
            space_name: The space identifier (e.g., "spaces/abc123").

        Returns:
            Dictionary with result or error.
        """
        try:
            service = self._get_service()

            # First, get the active conference for this space
            # We need to find conference records for this space
            response = service.conferenceRecords().list(
                filter=f'space="{space_name}"'
            ).execute()

            records = response.get('conferenceRecords', [])

            # Find active conference (no endTime)
            active_conference = None
            for record in records:
                if not record.get('endTime'):
                    active_conference = record
                    break

            if not active_conference:
                return {'error': 'No active conference found in this space'}

            conference_name = active_conference.get('name', '')

            # End the active conference
            service.spaces().endActiveConference(name=space_name).execute()

            return {
                'success': True,
                'message': f'Conference ended: {conference_name}',
            }
        except HttpError as error:
            error_str = str(error)
            if '404' in error_str:
                return {'error': 'Space not found or no active conference'}
            return {'error': f"Failed to end conference: {error}"}
        except Exception as e:
            return {'error': str(e)}

    def list_recordings(self, space_name: str) -> Dict[str, Any]:
        """
        List recordings for a meeting space.

        Args:
            space_name: The space identifier (e.g., "spaces/abc123").

        Returns:
            Dictionary with recordings list.
        """
        try:
            service = self._get_service()

            # Get conference records for this space
            response = service.conferenceRecords().list(
                filter=f'space="{space_name}"'
            ).execute()

            records = response.get('conferenceRecords', [])

            all_recordings: List[Dict[str, Any]] = []

            for record in records:
                conference_name = record.get('name', '')

                # Get recordings for this conference
                try:
                    recordings_response = service.conferenceRecords().recordings().list(
                        parent=conference_name
                    ).execute()

                    recordings = recordings_response.get('recordings', [])

                    for rec in recordings:
                        all_recordings.append({
                            'name': rec.get('name', ''),
                            'startTime': rec.get('startTime', ''),
                            'endTime': rec.get('endTime', ''),
                            'state': rec.get('state', ''),
                            'driveDestination': rec.get('driveDestination', {}),
                        })
                except HttpError:
                    # Conference may not have recordings
                    continue

            return {'recordings': all_recordings}
        except HttpError as error:
            return {'error': f"Failed to list recordings: {error}"}
        except Exception as e:
            return {'error': str(e)}

    def get_transcript(self, recording_name: str) -> Dict[str, Any]:
        """
        Get transcript for a recording.

        Note: This requires the recording to have an associated transcript.
        The recording_name should be in format "conferenceRecords/{id}/recordings/{id}"

        Args:
            recording_name: The recording identifier.

        Returns:
            Dictionary with transcript text or entries.
        """
        try:
            service = self._get_service()

            # Extract conference record parent from recording name
            # Format: conferenceRecords/{conf_id}/recordings/{rec_id}
            parts = recording_name.split('/')
            if len(parts) >= 2:
                conference_name = '/'.join(parts[:2])
            else:
                return {'error': 'Invalid recording name format'}

            # List transcripts for the conference
            transcripts_response = service.conferenceRecords().transcripts().list(
                parent=conference_name
            ).execute()

            transcripts = transcripts_response.get('transcripts', [])

            if not transcripts:
                return {
                    'error': 'No transcripts found for this conference',
                    'note': 'Transcription may not have been enabled for this meeting'
                }

            # Get entries from the first transcript
            transcript = transcripts[0]
            transcript_name = transcript.get('name', '')

            entries_response = service.conferenceRecords().transcripts().entries().list(
                parent=transcript_name,
                pageSize=100
            ).execute()

            entries = entries_response.get('transcriptEntries', [])

            # Format transcript entries
            formatted_entries = []
            for entry in entries:
                formatted_entries.append({
                    'startTime': entry.get('startTime', ''),
                    'endTime': entry.get('endTime', ''),
                    'text': entry.get('text', ''),
                    'participant': entry.get('participant', ''),
                })

            return {
                'transcriptName': transcript_name,
                'startTime': transcript.get('startTime', ''),
                'endTime': transcript.get('endTime', ''),
                'entries': formatted_entries,
            }
        except HttpError as error:
            return {'error': f"Failed to get transcript: {error}"}
        except Exception as e:
            return {'error': str(e)}


def _json_output(data: Dict[str, Any]) -> None:
    """Print data as formatted JSON."""
    print(json.dumps(data, indent=2, ensure_ascii=False))
