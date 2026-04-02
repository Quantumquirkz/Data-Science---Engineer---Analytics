from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy import signal, stats


@dataclass(slots=True)
class FeatureConfig:
    spectral_bands_hz: tuple[tuple[float, float], ...] = (
        (0.05, 0.20),
        (0.20, 1.00),
        (1.00, 3.00),
        (3.00, 8.00),
    )
    wavelet_levels: int = 4


def _safe_entropy(values: np.ndarray) -> float:
    values = np.asarray(values, dtype=float)
    total = float(np.sum(values))
    if total <= 0:
        return 0.0
    probs = np.clip(values / total, 1e-12, None)
    return float(-np.sum(probs * np.log2(probs)))


def _zero_crossing_rate(waveform: np.ndarray) -> float:
    signs = np.signbit(waveform)
    return float(np.mean(signs[1:] != signs[:-1]))


def _effective_duration(waveform: np.ndarray, sample_rate_hz: float) -> float:
    energy = waveform**2
    threshold = 0.1 * np.max(energy)
    active = np.flatnonzero(energy >= threshold)
    if active.size == 0:
        return 0.0
    return float((active[-1] - active[0] + 1) / sample_rate_hz)


def _temporal_features(waveform: np.ndarray, sample_rate_hz: float) -> dict[str, float]:
    abs_waveform = np.abs(waveform)
    return {
        "mean": float(np.mean(waveform)),
        "std": float(np.std(waveform)),
        "rms": float(np.sqrt(np.mean(waveform**2))),
        "energy": float(np.sum(waveform**2) / waveform.size),
        "zcr": _zero_crossing_rate(waveform),
        "peak_to_peak": float(np.ptp(waveform)),
        "crest_factor": float(np.max(abs_waveform) / (np.sqrt(np.mean(waveform**2)) + 1e-8)),
        "skewness": float(stats.skew(waveform)),
        "kurtosis": float(stats.kurtosis(waveform)),
        "q10": float(np.quantile(waveform, 0.10)),
        "q50": float(np.quantile(waveform, 0.50)),
        "q90": float(np.quantile(waveform, 0.90)),
        "activity_density": float(np.mean(abs_waveform > 0.75 * np.std(waveform))),
        "effective_duration_s": _effective_duration(waveform, sample_rate_hz),
    }


def _spectral_features(
    waveform: np.ndarray,
    sample_rate_hz: float,
    config: FeatureConfig,
) -> dict[str, float]:
    freqs, power = signal.welch(
        waveform,
        fs=sample_rate_hz,
        nperseg=min(256, waveform.size),
        noverlap=min(128, waveform.size // 2),
    )
    power = np.maximum(power, 1e-12)
    total_power = float(np.sum(power))
    dominant_idx = int(np.argmax(power))
    centroid = float(np.sum(freqs * power) / total_power)
    spread = float(np.sqrt(np.sum(((freqs - centroid) ** 2) * power) / total_power))
    cumulative = np.cumsum(power) / total_power
    rolloff_idx = int(np.searchsorted(cumulative, 0.85))

    band_features = {}
    for lower, upper in config.spectral_bands_hz:
        mask = (freqs >= lower) & (freqs < upper)
        band_name = f"bandpower_{lower:.2f}_{upper:.2f}".replace(".", "p")
        band_features[band_name] = float(np.sum(power[mask]) / total_power)

    return {
        "dominant_frequency_hz": float(freqs[dominant_idx]),
        "spectral_centroid_hz": centroid,
        "spectral_bandwidth_hz": spread,
        "spectral_entropy": _safe_entropy(power),
        "spectral_flatness": float(np.exp(np.mean(np.log(power))) / np.mean(power)),
        "rolloff_85_hz": float(freqs[min(rolloff_idx, len(freqs) - 1)]),
        **band_features,
    }


def _haar_detail_energies(waveform: np.ndarray, levels: int) -> list[float]:
    approx = waveform.copy()
    energies: list[float] = []

    for _ in range(levels):
        usable = approx[: (approx.size // 2) * 2]
        if usable.size < 2:
            break
        even = usable[::2]
        odd = usable[1::2]
        detail = (even - odd) / np.sqrt(2.0)
        approx = (even + odd) / np.sqrt(2.0)
        energies.append(float(np.mean(detail**2)))

    energies.append(float(np.mean(approx**2)))
    return energies


def _wavelet_features(waveform: np.ndarray, config: FeatureConfig) -> dict[str, float]:
    energies = np.array(_haar_detail_energies(waveform, config.wavelet_levels), dtype=float)
    features = {
        f"wavelet_energy_level_{idx + 1}": float(energy)
        for idx, energy in enumerate(energies[:-1])
    }
    features["wavelet_approx_energy"] = float(energies[-1])
    features["wavelet_entropy"] = _safe_entropy(energies)
    features["wavelet_energy_ratio_high_low"] = float(
        np.sum(energies[:-1][:2]) / (energies[-1] + 1e-8)
    )
    return features


def build_feature_table(
    waveforms: np.ndarray,
    metadata: pd.DataFrame,
    sample_rate_hz: float,
    config: FeatureConfig | None = None,
) -> pd.DataFrame:
    config = config or FeatureConfig()
    rows: list[dict[str, float | str]] = []

    for waveform, row in zip(waveforms, metadata.itertuples(index=False), strict=True):
        feature_row: dict[str, float | str] = {
            "signal_id": row.signal_id,
            "label": row.label,
            "split": row.split,
            "station_id": row.station_id,
        }
        feature_row.update(_temporal_features(waveform, sample_rate_hz))
        feature_row.update(_spectral_features(waveform, sample_rate_hz, config))
        feature_row.update(_wavelet_features(waveform, config))
        rows.append(feature_row)

    return pd.DataFrame(rows)


def select_feature_columns(features_df: pd.DataFrame) -> list[str]:
    excluded = {"signal_id", "label", "split", "station_id"}
    return [column for column in features_df.columns if column not in excluded]
