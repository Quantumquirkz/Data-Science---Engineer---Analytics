"""Data quality helpers for repository-wide checks."""

from __future__ import annotations

import pandas as pd


def summarize_missingness(frame: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "column": frame.columns,
            "missing_count": [int(frame[col].isna().sum()) for col in frame.columns],
            "missing_rate": [float(frame[col].isna().mean()) for col in frame.columns],
        }
    )
