from __future__ import annotations

import numpy as np
from scipy import stats


def variance_endpoint_1d(sigma: float, T: float) -> float:
    """Var(X_T) for dX = sigma dW, X_0 = 0."""
    return float(sigma**2 * T)


def std_endpoint_1d(sigma: float, T: float) -> float:
    return float(sigma * np.sqrt(T))


def pdf_endpoint_1d(x: np.ndarray, sigma: float, T: float) -> np.ndarray:
    """Gaussian density of X_T ~ N(0, sigma^2 T)."""
    s = std_endpoint_1d(sigma, T)
    return stats.norm.pdf(x, loc=0.0, scale=s)


def cdf_endpoint_1d(x: np.ndarray, sigma: float, T: float) -> np.ndarray:
    s = std_endpoint_1d(sigma, T)
    return stats.norm.cdf(x, loc=0.0, scale=s)


def msd_theory_1d(times: np.ndarray, sigma: float) -> np.ndarray:
    """E[X_t^2] = sigma^2 t for each t (1D BM from 0)."""
    return (sigma**2) * times


def msd_theory_2d_squared_norm(times: np.ndarray, sigma: float) -> np.ndarray:
    """E[||X_t||^2] = 2 sigma^2 t for isotropic 2D BM from origin."""
    return 2.0 * (sigma**2) * times


def rayleigh_scale_2d_endpoint(sigma: float, T: float) -> float:
    """If X,Y ~ iid N(0, sigma^2 T), R = sqrt(X^2+Y^2) is Rayleigh(scale=sigma*sqrt(T))."""
    return float(sigma * np.sqrt(T))


def pdf_rayleigh_endpoint(r: np.ndarray, sigma: float, T: float) -> np.ndarray:
    scale = rayleigh_scale_2d_endpoint(sigma, T)
    return stats.rayleigh.pdf(r, scale=scale)


def cdf_rayleigh_endpoint(r: np.ndarray, sigma: float, T: float) -> np.ndarray:
    scale = rayleigh_scale_2d_endpoint(sigma, T)
    return stats.rayleigh.cdf(r, scale=scale)
