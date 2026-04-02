from __future__ import annotations

from dataclasses import asdict

import pandas as pd

from .data import SimulationConfig, generate_sensor_data
from .drift_detection import (
    DistributionDriftConfig,
    EwmaConfig,
    detect_distribution_drift,
    detect_ewma_drift,
)
from .evaluation import compare_methods
from .features import build_window_features


def run_sensor_drift_pipeline(
    sensor_type: str = "temperature",
    simulation_config: SimulationConfig | None = None,
    window_size: int = 60,
    step_size: int = 20,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, int | float]]:
    simulation_config = simulation_config or SimulationConfig()
    raw_df = generate_sensor_data(sensor_type=sensor_type, config=simulation_config)
    windows_df = build_window_features(raw_df, window_size=window_size, step_size=step_size)
    windows_df = detect_distribution_drift(windows_df, DistributionDriftConfig())
    windows_df = detect_ewma_drift(windows_df, feature_name="mean", config=EwmaConfig())
    metrics_df = compare_methods(windows_df)

    metadata = {
        "sensor_type": sensor_type,
        "window_size": window_size,
        "step_size": step_size,
        **asdict(simulation_config),
    }
    return raw_df, windows_df, metrics_df, metadata
