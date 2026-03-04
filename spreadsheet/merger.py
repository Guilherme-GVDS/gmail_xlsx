"""Spreadsheet merge and persistence helpers."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from core.logger import get_logger


logger = get_logger('spreadsheet.merger')


def load_base(base_path: str) -> pd.DataFrame:
    """Load base spreadsheet into a DataFrame.

    Args:
        base_path: Full path to base spreadsheet file.

    Returns:
        DataFrame loaded from base spreadsheet.
    """
    return pd.read_excel(base_path)


def merge_data(base_df: pd.DataFrame, new_df: pd.DataFrame) -> pd.DataFrame:
    """Append new rows to base DataFrame.

    Args:
        base_df: Current base DataFrame.
        new_df: New rows to append.

    Returns:
        Merged DataFrame.
    """
    rows_before = len(base_df)
    merged_df = pd.concat([base_df, new_df], ignore_index=True)
    rows_after = len(merged_df)
    logger.info(
        'Rows before merge=%d | after merge=%d',
        rows_before,
        rows_after,
    )
    return merged_df


def save_base(df, base_path: str) -> None:
    """Persist merged DataFrame into base spreadsheet.

    Args:
        df: Final merged DataFrame.
        base_path: Full destination path of base spreadsheet.

    Raises:
        OSError: If writing or replace operation fails.
    """
    destination = Path(base_path)
    temp_path = destination.with_suffix(f'{destination.suffix}.tmp')
    try:
        df.to_excel(temp_path, index=False, engine='openpyxl')
        temp_path.replace(destination)
    except OSError as exc:
        logger.error(
            'Failed to save base spreadsheet %s: %s',
            destination,
            exc,
        )
        if temp_path.exists():
            temp_path.unlink(missing_ok=True)
        raise
