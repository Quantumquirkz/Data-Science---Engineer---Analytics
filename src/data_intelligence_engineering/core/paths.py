"""Path helpers for repository tooling."""

from __future__ import annotations

from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def project_root(slug: str) -> Path:
    return repo_root() / "projects" / slug
