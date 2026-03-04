"""Application configuration loader."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT_DIR / '.env'

load_dotenv(ENV_PATH)

ASSUNTO = os.getenv('ASSUNTO', '').strip()
BASE_SPREADSHEET_PATH = Path(
    os.getenv('BASE_SPREADSHEET_PATH', 'core/base.xlsx')
)
DOWNLOADS_DIR = Path(os.getenv('DOWNLOADS_DIR', 'downloads'))
PROCESSED_IDS_FILE = Path(os.getenv('PROCESSED_IDS_FILE', 'processed_ids.txt'))
KEEP_DOWNLOADS = os.getenv('KEEP_DOWNLOADS', 'true').lower() == 'true'


def validate_config() -> None:
    """Validate required runtime configuration."""
    if not ASSUNTO:
        raise ValueError('ASSUNTO must not be empty.')

    base_path = ROOT_DIR / BASE_SPREADSHEET_PATH
    if not base_path.exists():
        raise FileNotFoundError(
            f'Base spreadsheet not found: {base_path}'
        )

