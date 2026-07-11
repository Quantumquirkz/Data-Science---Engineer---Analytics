from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_validation_predictions(predictions_path: Path) -> pd.DataFrame:
    return pd.read_csv(predictions_path)


def load_metrics(metrics_path: Path) -> pd.DataFrame:
    return pd.read_csv(metrics_path)
