"""OAuth2 authentication helpers for Gmail API."""

from __future__ import annotations

from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_credentials(root_dir: Path) -> Credentials:
    """Load or create OAuth2 credentials for Gmail API access."""
    token_path = root_dir / 'token.json'
    credentials_path = root_dir / 'credentials.json'

    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    if not creds or not creds.valid:
        if not credentials_path.exists():
            raise FileNotFoundError(
                f'credentials.json not found: {credentials_path}'
            )

        flow = InstalledAppFlow.from_client_secrets_file(
            str(credentials_path),
            SCOPES,
        )
        creds = flow.run_local_server(port=0)
        token_path.write_text(creds.to_json(), encoding='utf-8')

    return creds

