from __future__ import annotations

import numpy as np
import pandas as pd


def _safe_skew(values: np.ndarray) -> float:
    centered = values - values.mean()
    std = values.std(ddof=0)
    if std == 0:
        return 0.0
    return float(np.mean((centered / std) ** 3))


def _safe_kurtosis(values: np.ndarray) -> float:
    centered = values - values.mean()
    std = values.std(ddof=0)
    if std == 0:
        return 0.0
    return float(np.mean((centered / std) ** 4) - 3.0)


def _lag1_autocorrelation(values: np.ndarray) -> float:
    if len(values) < 2:
        return 0.0
    a = values[:-1]
    b = values[1:]
    a_std = a.std(ddof=0)
    b_std = b.std(ddof=0)
    if a_std == 0 or b_std == 0:
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])


def _window_label(is_gradual: pd.Series, is_abrupt: pd.Series) -> str:
    if bool(is_abrupt.any()):
        return "abrupt_drift"
    if bool(is_gradual.any()):
        return "gradual_drift"
    return "normal"


def build_window_features(
    df: pd.DataFrame,
    window_size: int = 60,
    step_size: int = 20,
) -> pd.DataFrame:
    records: list[dict[str, float | int | str | bool | np.ndarray | pd.Timestamp]] = []
    values = df["value"].to_numpy()

    for start in range(0, len(df) - window_size + 1, step_size):
        end = start + window_size
        window = df.iloc[start:end]
        window_values = values[start:end]
        slope, _ = np.polyfit(np.arange(window_size), window_values, deg=1)

        records.append(
            {
                "window_start": start,
                "window_end": end - 1,
                "start_timestamp": window["timestamp"].iloc[0],
                "end_timestamp": window["timestamp"].iloc[-1],
                "mean": float(window_values.mean()),
                "median": float(np.median(window_values)),
                "std": float(window_values.std(ddof=0)),
                "variance": float(window_values.var(ddof=0)),
                "range": float(window_values.max() - window_values.min()),
                "p10": float(np.percentile(window_values, 10)),
                "p25": float(np.percentile(window_values, 25)),
                "p75": float(np.percentile(window_values, 75)),
                "p90": float(np.percentile(window_values, 90)),
                "iqr": float(np.percentile(window_values, 75) - np.percentile(window_values, 25)),
                "skewness": _safe_skew(window_values),
                "kurtosis": _safe_kurtosis(window_values),
                "slope": float(slope),
                "lag1_autocorr": _lag1_autocorrelation(window_values),
                "rms": float(np.sqrt(np.mean(window_values**2))),
                "energy": float(np.mean(window_values**2)),
                "mean_abs_delta": float(np.mean(np.abs(np.diff(window_values)))),
                "outlier_fraction": float(window["is_outlier"].mean()),
                "drift_fraction": float(window["is_drift"].mean()),
                "is_baseline_window": bool(window["is_baseline"].all()),
                "window_label": _window_label(window["is_gradual_drift"], window["is_abrupt_drift"]),
                "window_values": window_values.copy(),
            }
        )

    return pd.DataFrame.from_records(records)
