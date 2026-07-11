"""Repository-level configuration defaults."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RepositoryConfig:
    project_package_root: str = "projects"
    shared_package_root: str = "src/data_intelligence_engineering"
    default_sample_size: int = 720
    default_random_seed: int = 1729
