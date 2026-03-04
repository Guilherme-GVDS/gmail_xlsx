"""Tests for spreadsheet.merger module."""

from __future__ import annotations

import pandas as pd

from spreadsheet.merger import merge_data


def test_merge_data_appends_rows() -> None:
    """Append new rows to the base DataFrame."""
    base_df = pd.DataFrame({'id': [1, 2], 'name': ['a', 'b']})
    new_df = pd.DataFrame({'id': [3], 'name': ['c']})

    merged = merge_data(base_df, new_df)

    assert len(merged) == 3
    assert merged.to_dict(orient='records') == [
        {'id': 1, 'name': 'a'},
        {'id': 2, 'name': 'b'},
        {'id': 3, 'name': 'c'},
    ]
