"""OAuth2 authentication helpers for Gmail API."""

from __future__ import annotations

import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from core.logger import get_logger


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
logger = get_logger('gmail.auth')


def _resolve_token_path(root_dir: Path) -> Path:
    """Resolve token file path from env var or default project location."""
    token_env = os.getenv('GOOGLE_TOKEN_PATH', 'token.json').strip()
    token_candidate = Path(token_env) if token_env else Path('token.json')
    if token_candidate.is_absolute():
        return token_candidate
    return root_dir / token_candidate


def _resolve_credentials_path(root_dir: Path) -> Path | None:
    """Resolve OAuth credentials path with fallback for Google default filename."""
    credentials_env = os.getenv(
        'GOOGLE_CREDENTIALS_PATH',
        'credentials.json',
    ).strip()
    credentials_candidate = (
        Path(credentials_env) if credentials_env else Path('credentials.json')
    )
    credentials_path = (
        credentials_candidate
        if credentials_candidate.is_absolute()
        else root_dir / credentials_candidate
    )
    if credentials_path.exists():
        return credentials_path

    # Google often downloads files like `client_secret_<id>.json`.
    for file_path in root_dir.glob('client_secret*.json'):
        if file_path.is_file():
            logger.warning(
                'Using fallback OAuth credentials file: %s',
                file_path,
            )
            return file_path

    return None


def get_credentials(root_dir: Path) -> Credentials:
    """Load or create OAuth2 credentials for Gmail API access.

    Args:
        root_dir: Project root path containing credential/token files.

    Returns:
        Valid OAuth2 credentials for Gmail API.

    Raises:
        SystemExit: If OAuth credentials file is missing.
    """
    token_path = _resolve_token_path(root_dir)
    credentials_path = _resolve_credentials_path(root_dir)

    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    if not creds or not creds.valid:
        if not credentials_path:
            message = (
                'OAuth credentials file not found. '
                f'Checked GOOGLE_CREDENTIALS_PATH and default path '
                f'"{root_dir / "credentials.json"}". '
                'Save the Google OAuth Desktop App JSON as '
                '"credentials.json" in project root or set '
                'GOOGLE_CREDENTIALS_PATH in .env.'
            )
            logger.error(message)
            raise SystemExit(1) from FileNotFoundError(message)

        flow = InstalledAppFlow.from_client_secrets_file(
            str(credentials_path),
            SCOPES,
        )
        creds = flow.run_local_server(port=0)
        token_path.write_text(creds.to_json(), encoding='utf-8')

    return creds
