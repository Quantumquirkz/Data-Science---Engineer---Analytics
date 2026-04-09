from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

SOLAR_CONSTANT_WM2 = 1361.0


@dataclass(slots=True)
class FeatureConfig:
    forecast_horizons_hours: tuple[int, ...] = (1, 3, 6)
    ghi_lag_hours: tuple[int, ...] = (1, 2, 3, 6, 12, 24)
    rolling_windows_hours: tuple[int, ...] = (3, 6, 24)
    clearness_epsilon_wm2: float = 1.0


def solar_elevation_degrees(times: pd.DatetimeIndex, latitude: float, longitude: float) -> np.ndarray:
    """Solar elevation (degrees) for UTC timestamps (NOAA-style approximation)."""
    lat_rad = np.radians(latitude)
    n = times.dayofyear.to_numpy(dtype=float)
    utc_hours = (
        times.hour.to_numpy(dtype=float)
        + times.minute.to_numpy(dtype=float) / 60.0
        + times.second.to_numpy(dtype=float) / 3600.0
    )
    gamma = 2.0 * np.pi * (n - 1.0) / 365.0
    eq_time = 229.18 * (
        0.000075
        + 0.001868 * np.cos(gamma)
        - 0.032077 * np.sin(gamma)
        - 0.014615 * np.cos(2 * gamma)
        - 0.040849 * np.sin(2 * gamma)
    )
    decl = (
        0.006918
        - 0.399912 * np.cos(gamma)
        + 0.070257 * np.sin(gamma)
        - 0.006758 * np.cos(2 * gamma)
        + 0.000907 * np.sin(2 * gamma)
    )
    time_min = utc_hours * 60.0 + eq_time + 4.0 * longitude
    time_min = np.mod(time_min, 24.0 * 60.0)
    ha_rad = np.radians(time_min / 4.0 - 180.0)
    sin_elev = np.sin(lat_rad) * np.sin(decl) + np.cos(lat_rad) * np.cos(decl) * np.cos(ha_rad)
    elev = np.degrees(np.arcsin(np.clip(sin_elev, -1.0, 1.0)))
    return elev.astype(np.float64)


def extraterrestrial_horizontal_wm2(
    day_of_year: np.ndarray,
    solar_elevation_deg: np.ndarray,
) -> np.ndarray:
    """Approximate extraterrestrial irradiance on a horizontal surface (W/m²)."""
    dr = 1.0 + 0.033 * np.cos(2.0 * np.pi * (day_of_year - 1) / 365.0)
    elev_rad = np.radians(solar_elevation_deg)
    beam = SOLAR_CONSTANT_WM2 * dr * np.maximum(np.sin(elev_rad), 0.0)
    return beam.astype(np.float64)


def build_feature_table(
    frame: pd.DataFrame,
    latitude: float,
    longitude: float,
    split: pd.Series,
    config: FeatureConfig,
) -> pd.DataFrame:
    """Engineer lags, solar geometry, clearness, targets, and split column."""
    df = frame.copy()
    idx = df.index
    elev = solar_elevation_degrees(idx, latitude, longitude)
    df["solar_elevation_deg"] = elev
    df["solar_zenith_deg"] = 90.0 - elev
    day_of_year = idx.dayofyear.to_numpy(dtype=float)
    df["extraterrestrial_horizontal_wm2"] = extraterrestrial_horizontal_wm2(day_of_year, elev)

    hour = idx.hour.to_numpy(dtype=float)
    df["hour_sin"] = np.sin(2 * np.pi * hour / 24.0)
    df["hour_cos"] = np.cos(2 * np.pi * hour / 24.0)
    doy = day_of_year
    df["doy_sin"] = np.sin(2 * np.pi * (doy - 1) / 365.25)
    df["doy_cos"] = np.cos(2 * np.pi * (doy - 1) / 365.25)

    denom = np.maximum(df["extraterrestrial_horizontal_wm2"].to_numpy(), config.clearness_epsilon_wm2)
    df["clearness_index"] = np.minimum(
        df["ghi_wm2"].to_numpy() / denom,
        1.5,
    )

    for lag in config.ghi_lag_hours:
        df[f"ghi_lag_{lag}h"] = df["ghi_wm2"].shift(lag)
    for lag in (1, 3):
        df[f"cloud_lag_{lag}h"] = df["cloud_cover_pct"].shift(lag)

    for window in config.rolling_windows_hours:
        df[f"ghi_roll_mean_{window}h"] = df["ghi_wm2"].shift(1).rolling(window, min_periods=1).mean()
        df[f"cloud_roll_mean_{window}h"] = df["cloud_cover_pct"].shift(1).rolling(window, min_periods=1).mean()

    df["cloud_times_elevation"] = df["cloud_cover_pct"] * df["solar_elevation_deg"].clip(lower=0.0)

    for h in config.forecast_horizons_hours:
        df[f"target_ghi_{h}h"] = df["ghi_wm2"].shift(-h)

    df["split"] = split.reindex(df.index).astype("string")

    df = df.dropna(subset=[f"target_ghi_{h}h" for h in config.forecast_horizons_hours])
    df = df.dropna(subset=select_feature_columns(df))
    return df


def select_feature_columns(features_df: pd.DataFrame) -> list[str]:
    exclude = {"split"}
    exclude.update(c for c in features_df.columns if c.startswith("target_ghi_"))
    return sorted(c for c in features_df.columns if c not in exclude)
