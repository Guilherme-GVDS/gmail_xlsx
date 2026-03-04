"""Centralized logger setup."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


LOG_FORMAT = '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
LOGGER_NAME = 'gmail_xlsx_sync'


def setup_logger(log_file: Path) -> logging.Logger:
    """Create and configure project logger.

    Args:
        log_file: Full path to the log file.

    Returns:
        Configured application logger.
    """
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if logger.handlers:
        return logger

    log_file.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(LOG_FORMAT)

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding='utf-8',
    )
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Return a child logger from the project root logger.

    Args:
        name: Child logger suffix.

    Returns:
        Logger instance scoped under `gmail_xlsx_sync`.
    """
    return logging.getLogger(f'{LOGGER_NAME}.{name}')
