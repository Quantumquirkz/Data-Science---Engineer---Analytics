from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(slots=True)
class SimulationConfig:
    n_points: int = 2400
    baseline_fraction: float = 0.35
    random_seed: int = 42
    noise_scale: float = 0.35
    seasonality_strength: float = 0.2
    gradual_drift_start: float = 0.45
    gradual_drift_end: float = 0.78
    gradual_drift_magnitude: float = 2.6
    abrupt_drift_start: float = 0.82
    abrupt_drift_magnitude: float = 1.8
    outlier_fraction: float = 0.01
    sampling_minutes: int = 5


SENSOR_PROFILES = {
    "temperature": {"base": 72.0, "amplitude": 1.6, "trend": 0.02, "unit": "C"},
    "pressure": {"base": 18.5, "amplitude": 0.9, "trend": 0.01, "unit": "bar"},
    "vibration": {"base": 4.2, "amplitude": 1.8, "trend": 0.03, "unit": "mm/s"},
}


def _build_gradual_drift(index: np.ndarray, config: SimulationConfig) -> np.ndarray:
    start = int(config.n_points * config.gradual_drift_start)
    end = max(start + 1, int(config.n_points * config.gradual_drift_end))
    drift = np.zeros_like(index, dtype=float)
    ramp = np.linspace(0.0, config.gradual_drift_magnitude, end - start)
    drift[start:end] = ramp
    drift[end:] = config.gradual_drift_magnitude
    return drift


def _build_abrupt_drift(index: np.ndarray, config: SimulationConfig) -> np.ndarray:
    start = int(config.n_points * config.abrupt_drift_start)
    drift = np.zeros_like(index, dtype=float)
    drift[start:] = config.abrupt_drift_magnitude
    return drift


def generate_sensor_data(
    sensor_type: str = "temperature",
    config: SimulationConfig | None = None,
) -> pd.DataFrame:
    if sensor_type not in SENSOR_PROFILES:
        valid = ", ".join(sorted(SENSOR_PROFILES))
        raise ValueError(f"Unknown sensor_type '{sensor_type}'. Valid values: {valid}.")

    config = config or SimulationConfig()
    profile = SENSOR_PROFILES[sensor_type]
    rng = np.random.default_rng(config.random_seed)
    index = np.arange(config.n_points)

    baseline_level = profile["base"] + profile["trend"] * index
    seasonality = (
        profile["amplitude"]
        * config.seasonality_strength
        * np.sin(2 * np.pi * index / 96.0)
    )
    short_cycle = 0.35 * np.sin(2 * np.pi * index / 18.0)
    gradual_drift = _build_gradual_drift(index, config)
    abrupt_drift = _build_abrupt_drift(index, config)
    noise = rng.normal(0.0, config.noise_scale, size=config.n_points)

    observed = baseline_level + seasonality + short_cycle + gradual_drift + abrupt_drift + noise

    n_outliers = int(config.n_points * config.outlier_fraction)
    outlier_mask = np.zeros(config.n_points, dtype=bool)
    if n_outliers > 0:
        outlier_idx = rng.choice(config.n_points, size=n_outliers, replace=False)
        observed[outlier_idx] += rng.normal(0.0, 3.5 * config.noise_scale, size=n_outliers)
        outlier_mask[outlier_idx] = True

    baseline_cutoff = int(config.n_points * config.baseline_fraction)
    is_gradual = gradual_drift > 0.0
    is_abrupt = abrupt_drift > 0.0
    is_drift = is_gradual | is_abrupt

    regime = np.where(
        index < baseline_cutoff,
        "baseline",
        np.where(is_abrupt, "abrupt_drift", np.where(is_gradual, "gradual_drift", "monitoring")),
    )

    timestamps = pd.date_range(
        "2025-01-01",
        periods=config.n_points,
        freq=f"{config.sampling_minutes}min",
    )

    return pd.DataFrame(
        {
            "timestamp": timestamps,
            "sensor_type": sensor_type,
            "sensor_unit": profile["unit"],
            "value": observed,
            "baseline_value": baseline_level + seasonality + short_cycle,
            "gradual_drift_component": gradual_drift,
            "abrupt_drift_component": abrupt_drift,
            "noise_component": noise,
            "is_outlier": outlier_mask,
            "is_baseline": index < baseline_cutoff,
            "is_gradual_drift": is_gradual,
            "is_abrupt_drift": is_abrupt,
            "is_drift": is_drift,
            "regime": regime,
        }
    )
