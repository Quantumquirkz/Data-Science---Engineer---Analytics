from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    log_loss,
    precision_recall_fscore_support,
)


@dataclass(slots=True)
class EvaluationBundle:
    summary: pd.DataFrame
    per_class: pd.DataFrame
    confusion: pd.DataFrame
    confidence: pd.DataFrame
    predictions: pd.DataFrame


def _multiclass_brier_score(y_true: np.ndarray, probabilities: np.ndarray, labels: list[str]) -> float:
    label_to_index = {label: idx for idx, label in enumerate(labels)}
    one_hot = np.zeros_like(probabilities)
    for row_idx, label in enumerate(y_true):
        one_hot[row_idx, label_to_index[str(label)]] = 1.0
    return float(np.mean(np.sum((probabilities - one_hot) ** 2, axis=1)))


def evaluate_classifier(
    model_name: str,
    split_name: str,
    y_true: np.ndarray,
    y_pred: np.ndarray,
    probabilities: np.ndarray,
    labels: list[str],
    signal_ids: np.ndarray,
) -> EvaluationBundle:
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true,
        y_pred,
        labels=labels,
        zero_division=0,
    )
    per_class = pd.DataFrame(
        {
            "model": model_name,
            "split": split_name,
            "label": labels,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "support": support,
        }
    )

    summary = pd.DataFrame(
        [
            {
                "model": model_name,
                "split": split_name,
                "accuracy": accuracy_score(y_true, y_pred),
                "macro_f1": f1_score(y_true, y_pred, average="macro"),
                "weighted_f1": f1_score(y_true, y_pred, average="weighted"),
                "log_loss": log_loss(y_true, probabilities, labels=labels),
                "multiclass_brier": _multiclass_brier_score(y_true, probabilities, labels),
            }
        ]
    )

    confusion = pd.DataFrame(
        confusion_matrix(y_true, y_pred, labels=labels),
        index=labels,
        columns=labels,
    )
    confusion.index.name = "true_label"
    confusion.columns.name = "predicted_label"

    max_confidence = probabilities.max(axis=1)
    confidence = pd.DataFrame(
        {
            "model": model_name,
            "split": split_name,
            "mean_max_probability": [float(np.mean(max_confidence))],
            "median_max_probability": [float(np.median(max_confidence))],
            "low_confidence_share": [float(np.mean(max_confidence < 0.60))],
        }
    )

    predictions = pd.DataFrame(
        {
            "signal_id": signal_ids,
            "split": split_name,
            "true_label": y_true,
            "predicted_label": y_pred,
            "confidence": max_confidence,
        }
    )
    for idx, label in enumerate(labels):
        predictions[f"prob_{label}"] = probabilities[:, idx]

    return EvaluationBundle(
        summary=summary,
        per_class=per_class,
        confusion=confusion,
        confidence=confidence,
        predictions=predictions,
    )


def compare_model_summaries(evaluations: list[EvaluationBundle]) -> pd.DataFrame:
    return pd.concat([evaluation.summary for evaluation in evaluations], ignore_index=True)


def build_classification_report_text(y_true: np.ndarray, y_pred: np.ndarray, labels: list[str]) -> str:
    return classification_report(y_true, y_pred, labels=labels, zero_division=0)
