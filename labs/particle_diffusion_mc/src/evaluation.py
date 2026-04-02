from __future__ import annotations

import numpy as np
from scipy import stats

from . import analytics


def empirical_msd_1d(paths: np.ndarray, times: np.ndarray) -> np.ndarray:
    return np.mean(paths**2, axis=0)


def empirical_msd_2d(paths_2d: np.ndarray, times: np.ndarray) -> np.ndarray:
    sq = np.sum(paths_2d**2, axis=2)
    return np.mean(sq, axis=0)


def msd_rmse(empirical: np.ndarray, theoretical: np.ndarray) -> float:
    return float(np.sqrt(np.mean((empirical - theoretical) ** 2)))


def ks_test_endpoint_1d(samples: np.ndarray, sigma: float, T: float) -> tuple[float, float]:
    std = analytics.std_endpoint_1d(sigma, T)

    def cdf_reference(x):
        return stats.norm.cdf(x, loc=0.0, scale=std)

    result = stats.kstest(samples, cdf_reference)
    return float(result.statistic), float(result.pvalue)


def histogram_density_l2_error(
    samples: np.ndarray,
    sigma: float,
    T: float,
    n_bins: int = 80,
    span_sigmas: float = 6.0,
) -> float:
    std = analytics.std_endpoint_1d(sigma, T)
    half = span_sigmas * std
    counts, edges = np.histogram(samples, bins=n_bins, range=(-half, half), density=True)
    centers = 0.5 * (edges[:-1] + edges[1:])
    theory = analytics.pdf_endpoint_1d(centers, sigma, T)
    width = edges[1] - edges[0]
    return float(np.sqrt(np.sum((counts - theory) ** 2) * width))


def ks_test_rayleigh_2d(radii: np.ndarray, sigma: float, T: float) -> tuple[float, float]:
    scale = analytics.rayleigh_scale_2d_endpoint(sigma, T)
    dist = stats.rayleigh(scale=scale)

    def cdf_reference(x):
        return dist.cdf(x)

    result = stats.kstest(radii, cdf_reference)
    return float(result.statistic), float(result.pvalue)


def histogram_rayleigh_l2(
    radii: np.ndarray,
    sigma: float,
    T: float,
    n_bins: int = 60,
    r_max_factor: float = 5.0,
) -> float:
    scale = analytics.rayleigh_scale_2d_endpoint(sigma, T)
    r_max = r_max_factor * scale
    counts, edges = np.histogram(radii, bins=n_bins, range=(0.0, r_max), density=True)
    centers = 0.5 * (edges[:-1] + edges[1:])
    theory = analytics.pdf_rayleigh_endpoint(centers, sigma, T)
    width = edges[1] - edges[0]
    return float(np.sqrt(np.sum((counts - theory) ** 2) * width))
