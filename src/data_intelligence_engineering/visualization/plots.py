from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from ..catalog.schemas import ProjectSpec


def save_project_figures(
    features: pd.DataFrame,
    predictions: pd.DataFrame,
    projection: pd.DataFrame,
    spec: ProjectSpec,
    reports_dir: Path,
) -> dict[str, Path]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    paths: dict[str, Path] = {}

    fig, ax = plt.subplots(figsize=(8, 3.8))
    sample = features.head(240)
    ax.plot(sample["timestamp"], sample["physics_signal"], label="physics signal", linewidth=1.5)
    ax.plot(sample["timestamp"], sample["external_forcing"], label="external forcing", linewidth=1.1, alpha=0.8)
    ax.set_title(f"{spec.title}: domain signals")
    ax.set_xlabel("time")
    ax.set_ylabel("standardized units")
    ax.legend(loc="best")
    fig.autofmt_xdate()
    path = reports_dir / "domain_signals.png"
    fig.savefig(path, dpi=130, bbox_inches="tight")
    plt.close(fig)
    paths["domain_signals"] = path

    fig, ax = plt.subplots(figsize=(5.4, 4.6))
    color = features["anomaly"] if "anomaly" in features else features[spec.target_name]
    sc = ax.scatter(projection["pc1"], projection["pc2"], c=color, s=14, cmap="viridis", alpha=0.8)
    ax.set_title("Feature-space projection")
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    fig.colorbar(sc, ax=ax, label="anomaly / target")
    path = reports_dir / "feature_projection.png"
    fig.savefig(path, dpi=130, bbox_inches="tight")
    plt.close(fig)
    paths["feature_projection"] = path

    fig, ax = plt.subplots(figsize=(5.8, 4.6))
    y_true = pd.to_numeric(predictions[spec.target_name], errors="coerce")
    y_pred = pd.to_numeric(predictions["prediction"], errors="coerce")
    ax.scatter(y_true, y_pred, s=18, alpha=0.75)
    if y_true.nunique() > 5:
        low = min(y_true.min(), y_pred.min())
        high = max(y_true.max(), y_pred.max())
        ax.plot([low, high], [low, high], "--", color="black", linewidth=1)
    ax.set_title("Validation predictions")
    ax.set_xlabel("observed")
    ax.set_ylabel("predicted")
    path = reports_dir / "validation_predictions.png"
    fig.savefig(path, dpi=130, bbox_inches="tight")
    plt.close(fig)
    paths["validation_predictions"] = path

    return paths
