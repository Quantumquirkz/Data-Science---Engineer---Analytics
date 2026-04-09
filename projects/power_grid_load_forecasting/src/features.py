from __future__ import annotations

from dataclasses import dataclass

import holidays
import numpy as np
import pandas as pd

HDD_CDD_BASE_C = 18.0


@dataclass(slots=True)
class FeatureConfig:
    forecast_horizons_hours: tuple[int, ...] = (24, 168)
    load_lag_hours: tuple[int, ...] = (1, 2, 3, 6, 12, 24, 48, 168)
    rolling_windows_hours: tuple[int, ...] = (6, 24, 168)
    hdd_cdd_base_c: float = HDD_CDD_BASE_C


def _country_holiday_calendar(country_code: str, years: range):
    mapping: dict[str, type] = {
        "DE": holidays.Germany,
        "AT": holidays.Austria,
        "FR": holidays.France,
        "ES": holidays.Spain,
    }
    cls = mapping.get(country_code.upper(), holidays.Germany)
    return cls(years=years)


def build_feature_table(
    frame: pd.DataFrame,
    split: pd.Series,
    country_code: str,
    config: FeatureConfig,
) -> pd.DataFrame:
    """Calendar, weather, lags, HDD/CDD, targets, and split column."""
    df = frame.copy()
    idx = df.index
    if idx.tz is None:
        raise ValueError("Expected timezone-aware index.")

    years = range(idx.year.min(), idx.year.max() + 1)
    cal = _country_holiday_calendar(country_code, years)
    local_idx = idx.tz_convert("Europe/Berlin")
    is_holiday = np.array([d in cal for d in local_idx.date], dtype=np.float64)
    df["is_holiday"] = is_holiday
    df["is_weekend"] = (local_idx.weekday >= 5).astype(np.float64)

    hour = idx.hour.to_numpy(dtype=float)
    dow = idx.dayofweek.to_numpy(dtype=float)
    month = idx.month.to_numpy(dtype=float)
    df["hour_sin"] = np.sin(2 * np.pi * hour / 24.0)
    df["hour_cos"] = np.cos(2 * np.pi * hour / 24.0)
    df["dow_sin"] = np.sin(2 * np.pi * dow / 7.0)
    df["dow_cos"] = np.cos(2 * np.pi * dow / 7.0)
    df["month_sin"] = np.sin(2 * np.pi * (month - 1) / 12.0)
    df["month_cos"] = np.cos(2 * np.pi * (month - 1) / 12.0)

    temp = df["temperature_c"].to_numpy(dtype=float)
    base = config.hdd_cdd_base_c
    df["hdd"] = np.maximum(0.0, base - temp)
    df["cdd"] = np.maximum(0.0, temp - base)

    for lag in config.load_lag_hours:
        df[f"load_lag_{lag}h"] = df["load_mw"].shift(lag)

    for window in config.rolling_windows_hours:
        df[f"load_roll_mean_{window}h"] = (
            df["load_mw"].shift(1).rolling(window, min_periods=1).mean()
        )

    for h in config.forecast_horizons_hours:
        df[f"target_load_{h}h"] = df["load_mw"].shift(-h)

    df["split"] = split.reindex(df.index).astype("string")

    target_cols = [f"target_load_{h}h" for h in config.forecast_horizons_hours]
    df = df.dropna(subset=target_cols)
    df = df.dropna(subset=select_feature_columns(df))
    return df


def select_feature_columns(features_df: pd.DataFrame) -> list[str]:
    exclude = {"split"}
    exclude.update(c for c in features_df.columns if c.startswith("target_load_"))
    return sorted(c for c in features_df.columns if c not in exclude)
