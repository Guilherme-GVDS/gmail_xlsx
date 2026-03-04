"""Tests for spreadsheet.processor module."""

from __future__ import annotations

import pandas as pd

from spreadsheet.processor import filter_columns


def test_filter_columns_returns_only_base_columns() -> None:
    """Return DataFrame with only columns present in base."""
    source_df = pd.DataFrame(
        {
            'extra': [1, 2],
            'name': ['a', 'b'],
            'value': [10, 20],
        }
    )
    base_columns = ['name', 'value']

    filtered = filter_columns(source_df, base_columns)

    assert filtered is not None
    assert list(filtered.columns) == ['name', 'value']
    assert filtered.to_dict(orient='records') == [
        {'name': 'a', 'value': 10},
        {'name': 'b', 'value': 20},
    ]


def test_filter_columns_returns_none_when_no_common_columns() -> None:
    """Return None when source and base have no common columns."""
    source_df = pd.DataFrame({'foo': [1], 'bar': [2]})
    base_columns = ['name', 'value']

    filtered = filter_columns(source_df, base_columns)

    assert filtered is None
