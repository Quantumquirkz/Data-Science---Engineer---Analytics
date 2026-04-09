from __future__ import annotations

import numpy as np
import pandas as pd


def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))


def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(np.mean(np.abs(y_true - y_pred)))


def smape(y_true: np.ndarray, y_pred: np.ndarray, epsilon: float = 1e-6) -> float:
    denom = np.maximum(np.abs(y_true) + np.abs(y_pred), epsilon)
    return float(100.0 * np.mean(2.0 * np.abs(y_pred - y_true) / denom))


def pinball_loss(y_true: np.ndarray, y_pred: np.ndarray, alpha: float) -> float:
    diff = y_true - y_pred
    return float(np.mean(np.maximum(alpha * diff, (alpha - 1.0) * diff)))


def interval_coverage(y_true: np.ndarray, lower: np.ndarray, upper: np.ndarray) -> float:
    return float(np.mean((y_true >= lower) & (y_true <= upper)))


def metrics_row(
    horizon_h: int,
    model_name: str,
    y_true: np.ndarray,
    y_pred: np.ndarray,
    q10: np.ndarray | None = None,
    q50: np.ndarray | None = None,
    q90: np.ndarray | None = None,
) -> dict[str, object]:
    row: dict[str, object] = {
        "horizon_h": horizon_h,
        "model": model_name,
        "rmse": rmse(y_true, y_pred),
        "mae": mae(y_true, y_pred),
        "smape": smape(y_true, y_pred),
        "pinball_q10": None,
        "pinball_q50": None,
        "pinball_q90": None,
        "interval_coverage_80": None,
    }
    if q10 is not None and q50 is not None and q90 is not None:
        row["pinball_q10"] = pinball_loss(y_true, q10, 0.1)
        row["pinball_q50"] = pinball_loss(y_true, q50, 0.5)
        row["pinball_q90"] = pinball_loss(y_true, q90, 0.9)
        row["interval_coverage_80"] = interval_coverage(y_true, q10, q90)
    return row
