from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit


PUBLIC_DATASET_REFERENCES = [
    {
        "name": "INSTANCE",
        "role": "reference_taxonomy",
        "url": "https://doi.org/10.13127/instance",
        "notes": "Reference dataset for earthquake and background noise classes.",
    },
    {
        "name": "Seismic ambient noise classification scheme",
        "role": "microseism_proxy_reference",
        "url": "https://zenodo.org/records/7494745",
        "notes": "Surface-wave dominated slices motivate the microseism proxy class.",
    },
    {
        "name": "STEAD",
        "role": "external_validation_reference",
        "url": "https://doi.org/10.1109/ACCESS.2019.2947848",
        "notes": "Secondary benchmark for future external generalization checks.",
    },
]


@dataclass(slots=True)
class DatasetConfig:
    n_samples_per_class: int = 240
    duration_seconds: float = 60.0
    sample_rate_hz: float = 20.0
    random_seed: int = 42
    val_size: float = 0.2
    test_size: float = 0.2
    n_stations: int = 18

    @property
    def n_timesteps(self) -> int:
        return int(self.duration_seconds * self.sample_rate_hz)


def _power_law_noise(rng: np.random.Generator, n_samples: int, exponent: float) -> np.ndarray:
    freqs = np.fft.rfftfreq(n_samples, d=1.0)
    scaling = np.ones_like(freqs)
    scaling[1:] = freqs[1:] ** (-exponent / 2.0)
    phases = rng.normal(size=scaling.size) + 1j * rng.normal(size=scaling.size)
    spectrum = phases * scaling
    signal = np.fft.irfft(spectrum, n=n_samples)
    return signal / (np.std(signal) + 1e-8)


def _normalize(signal: np.ndarray) -> np.ndarray:
    centered = signal - np.mean(signal)
    scale = np.std(centered) + 1e-8
    return centered / scale


def _make_noise_signal(
    rng: np.random.Generator,
    time_axis: np.ndarray,
    station_factor: float,
) -> np.ndarray:
    colored = _power_law_noise(rng, time_axis.size, exponent=1.0)
    broadband = rng.normal(0.0, 0.6, size=time_axis.size)
    slow_trend = 0.35 * np.sin(2 * np.pi * (0.01 + 0.005 * station_factor) * time_axis + rng.uniform(0, np.pi))
    weak_swell = 0.45 * np.sin(2 * np.pi * rng.uniform(0.09, 0.18) * time_axis + rng.uniform(0, np.pi))

    impulses = np.zeros_like(time_axis)
    n_spikes = rng.integers(3, 8)
    spike_positions = rng.choice(time_axis.size, size=n_spikes, replace=False)
    impulses[spike_positions] = rng.normal(0.0, 2.5, size=n_spikes)

    signal = 0.85 * colored + 0.55 * broadband + slow_trend + 0.35 * weak_swell + impulses
    return _normalize(signal)


def _make_microseism_signal(
    rng: np.random.Generator,
    time_axis: np.ndarray,
    station_factor: float,
) -> np.ndarray:
    primary_frequency = rng.uniform(0.08, 0.12)
    secondary_frequency = rng.uniform(0.14, 0.28)
    envelope = 1.0 + 0.3 * np.sin(2 * np.pi * rng.uniform(0.005, 0.02) * time_axis + rng.uniform(0, np.pi))
    phase_shift = rng.uniform(0, np.pi)
    low_band = (
        1.6 * np.sin(2 * np.pi * primary_frequency * time_axis + phase_shift)
        + 1.2 * np.sin(2 * np.pi * secondary_frequency * time_axis)
        + 0.5 * np.sin(2 * np.pi * (secondary_frequency * 1.8) * time_axis)
    )
    background = 0.55 * _power_law_noise(rng, time_axis.size, exponent=1.4)
    transient = 0.4 * np.exp(-((time_axis - rng.uniform(20.0, 45.0)) ** 2) / (2 * 1.6**2))
    signal = (
        envelope * low_band
        + background
        + 0.1 * station_factor * np.sin(2 * np.pi * 0.04 * time_axis)
        + transient * np.sin(2 * np.pi * rng.uniform(0.7, 1.4) * time_axis)
    )
    return _normalize(signal)


