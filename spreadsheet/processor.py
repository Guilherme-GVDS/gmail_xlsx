"""Spreadsheet read and filtering helpers."""

from __future__ import annotations

import pandas as pd


def read_xlsx(filepath: str):
    """Read xlsx file into DataFrame."""
    return pd.read_excel(filepath)


def filter_columns(df_source, base_columns: list[str]):
    """Filter source DataFrame to columns present in base columns list."""
    common_columns = [col for col in df_source.columns if col in base_columns]
    if not common_columns:
        return None

    return df_source[common_columns]

