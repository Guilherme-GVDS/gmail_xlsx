"""Spreadsheet merge and persistence helpers."""

from __future__ import annotations

import pandas as pd


def load_base(base_path: str):
    """Load base spreadsheet into DataFrame."""
    return pd.read_excel(base_path)


def merge_data(base_df, new_df):
    """Append new data rows to base DataFrame."""
    return pd.concat([base_df, new_df], ignore_index=True)


def save_base(df, base_path: str) -> None:
    """Persist merged DataFrame into base spreadsheet."""
    df.to_excel(base_path, index=False, engine='openpyxl')