def _make_earthquake_signal(
    rng: np.random.Generator,
    time_axis: np.ndarray,
    station_factor: float,
) -> np.ndarray:
    baseline = 0.35 * _power_law_noise(rng, time_axis.size, exponent=0.7)
    onset = rng.uniform(8.0, 20.0)
    p_delay = rng.uniform(0.8, 2.2)
    s_delay = p_delay + rng.uniform(2.0, 5.0)
    coda_decay = rng.uniform(0.06, 0.12)

    envelope = np.zeros_like(time_axis)
    p_mask = time_axis >= onset
    s_mask = time_axis >= onset + s_delay
    envelope[p_mask] += np.exp(-coda_decay * (time_axis[p_mask] - onset))
    envelope[s_mask] += 1.3 * np.exp(-0.6 * coda_decay * (time_axis[s_mask] - (onset + s_delay)))

    carrier = (
        1.0 * np.sin(2 * np.pi * rng.uniform(0.8, 2.2) * time_axis)
        + 0.8 * np.sin(2 * np.pi * rng.uniform(2.0, 4.2) * time_axis + rng.uniform(0, np.pi))
        + 0.5 * np.sin(2 * np.pi * rng.uniform(4.5, 6.0) * time_axis)
    )
    impulsive_wavelet = np.exp(-((time_axis - onset) ** 2) / (2 * 0.18**2))
    microseism_tail = 0.35 * np.sin(2 * np.pi * rng.uniform(0.12, 0.22) * time_axis)
    snr_scale = rng.uniform(0.8, 1.25)
    signal = (
        baseline
        + snr_scale * envelope * carrier
        + 2.4 * impulsive_wavelet
        + 0.2 * station_factor * rng.normal(size=time_axis.size)
        + microseism_tail
    )
    return _normalize(signal)


def _assign_splits(metadata: pd.DataFrame, random_seed: int, val_size: float, test_size: float) -> pd.Series:
    groups = metadata["station_id"].to_numpy()
    indices = np.arange(len(metadata))

    test_split = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=random_seed)
    train_val_idx, test_idx = next(test_split.split(indices, metadata["label"], groups))

    train_val = metadata.iloc[train_val_idx].reset_index(drop=True)
    train_val_groups = train_val["station_id"].to_numpy()
    relative_val_size = val_size / (1.0 - test_size)
    val_split = GroupShuffleSplit(n_splits=1, test_size=relative_val_size, random_state=random_seed + 1)
    train_idx_relative, val_idx_relative = next(
        val_split.split(np.arange(len(train_val)), train_val["label"], train_val_groups)
    )

    split_labels = pd.Series("train", index=metadata.index, dtype="object")
    split_labels.iloc[test_idx] = "test"
    split_labels.iloc[train_val_idx[val_idx_relative]] = "validation"
    split_labels.iloc[train_val_idx[train_idx_relative]] = "train"
    return split_labels


