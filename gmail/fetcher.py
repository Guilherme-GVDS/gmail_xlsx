"""Email fetching and processed-id controls."""

from __future__ import annotations

from pathlib import Path


def get_processed_ids(file_path: Path) -> set[str]:
    """Load processed Gmail message ids into a set."""
    if not file_path.exists():
        return set()

    return {
        line.strip()
        for line in file_path.read_text(encoding='utf-8').splitlines()
        if line.strip()
    }


def mark_as_processed(file_path: Path, email_id: str) -> None:
    """Append a processed Gmail message id to control file."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open('a', encoding='utf-8') as file:
        file.write(f'{email_id}\n')


def fetch_emails_by_subject(service, subject: str, processed_ids: set[str]) -> list[dict]:
    """Fetch all unprocessed messages matching subject query."""
    query = f'subject:{subject}'
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

    return [msg for msg in messages if msg.get('id') not in processed_ids]


def get_xlsx_attachments(service, email_id: str) -> list[dict]:
    """Return xlsx attachment metadata from a message payload."""
    message = service.users().messages().get(userId='me', id=email_id).execute()
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

