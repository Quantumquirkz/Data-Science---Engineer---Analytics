from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import precision_recall_fscore_support


def detection_delay(y_true: pd.Series, y_pred: pd.Series) -> float:
    true_indices = np.flatnonzero(y_true.to_numpy())
    pred_indices = np.flatnonzero(y_pred.to_numpy())
    if len(true_indices) == 0 or len(pred_indices) == 0:
        return float("nan")
    first_true = int(true_indices[0])
    first_pred_after_true = pred_indices[pred_indices >= first_true]
    if len(first_pred_after_true) == 0:
        return float("nan")
    return float(first_pred_after_true[0] - first_true)


def false_alarm_rate(y_true: pd.Series, y_pred: pd.Series) -> float:
    normal_mask = ~y_true.astype(bool)
    normal_count = int(normal_mask.sum())
    if normal_count == 0:
        return 0.0
    false_alarms = int((y_pred.astype(bool) & normal_mask).sum())
    return float(false_alarms / normal_count)


def summarize_method(
    df: pd.DataFrame,
    prediction_col: str,
    name: str,
) -> dict[str, float | str]:
    y_true = df["window_label"].isin(["gradual_drift", "abrupt_drift"])
    y_pred = df[prediction_col].astype(bool)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true,
        y_pred,
        average="binary",
        zero_division=0,
    )
    return {
        "method": name,
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "false_alarm_rate": false_alarm_rate(y_true, y_pred),
        "detection_delay_windows": detection_delay(y_true, y_pred),
    }


def compare_methods(df: pd.DataFrame) -> pd.DataFrame:
    summaries = [
        summarize_method(df, "distribution_alarm", "DistributionShift"),
        summarize_method(df, "ewma_alarm", "EWMA"),
    ]
    return pd.DataFrame(summaries)
