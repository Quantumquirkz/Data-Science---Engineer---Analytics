from __future__ import annotations

from pathlib import Path
import pickle

import pandas as pd


def load_forecast_bundle(model_bundle_path: Path) -> dict:
    with model_bundle_path.open("rb") as file:
        return pickle.load(file)


def load_validation_predictions(predictions_path: Path) -> pd.DataFrame:
    df = pd.read_csv(predictions_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    return df
