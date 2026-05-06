from __future__ import annotations

import numpy as np
import pandas as pd

from .spec import ProjectSpec


def build_feature_table(frame: pd.DataFrame, spec: ProjectSpec) -> tuple[pd.DataFrame, list[str]]:
    features = frame.copy()
    features["hour_sin"] = np.sin(2.0 * np.pi * features["hour"] / 24.0)
    features["hour_cos"] = np.cos(2.0 * np.pi * features["hour"] / 24.0)
    features["interaction_ab"] = features["sensor_a"] * features["sensor_b"]
    features["energy_proxy"] = features["sensor_a"] ** 2 + features["sensor_b"] ** 2 + features["sensor_c"] ** 2
    features["rolling_signal_mean"] = features["physics_signal"].rolling(12, min_periods=1).mean()
    features["rolling_signal_std"] = features["physics_signal"].rolling(12, min_periods=2).std().fillna(0.0)
    features["forcing_lag_1"] = features["external_forcing"].shift(1).bfill()
    features["target_lag_1"] = pd.to_numeric(features[spec.target_name], errors="coerce").shift(1).bfill()

    feature_columns = [
        "x_coord",
        "y_coord",
        "sensor_a",
        "sensor_b",
        "sensor_c",
        "external_forcing",
        "physics_signal",
        "stressor_index",
        "hour_sin",
        "hour_cos",
        "interaction_ab",
        "energy_proxy",
        "rolling_signal_mean",
        "rolling_signal_std",
        "forcing_lag_1",
        "target_lag_1",
    ]
    return features, feature_columns
