from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import signal


@dataclass(slots=True)
class PreprocessingConfig:
    lowcut_hz: float = 0.05
    highcut_hz: float = 8.0
    filter_order: int = 4
    normalize: bool = True
    taper_fraction: float = 0.05


def bandpass_filter(
    waveform: np.ndarray,
    sample_rate_hz: float,
    config: PreprocessingConfig,
) -> np.ndarray:
    nyquist = 0.5 * sample_rate_hz
    low = max(config.lowcut_hz / nyquist, 1e-4)
    high = min(config.highcut_hz / nyquist, 0.99)
    if low >= high:
        return waveform.copy()

    sos = signal.butter(config.filter_order, [low, high], btype="bandpass", output="sos")
    return signal.sosfiltfilt(sos, waveform)


def taper_waveform(waveform: np.ndarray, taper_fraction: float) -> np.ndarray:
    if taper_fraction <= 0:
        return waveform.copy()
    taper_fraction = min(max(taper_fraction, 0.0), 0.45)
    window = signal.windows.tukey(waveform.size, alpha=2 * taper_fraction)
    return waveform * window


def preprocess_waveform(
    waveform: np.ndarray,
    sample_rate_hz: float,
    config: PreprocessingConfig | None = None,
) -> np.ndarray:
    config = config or PreprocessingConfig()
    cleaned = np.asarray(waveform, dtype=float)
    cleaned = signal.detrend(cleaned, type="linear")
    cleaned = taper_waveform(cleaned, taper_fraction=config.taper_fraction)
    cleaned = bandpass_filter(cleaned, sample_rate_hz=sample_rate_hz, config=config)

    if config.normalize:
        cleaned = cleaned - np.mean(cleaned)
        cleaned = cleaned / (np.std(cleaned) + 1e-8)

    return cleaned.astype(np.float32)


def preprocess_dataset(
    waveforms: np.ndarray,
    sample_rate_hz: float,
    config: PreprocessingConfig | None = None,
) -> np.ndarray:
    config = config or PreprocessingConfig()
    return np.vstack([preprocess_waveform(waveform, sample_rate_hz, config) for waveform in waveforms])
