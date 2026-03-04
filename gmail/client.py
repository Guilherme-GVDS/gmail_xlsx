"""Gmail API client factory."""

from __future__ import annotations

from pathlib import Path

from googleapiclient.discovery import build

from gmail.auth import get_credentials


def build_gmail_client(root_dir: Path):
    """Build and return Gmail API service client."""
    credentials = get_credentials(root_dir)
    return build('gmail', 'v1', credentials=credentials)

