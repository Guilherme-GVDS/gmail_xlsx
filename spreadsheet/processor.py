"""Spreadsheet read and filtering helpers."""

from __future__ import annotations

import pandas as pd

from core.logger import get_logger


logger = get_logger('spreadsheet.processor')


def read_xlsx(filepath: str) -> pd.DataFrame:
    """Read an `.xlsx` file into a DataFrame.

    Args:
        filepath: Full path to the spreadsheet file.

    Returns:
        DataFrame with spreadsheet data.

    Raises:
        Exception: Re-raises read errors after logging.
    """
    try:
        return pd.read_excel(filepath)
    except Exception as exc:
        logger.error('Failed to read xlsx file %s: %s', filepath, exc)
        raise


def filter_columns(
    df_source: pd.DataFrame,
    base_columns: list[str],
) -> pd.DataFrame | None:
    """Keep only source columns that exist in base columns.

    Args:
        df_source: Source DataFrame loaded from attachment.
        base_columns: Ordered list of columns from base spreadsheet.

    Returns:
        Filtered DataFrame with common columns, or `None` when there are none.
    """
    source_columns = list(df_source.columns)
    common_columns = [col for col in base_columns if col in source_columns]
    ignored_columns = [
        col for col in source_columns if col not in base_columns
    ]

    logger.info('Base columns: %s', base_columns)
    logger.info('Source columns: %s', source_columns)
    logger.info('Ignored columns: %s', ignored_columns)

    if not common_columns:
        logger.warning('No common columns found between source and base.')
        return None

    return df_source[common_columns]
