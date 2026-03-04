"""Attachment download helpers."""

from __future__ import annotations

import base64
from datetime import datetime
from pathlib import Path

from core.logger import get_logger


logger = get_logger('spreadsheet.downloader')


def _filename_with_timestamp(filename: str) -> str:
    """Add timestamp suffix to filename."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    path = Path(filename)
    return f'{path.stem}_{timestamp}{path.suffix}'


def _resolve_target_path(downloads_dir: Path, filename: str) -> Path:
    """Resolve destination path and avoid collisions."""
    candidate = downloads_dir / filename
    if not candidate.exists():
        return candidate
    return downloads_dir / _filename_with_timestamp(filename)


def download_attachment(
    service,
    email_id: str,
    attachment_id: str,
    filename: str,
    downloads_dir: Path,
) -> Path:
    """Download Gmail attachment payload and persist it.

    Args:
        service: Gmail API service object.
        email_id: Gmail message ID.
        attachment_id: Attachment ID from message payload.
        filename: Original attachment filename.
        downloads_dir: Destination directory for downloaded files.

    Returns:
        Full path to the saved file.

    Raises:
        OSError: If write operation fails.
    """
    downloads_dir.mkdir(parents=True, exist_ok=True)
    target = _resolve_target_path(downloads_dir, filename)

    try:
        response = service.users().messages().attachments().get(
            userId='me',
            messageId=email_id,
            id=attachment_id,
        ).execute()
        data = response.get('data', '')
        raw_bytes = base64.urlsafe_b64decode(data.encode('utf-8'))
        target.write_bytes(raw_bytes)
    except OSError as exc:
        logger.error(
            'I/O error downloading attachment filename=%s to %s: %s',
            filename,
            target,
            exc,
        )
        raise

    logger.info(
        'Attachment downloaded | filename=%s | size_bytes=%d | path=%s',
        target.name,
        len(raw_bytes),
        target,
    )

    return target
