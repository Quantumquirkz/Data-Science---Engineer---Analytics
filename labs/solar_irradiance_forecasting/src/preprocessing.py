from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(slots=True)
class PreprocessingConfig:
    forward_fill_limit_hours: int = 3
    clip_ghi_non_negative: bool = True


def preprocess_hourly_frame(
    frame: pd.DataFrame,
    config: PreprocessingConfig,
) -> pd.DataFrame:
    """Resample to hourly grid, light imputation, optional GHI clip."""
    out = frame.copy()
    if not isinstance(out.index, pd.DatetimeIndex):
        raise TypeError("Expected DatetimeIndex.")
    if out.index.tz is None:
        out.index = out.index.tz_localize("UTC")
    out = out.sort_index()
    out = out[~out.index.duplicated(keep="last")]
    out = out.asfreq("h")
    numeric_cols = out.select_dtypes(include=[np.number]).columns
    out[numeric_cols] = out[numeric_cols].ffill(limit=config.forward_fill_limit_hours)
    out[numeric_cols] = out[numeric_cols].bfill(limit=config.forward_fill_limit_hours)
    if config.clip_ghi_non_negative and "ghi_wm2" in out.columns:
        out["ghi_wm2"] = out["ghi_wm2"].clip(lower=0.0)
    return out
