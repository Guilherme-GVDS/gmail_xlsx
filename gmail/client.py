"""Gmail API client factory."""

from __future__ import annotations

from pathlib import Path

from googleapiclient.discovery import build

from core.logger import get_logger
from gmail.auth import get_credentials

logger = get_logger('gmail.client')


def build_gmail_client(root_dir: Path):
    """Build and return Gmail API service client.

    Args:
        root_dir: Project root path.

    Returns:
        Gmail API service object.

    Raises:
        Exception: Re-raises any Gmail client creation error.
    """
    try:
        credentials = get_credentials(root_dir)
        return build('gmail', 'v1', credentials=credentials)
    except Exception as exc:
        logger.error('Failed to build Gmail client: %s', exc)
        raise
