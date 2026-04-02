from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class SimulationConfig:
    sigma: float = 1.0
    T: float = 1.0
    n_steps: int = 500
    n_paths: int = 20_000
    random_seed: int = 42
    include_2d: bool = True


def time_grid(config: SimulationConfig) -> np.ndarray:
    return np.linspace(0.0, config.T, config.n_steps + 1, dtype=np.float64)


def simulate_bm_1d(config: SimulationConfig) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(config.random_seed)
    dt = config.T / config.n_steps
    scale = config.sigma * np.sqrt(dt)
    increments = rng.standard_normal(size=(config.n_paths, config.n_steps)) * scale
    paths = np.zeros((config.n_paths, config.n_steps + 1), dtype=np.float64)
    paths[:, 1:] = np.cumsum(increments, axis=1)
    return time_grid(config), paths


def simulate_bm_2d(config: SimulationConfig) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(config.random_seed + 1)
    dt = config.T / config.n_steps
    scale = config.sigma * np.sqrt(dt)
    inc = rng.standard_normal(size=(config.n_paths, config.n_steps, 2)) * scale
    paths = np.zeros((config.n_paths, config.n_steps + 1, 2), dtype=np.float64)
    paths[:, 1:, :] = np.cumsum(inc, axis=1)
    return time_grid(config), paths


def endpoint_radius_2d(paths_2d: np.ndarray) -> np.ndarray:
    final = paths_2d[:, -1, :]
    return np.linalg.norm(final, axis=1)
