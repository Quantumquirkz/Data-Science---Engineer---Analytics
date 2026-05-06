from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .spec import ProjectSpec


def _domain_coordinates(domain: str, n_samples: int, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    if domain in {"spatial", "environment", "geoscience", "astronomy"}:
        x = rng.uniform(-1.0, 1.0, n_samples)
        y = rng.uniform(-1.0, 1.0, n_samples)
    elif domain in {"network", "logistics", "traffic", "recommendation"}:
        x = rng.integers(0, 25, n_samples).astype(float)
        y = rng.integers(0, 25, n_samples).astype(float)
    else:
        x = np.linspace(-1.0, 1.0, n_samples)
        y = rng.normal(0.0, 0.45, n_samples)
    return x, y


def generate_domain_dataset(spec: ProjectSpec, n_samples: int = 720, random_seed: int | None = None) -> pd.DataFrame:
    """Generate a reproducible research-grade proxy dataset for the project domain.

    The generated table is intentionally compact enough for portfolio demos while
    preserving the dominant structure of the target problem: temporal dynamics,
    spatial fields, nonlinear physical response, rare events, and noisy sensors.
    """

    seed = spec.random_seed if random_seed is None else random_seed
    rng = np.random.default_rng(seed)
    n_samples = int(max(180, n_samples))
    t = np.arange(n_samples, dtype=float)
    phase = 2.0 * np.pi * t / max(n_samples, 1)
    x, y = _domain_coordinates(spec.domain, n_samples, rng)

    seasonal = np.sin(phase * 4.0)
    slow_trend = (t - t.mean()) / max(t.std(), 1.0)
    wave = np.sin(3.0 * x + 2.0 * y + phase) + 0.35 * np.cos(5.0 * y - phase / 2.0)
    forcing = 0.7 * seasonal + 0.25 * slow_trend + rng.normal(0.0, 0.08, n_samples)
    sensor_a = wave + forcing + rng.normal(0.0, 0.12, n_samples)
    sensor_b = 0.55 * np.cos(2.0 * x - y) + 0.35 * seasonal + rng.normal(0.0, 0.15, n_samples)
    sensor_c = np.sin(sensor_a) + 0.2 * sensor_b + rng.normal(0.0, 0.10, n_samples)
    stressor = np.abs(sensor_a) + 0.6 * np.abs(sensor_b) + 0.2 * np.maximum(slow_trend, 0)
    physics_response = 1.6 * sensor_a - 0.9 * sensor_b + 0.45 * sensor_c**2 + 0.25 * x * y

    anomaly_score = stressor + 0.25 * rng.normal(size=n_samples)
    anomaly_threshold = np.quantile(anomaly_score, 0.90)
    anomaly = anomaly_score > anomaly_threshold
    class_label = pd.qcut(
        physics_response + 0.45 * anomaly.astype(float) + rng.normal(0.0, 0.25, n_samples),
        q=3,
        labels=False,
        duplicates="drop",
    )
    class_label = np.asarray(class_label, dtype=int)
    target = physics_response + 0.35 * forcing + rng.normal(0.0, 0.18, n_samples)

    if spec.task_kind in {"forecasting", "state_space", "control"}:
        target = pd.Series(target).rolling(8, min_periods=1).mean().shift(-1).bfill().to_numpy()
    elif spec.task_kind in {"classification", "segmentation", "rare_event"}:
        target = class_label
    elif spec.task_kind in {"anomaly", "event_detection"}:
        target = anomaly.astype(int)
    elif spec.task_kind in {"optimization", "simulation"}:
        target = target - 0.35 * np.square(sensor_b) + 0.15 * np.maximum(sensor_a, 0)
    elif spec.task_kind == "recommendation":
        target = 0.5 * class_label + 0.5 * (sensor_a > np.median(sensor_a)).astype(int)

    frame = pd.DataFrame(
        {
            "timestamp": pd.date_range("2024-01-01", periods=n_samples, freq="h"),
            "x_coord": x,
            "y_coord": y,
            "sensor_a": sensor_a,
            "sensor_b": sensor_b,
            "sensor_c": sensor_c,
            "external_forcing": forcing,
            "physics_signal": physics_response,
            "stressor_index": stressor,
            "anomaly": anomaly.astype(int),
            "class_label": class_label,
            spec.target_name: target,
        }
    )
    return frame


def load_or_build_dataset(
    project_root: Path,
    spec: ProjectSpec,
    n_samples: int = 720,
    random_seed: int | None = None,
) -> tuple[pd.DataFrame, Path]:
    processed = project_root / "data" / "processed"
    processed.mkdir(parents=True, exist_ok=True)
    raw_path = processed / "synthetic_domain_observations.csv"
    frame = generate_domain_dataset(spec, n_samples=n_samples, random_seed=random_seed)
    frame.to_csv(raw_path, index=False)
    return frame, raw_path


def summarize_dataset(frame: pd.DataFrame, spec: ProjectSpec) -> dict[str, object]:
    target = frame[spec.target_name]
    return {
        "project": spec.title,
        "rows": int(len(frame)),
        "columns": int(frame.shape[1]),
        "domain": spec.domain,
        "task_kind": spec.task_kind,
        "target": spec.target_name,
        "target_mean": float(pd.to_numeric(target, errors="coerce").mean()),
        "target_std": float(pd.to_numeric(target, errors="coerce").std()),
        "anomaly_rate": float(frame["anomaly"].mean()) if "anomaly" in frame else None,
        "data_policy": spec.public_data_note,
    }
