from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import signal


sns.set_theme(style="whitegrid")


def _morlet_wavelet(width: int, w: float = 5.0) -> np.ndarray:
    support = int(max(16, 10 * width))
    half = support // 2
    time_axis = np.arange(-half, half + 1, dtype=float) / max(width, 1)
    gaussian = np.exp(-(time_axis**2) / 2.0)
    carrier = np.exp(1j * w * time_axis)
    wavelet = gaussian * carrier
    return wavelet / (np.sqrt(np.sum(np.abs(wavelet) ** 2)) + 1e-8)


def plot_example_waveforms(
    waveforms: np.ndarray,
    metadata: pd.DataFrame,
    sample_rate_hz: float,
    n_examples_per_class: int = 2,
):
    labels = metadata["label"].drop_duplicates().tolist()
    time_axis = np.arange(waveforms.shape[1]) / sample_rate_hz
    fig, axes = plt.subplots(len(labels), n_examples_per_class, figsize=(14, 8), sharex=True, sharey=True)
    axes = np.atleast_2d(axes)

    for row_idx, label in enumerate(labels):
        subset = metadata.loc[metadata["label"] == label].head(n_examples_per_class)
        for col_idx, sample_index in enumerate(subset["sample_index"]):
            axes[row_idx, col_idx].plot(time_axis, waveforms[int(sample_index)], lw=1.0)
            axes[row_idx, col_idx].set_title(f"{label} #{col_idx + 1}")
            axes[row_idx, col_idx].set_ylabel("Amplitude")
    axes[-1, 0].set_xlabel("Seconds")
    axes[-1, -1].set_xlabel("Seconds")
    fig.tight_layout()
    return fig


def plot_average_spectra(waveforms: np.ndarray, metadata: pd.DataFrame, sample_rate_hz: float):
    fig, ax = plt.subplots(figsize=(10, 5))
    for label in metadata["label"].drop_duplicates():
        subset = metadata.loc[metadata["label"] == label, "sample_index"].head(80).to_numpy()
        spectra = []
        freqs = None
        for sample_index in subset:
            freqs, power = signal.welch(waveforms[int(sample_index)], fs=sample_rate_hz, nperseg=256)
            spectra.append(power)
        mean_spectrum = np.mean(spectra, axis=0)
        ax.semilogy(freqs, mean_spectrum, label=label)

    ax.set_title("Average power spectral density by class")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Power spectral density")
    ax.legend()
    fig.tight_layout()
    return fig


def plot_scalogram_example(waveform: np.ndarray, sample_rate_hz: float):
    widths = np.arange(1, 64)
    scalogram_rows = []
    for width in widths:
        kernel = _morlet_wavelet(width)
        transformed = signal.convolve(waveform, kernel, mode="same")
        scalogram_rows.append(np.abs(transformed))
    cwt = np.vstack(scalogram_rows)
    frequencies = sample_rate_hz / np.maximum(widths, 1)

    fig, ax = plt.subplots(figsize=(10, 4))
    mesh = ax.imshow(
        np.abs(cwt),
        aspect="auto",
        origin="lower",
        extent=[0, waveform.size / sample_rate_hz, frequencies.min(), frequencies.max()],
        cmap="magma",
    )
    ax.set_title("Wavelet scalogram example")
    ax.set_xlabel("Seconds")
    ax.set_ylabel("Pseudo-frequency (Hz)")
    fig.colorbar(mesh, ax=ax, label="Magnitude")
    fig.tight_layout()
    return fig


def plot_feature_separation(features_df: pd.DataFrame):
    selected = [
        "rms",
        "dominant_frequency_hz",
        "bandpower_0p20_1p00",
        "wavelet_entropy",
    ]
    available = [feature for feature in selected if feature in features_df.columns]
    melted = features_df.melt(id_vars=["label"], value_vars=available, var_name="feature", value_name="value")

    fig, ax = plt.subplots(figsize=(12, 5))
    sns.boxplot(data=melted, x="feature", y="value", hue="label", ax=ax)
    ax.set_title("Feature separation across classes")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    return fig


def plot_confusion_matrix(confusion_df: pd.DataFrame, title: str):
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(confusion_df, annot=True, fmt=".0f", cmap="Blues", ax=ax)
    ax.set_title(title)
    fig.tight_layout()
    return fig


def plot_feature_importance(importance_df: pd.DataFrame, model_name: str, top_n: int = 10):
    subset = (
        importance_df.loc[importance_df["model"] == model_name]
        .sort_values("importance", ascending=False)
        .head(top_n)
        .sort_values("importance")
    )
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(subset["feature"], subset["importance"])
    ax.set_title(f"Top {top_n} feature importances - {model_name}")
    ax.set_xlabel("Importance")
    fig.tight_layout()
    return fig


def plot_prediction_confidence(predictions_df: pd.DataFrame, model_name: str):
    subset = predictions_df.copy()
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(
        data=subset,
        x="confidence",
        hue="true_label",
        bins=20,
        element="step",
        stat="density",
        common_norm=False,
        ax=ax,
    )
    ax.set_title(f"Prediction confidence distribution - {model_name}")
    ax.set_xlabel("Maximum class probability")
    fig.tight_layout()
    return fig