def generate_curated_waveform_dataset(config: DatasetConfig) -> tuple[np.ndarray, pd.DataFrame]:
    rng = np.random.default_rng(config.random_seed)
    time_axis = np.arange(config.n_timesteps) / config.sample_rate_hz
    labels = ["noise", "microseisms", "earthquakes"]

    signals: list[np.ndarray] = []
    rows: list[dict[str, object]] = []

    signal_builders = {
        "noise": _make_noise_signal,
        "microseisms": _make_microseism_signal,
        "earthquakes": _make_earthquake_signal,
    }

    for label_idx, label in enumerate(labels):
        for sample_idx in range(config.n_samples_per_class):
            station_id = f"STA_{(sample_idx + label_idx * 3) % config.n_stations:02d}"
            station_factor = 0.9 + (int(station_id.split("_")[1]) % 7) / 10.0
            sample_rng = np.random.default_rng(config.random_seed + label_idx * 10_000 + sample_idx)
            signal = signal_builders[label](sample_rng, time_axis, station_factor)

            signal_id = f"{label[:3]}_{sample_idx:04d}"
            signals.append(signal.astype(np.float32))
            rows.append(
                {
                    "signal_id": signal_id,
                    "label": label,
                    "station_id": station_id,
                    "duration_seconds": config.duration_seconds,
                    "sample_rate_hz": config.sample_rate_hz,
                    "public_reference": "proxy_curated_subset",
                    "proxy_definition": (
                        "surface-wave-dominated ambient window"
                        if label == "microseisms"
                        else "earthquake event" if label == "earthquakes" else "background noise window"
                    ),
                }
            )

    metadata = pd.DataFrame(rows)
    metadata["split"] = _assign_splits(metadata, config.random_seed, config.val_size, config.test_size)
    metadata["sample_index"] = np.arange(len(metadata))
    metadata["signal_mean"] = [float(np.mean(signal)) for signal in signals]
    metadata["signal_std"] = [float(np.std(signal)) for signal in signals]
    return np.vstack(signals), metadata


def persist_dataset(
    signals: np.ndarray,
    metadata: pd.DataFrame,
    config: DatasetConfig,
    dataset_dir: Path,
) -> dict[str, Path]:
    dataset_dir.mkdir(parents=True, exist_ok=True)
    npz_path = dataset_dir / "curated_portfolio_waveforms.npz"
    metadata_path = dataset_dir / "curated_portfolio_metadata.csv"
    provenance_path = dataset_dir / "dataset_provenance.csv"

    np.savez_compressed(
        npz_path,
        signals=signals.astype(np.float32),
        sample_rate_hz=np.array([config.sample_rate_hz], dtype=np.float32),
        duration_seconds=np.array([config.duration_seconds], dtype=np.float32),
    )
    metadata.to_csv(metadata_path, index=False)
    pd.DataFrame(PUBLIC_DATASET_REFERENCES).to_csv(provenance_path, index=False)
    return {
        "npz": npz_path,
        "metadata": metadata_path,
        "provenance": provenance_path,
    }


def load_or_build_dataset(
    dataset_dir: Path,
    config: DatasetConfig | None = None,
) -> tuple[np.ndarray, pd.DataFrame, DatasetConfig, dict[str, Path]]:
    config = config or DatasetConfig()
    dataset_dir.mkdir(parents=True, exist_ok=True)
    npz_path = dataset_dir / "curated_portfolio_waveforms.npz"
    metadata_path = dataset_dir / "curated_portfolio_metadata.csv"
    provenance_path = dataset_dir / "dataset_provenance.csv"

    if npz_path.exists() and metadata_path.exists():
        archive = np.load(npz_path)
        signals = archive["signals"].astype(np.float32)
        metadata = pd.read_csv(metadata_path)
        paths = {"npz": npz_path, "metadata": metadata_path, "provenance": provenance_path}
        return signals, metadata, config, paths

    signals, metadata = generate_curated_waveform_dataset(config)
    paths = persist_dataset(signals, metadata, config, dataset_dir)
    return signals, metadata, config, paths


def summarize_dataset(metadata: pd.DataFrame, config: DatasetConfig) -> dict[str, object]:
    class_counts = metadata["label"].value_counts().sort_index().to_dict()
    split_counts = (
        metadata.groupby(["split", "label"]).size().rename("count").reset_index().to_dict(orient="records")
    )
    return {
        "config": asdict(config),
        "class_counts": class_counts,
        "split_counts": split_counts,
        "n_stations": int(metadata["station_id"].nunique()),
    }
