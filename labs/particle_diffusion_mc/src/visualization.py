from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from . import analytics


def plot_sample_paths_1d(
    times: np.ndarray,
    paths: np.ndarray,
    n_show: int = 40,
    seed: int = 0,
) -> plt.Figure:
    rng = np.random.default_rng(seed)
    idx = rng.choice(paths.shape[0], size=min(n_show, paths.shape[0]), replace=False)
    fig, ax = plt.subplots(figsize=(9, 4))
    for i in idx:
        ax.plot(times, paths[i], alpha=0.35, linewidth=0.8)
    ax.set_xlabel("t")
    ax.set_ylabel("X_t")
    ax.set_title("1D Brownian paths (sample)")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig


def plot_histogram_vs_pdf_1d(
    samples: np.ndarray,
    sigma: float,
    T: float,
    n_bins: int = 80,
) -> plt.Figure:
    std = analytics.std_endpoint_1d(sigma, T)
    span = 6.0 * std
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(samples, bins=n_bins, range=(-span, span), density=True, alpha=0.55, color="steelblue", label="MC empirical")
    xs = np.linspace(-span, span, 400)
    ax.plot(xs, analytics.pdf_endpoint_1d(xs, sigma, T), color="black", linewidth=2.0, label="N(0, sigma^2 T)")
    ax.set_xlabel("X_T")
    ax.set_ylabel("density")
    ax.set_title("Endpoint distribution vs Gaussian (heat kernel)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig


def plot_msd_1d(
    times: np.ndarray,
    empirical: np.ndarray,
    sigma: float,
) -> plt.Figure:
    theory = analytics.msd_theory_1d(times, sigma)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(times, empirical, label="empirical MSD", color="tab:blue")
    ax.plot(times, theory, "--", label="sigma^2 t", color="black")
    ax.set_xlabel("t")
    ax.set_ylabel("E[X_t^2] (sample mean)")
    ax.set_title("Mean square displacement (1D)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig


def plot_msd_2d(
    times: np.ndarray,
    empirical: np.ndarray,
    sigma: float,
) -> plt.Figure:
    theory = analytics.msd_theory_2d_squared_norm(times, sigma)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(times, empirical, label="empirical E[||X||^2]", color="tab:green")
    ax.plot(times, theory, "--", label="2 sigma^2 t", color="black")
    ax.set_xlabel("t")
    ax.set_ylabel("mean ||X_t||^2")
    ax.set_title("MSD isotropic 2D")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig


def plot_2d_endpoints_and_rayleigh(
    paths_2d: np.ndarray,
    sigma: float,
    T: float,
    n_bins: int = 50,
) -> plt.Figure:
    x = paths_2d[:, -1, 0]
    y = paths_2d[:, -1, 1]
    r = np.sqrt(x**2 + y**2)
    scale = analytics.rayleigh_scale_2d_endpoint(sigma, T)
    r_max = 5.0 * scale

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    ax0, ax1 = axes
    ax0.scatter(x, y, s=2, alpha=0.25, c="navy")
    ax0.set_aspect("equal")
    ax0.set_xlabel("X_T")
    ax0.set_ylabel("Y_T")
    ax0.set_title("2D endpoints (sample)")
    ax0.grid(True, alpha=0.3)

    ax1.hist(r, bins=n_bins, range=(0.0, r_max), density=True, alpha=0.55, color="teal", label="empirical R_T")
    rs = np.linspace(0.001, r_max, 300)
    ax1.plot(rs, analytics.pdf_rayleigh_endpoint(rs, sigma, T), color="black", linewidth=2.0, label="Rayleigh PDF")
    ax1.set_xlabel("R_T = ||X_T||")
    ax1.set_ylabel("density")
    ax1.set_title("Radial endpoint vs Rayleigh")
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig


def save_figure(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
