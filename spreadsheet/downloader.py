"""Attachment download helpers."""

from __future__ import annotations

import base64
from datetime import datetime
from pathlib import Path


def _safe_filename(filename: str) -> str:
    """Add timestamp suffix to avoid filename collisions."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    path = Path(filename)
    return f'{path.stem}_{timestamp}{path.suffix}'


def download_attachment(
    service,
    email_id: str,
    attachment_id: str,
    filename: str,
    downloads_dir: Path,
) -> Path:
    """Download Gmail attachment data and persist it in downloads dir."""
    downloads_dir.mkdir(parents=True, exist_ok=True)
    target = downloads_dir / _safe_filename(filename)

    response = service.users().messages().attachments().get(
        userId='me',
        messageId=email_id,
        id=attachment_id,
    ).execute()
    data = response.get('data', '')
    raw_bytes = base64.urlsafe_b64decode(data.encode('utf-8'))
    target.write_bytes(raw_bytes)

    return target

