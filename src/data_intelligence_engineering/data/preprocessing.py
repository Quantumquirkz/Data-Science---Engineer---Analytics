from __future__ import annotations

import pandas as pd


def preprocess_observations(frame: pd.DataFrame) -> pd.DataFrame:
    clean = frame.copy()
    clean["timestamp"] = pd.to_datetime(clean["timestamp"], errors="coerce")
    clean = clean.sort_values("timestamp").reset_index(drop=True)
    numeric_columns = clean.select_dtypes(include="number").columns
    clean[numeric_columns] = clean[numeric_columns].interpolate(limit_direction="both")
    clean[numeric_columns] = clean[numeric_columns].fillna(clean[numeric_columns].median(numeric_only=True))
    clean["hour"] = clean["timestamp"].dt.hour
    clean["dayofweek"] = clean["timestamp"].dt.dayofweek
    clean["time_index"] = range(len(clean))
    return clean
