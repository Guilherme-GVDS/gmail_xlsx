"""Project entrypoint for Gmail XLSX sync."""

from __future__ import annotations

from pathlib import Path

from core import config
from core.logger import get_logger, setup_logger
from gmail.client import build_gmail_client
from gmail.fetcher import (
    fetch_emails_by_subject,
    get_attachments,
    get_processed_ids,
    mark_as_processed,
)
from spreadsheet.downloader import download_attachment
from spreadsheet.merger import load_base, merge_data, save_base
from spreadsheet.processor import filter_columns, read_xlsx


def run() -> int:
    """Run one full synchronization cycle.

    Returns:
        Process exit code (`0` for success, `1` for failure).
    """
    root_dir = Path(__file__).resolve().parent
    logger = setup_logger(root_dir / 'logs' / 'app.log')
    app_logger = get_logger('main')

    try:
        config.validate_config()
    except Exception as exc:
        app_logger.error('Invalid configuration: %s', exc)
        return 1

    try:
        service = build_gmail_client(root_dir)
    except Exception as exc:
        app_logger.error('Gmail client initialization failed: %s', exc)
        return 1

    processed_path = root_dir / config.PROCESSED_IDS_FILE
    base_path = root_dir / config.BASE_SPREADSHEET_PATH
    downloads_dir = root_dir / config.DOWNLOADS_DIR

    processed_ids = get_processed_ids(processed_path)
    messages = fetch_emails_by_subject(service, config.ASSUNTO, processed_ids)
    app_logger.info('Messages to process: %d', len(messages))

    total_processed = 0
    total_skipped = 0
    total_errors = 0

    for message in messages:
        email_id = message.get('id')
        if not email_id:
            total_skipped += 1
            continue

        try:
            attachments = get_attachments(service, email_id)
            if not attachments:
                app_logger.info(
                    'No xlsx attachments for message id=%s',
                    email_id,
                )
                mark_as_processed(processed_path, email_id)
                total_skipped += 1
                continue

            base_df = load_base(str(base_path))
            for attachment in attachments:
                filepath = download_attachment(
                    service=service,
                    email_id=email_id,
                    attachment_id=attachment['attachment_id'],
                    filename=attachment['filename'],
                    downloads_dir=downloads_dir,
                )

                source_df = read_xlsx(str(filepath))
                filtered_df = filter_columns(source_df, list(base_df.columns))
                if filtered_df is None:
                    app_logger.warning(
                        'No compatible columns for file: %s',
                        filepath.name,
                    )
                    continue

                base_df = merge_data(base_df, filtered_df)

                if not config.KEEP_DOWNLOADS:
                    filepath.unlink(missing_ok=True)
                    app_logger.info('Removed downloaded file: %s', filepath)

            save_base(base_df, str(base_path))
            mark_as_processed(processed_path, email_id)
            total_processed += 1
            app_logger.info('Processed message id=%s', email_id)
        except Exception as exc:
            total_errors += 1
            app_logger.error(
                'Error processing message id=%s: %s',
                email_id,
                exc,
            )

    logger.info(
        'Cycle summary | processed=%d | skipped=%d | errors=%d',
        total_processed,
        total_skipped,
        total_errors,
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(run())
