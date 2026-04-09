from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.stats import ks_2samp, wasserstein_distance


@dataclass(slots=True)
class DistributionDriftConfig:
    persistence_windows: int = 2
    ks_weight: float = 0.55
    wasserstein_weight: float = 0.45
    threshold_quantile: float = 0.95


@dataclass(slots=True)
class EwmaConfig:
    alpha: float = 0.25
    persistence_windows: int = 2
    threshold_sigma: float = 3.0


def _psi(expected: np.ndarray, observed: np.ndarray, bins: int = 10) -> float:
    edges = np.histogram_bin_edges(expected, bins=bins)
    expected_hist, _ = np.histogram(expected, bins=edges)
    observed_hist, _ = np.histogram(observed, bins=edges)
    expected_pct = np.clip(expected_hist / max(len(expected), 1), 1e-6, None)
    observed_pct = np.clip(observed_hist / max(len(observed), 1), 1e-6, None)
    return float(np.sum((observed_pct - expected_pct) * np.log(observed_pct / expected_pct)))


def _normalize_scores(
    scores: pd.Series,
    baseline_mask: pd.Series,
    threshold_quantile: float,
) -> tuple[pd.Series, float]:
    baseline_scores = scores[baseline_mask]
    center = baseline_scores.median()
    spread = np.median(np.abs(baseline_scores - center))
    spread = float(spread if spread > 1e-6 else baseline_scores.std(ddof=0) + 1e-6)
    normalized = (scores - center) / spread
    threshold = float(np.quantile(normalized[baseline_mask], threshold_quantile))
    return normalized, threshold


def _apply_persistence(signal: pd.Series, persistence_windows: int) -> pd.Series:
    persistent = []
    streak = 0
    for flag in signal.astype(bool):
        streak = streak + 1 if flag else 0
        persistent.append(streak >= persistence_windows)
    return pd.Series(persistent, index=signal.index)


def detect_distribution_drift(
    windows_df: pd.DataFrame,
    config: DistributionDriftConfig | None = None,
) -> pd.DataFrame:
    config = config or DistributionDriftConfig()
    baseline_windows = windows_df.loc[windows_df["is_baseline_window"], "window_values"]
    baseline_values = np.concatenate(baseline_windows.to_list())

    scores = []
    for window_values in windows_df["window_values"]:
        ks_stat = float(ks_2samp(baseline_values, window_values).statistic)
        distance = float(wasserstein_distance(baseline_values, window_values))
        psi_value = _psi(baseline_values, window_values)
        scores.append((ks_stat, distance, psi_value))

    result = windows_df.copy()
    result["ks_stat"] = [row[0] for row in scores]
    result["wasserstein"] = [row[1] for row in scores]
    result["psi"] = [row[2] for row in scores]
    raw_score = (
        config.ks_weight * result["ks_stat"]
        + config.wasserstein_weight * result["wasserstein"]
    )
    result["distribution_score"], threshold = _normalize_scores(
        raw_score,
        result["is_baseline_window"],
        config.threshold_quantile,
    )
    result["distribution_threshold"] = threshold
    result["distribution_alarm_raw"] = result["distribution_score"] > threshold
    result["distribution_alarm"] = _apply_persistence(
        result["distribution_alarm_raw"],
        config.persistence_windows,
    )
    return result


def detect_ewma_drift(
    windows_df: pd.DataFrame,
    feature_name: str = "mean",
    config: EwmaConfig | None = None,
) -> pd.DataFrame:
    config = config or EwmaConfig()
    result = windows_df.copy()
    baseline = result.loc[result["is_baseline_window"], feature_name]
    baseline_mean = float(baseline.mean())
    baseline_std = float(baseline.std(ddof=0) + 1e-6)

    ewma_values = []
    previous = baseline_mean
    for value in result[feature_name]:
        previous = config.alpha * float(value) + (1 - config.alpha) * previous
        ewma_values.append(previous)

    result["ewma_value"] = ewma_values
    result["ewma_score"] = np.abs(result["ewma_value"] - baseline_mean) / baseline_std
    result["ewma_threshold"] = config.threshold_sigma
    result["ewma_alarm_raw"] = result["ewma_score"] > config.threshold_sigma
    result["ewma_alarm"] = _apply_persistence(
        result["ewma_alarm_raw"],
        config.persistence_windows,
    )
    return result
