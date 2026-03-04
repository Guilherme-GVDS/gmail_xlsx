"""Email fetching and processed-id controls."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

from core.logger import get_logger


logger = get_logger('gmail.fetcher')


def get_processed_ids(file_path: Path) -> set[str]:
    """Load processed Gmail message IDs into a set.

    Args:
        file_path: Path to processed IDs file.

    Returns:
        Set with processed message IDs.
    """
    if not file_path.exists():
        return set()

    return {
        line.strip()
        for line in file_path.read_text(encoding='utf-8').splitlines()
        if line.strip()
    }


def mark_as_processed(file_path: Path, email_id: str) -> None:
    """Append a processed Gmail message ID to control file.

    Args:
        file_path: Path to processed IDs file.
        email_id: Gmail message ID to persist.
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open('a', encoding='utf-8') as file:
        file.write(f'{email_id}\n')


def build_query(subject: str) -> str:
    """Build Gmail query for the subject within the last 24 hours.

    Args:
        subject: Subject text to filter.

    Returns:
        Query in `subject:{subject} after:{timestamp}` format.
    """
    timestamp = int((datetime.now() - timedelta(hours=24)).timestamp())
    return f'subject:{subject} after:{timestamp}'


def fetch_emails(service, query: str) -> list[dict]:
    """Fetch all messages matching a Gmail query.

    Args:
        service: Gmail API service object.
        query: Gmail search query.

    Returns:
        List of message dictionaries returned by Gmail API.
    """
    user_id = 'me'
    page_token = None
    messages = []

    while True:
        response = service.users().messages().list(
            userId=user_id,
            q=query,
            pageToken=page_token,
        ).execute()
        messages.extend(response.get('messages', []))
        page_token = response.get('nextPageToken')
        if not page_token:
            break

    return messages


def fetch_emails_by_subject(
    service,
    subject: str,
    processed_ids: set[str],
) -> list[dict]:
    """Fetch all unprocessed messages matching subject query.

    Args:
        service: Gmail API service object.
        subject: Subject text to filter.
        processed_ids: Set of already processed message IDs.

    Returns:
        Unprocessed messages matching the subject query.
    """
    query = build_query(subject)
    messages = fetch_emails(service, query)
    to_process = [
        msg for msg in messages if msg.get('id') not in processed_ids
    ]

    logger.info(
        'Messages found in last 24h=%d | to_process=%d',
        len(messages),
        len(to_process),
    )
    return to_process


def get_attachments(service, email_id: str) -> list[dict]:
    """Return `.xlsx` attachment metadata for a message.

    Args:
        service: Gmail API service object.
        email_id: Gmail message ID.

    Returns:
        List of dictionaries with `filename` and `attachment_id`.
    """
    message = service.users().messages().get(
        userId='me',
        id=email_id,
    ).execute()
    payload = message.get('payload', {})
    attachments = []

    parts = payload.get('parts', [])
    for part in parts:
        filename = part.get('filename', '')
        body = part.get('body', {})
        attachment_id = body.get('attachmentId')

        if filename.lower().endswith('.xlsx') and attachment_id:
            attachments.append(
                {
                    'filename': filename,
                    'attachment_id': attachment_id,
                }
            )

    return attachments


def get_xlsx_attachments(service, email_id: str) -> list[dict]:
    """Backward-compatible alias for xlsx attachment collection.

    Args:
        service: Gmail API service object.
        email_id: Gmail message ID.

    Returns:
        List of `.xlsx` attachment metadata.
    """
    return get_attachments(service, email_id)
