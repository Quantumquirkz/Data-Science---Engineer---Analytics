from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .pipeline import classify_single_waveform


def load_waveform_from_csv(file_path: str | Path) -> np.ndarray:
    file_path = Path(file_path)
    frame = pd.read_csv(file_path)
    if frame.shape[1] == 1:
        waveform = frame.iloc[:, 0].to_numpy(dtype=float)
    else:
        waveform = frame.select_dtypes(include=["number"]).iloc[:, 0].to_numpy(dtype=float)
    return waveform


def predict_csv_waveform(file_path: str | Path, model_bundle_path: str | Path) -> pd.DataFrame:
    waveform = load_waveform_from_csv(file_path)
    return classify_single_waveform(waveform=waveform, model_bundle_path=Path(model_bundle_path))
