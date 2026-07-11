"""Validation helpers for repository structure."""

from __future__ import annotations

from pathlib import Path

EXPECTED_PROJECT_FILES = (
    "README.md",
    "app.py",
    "data/README.md",
    "src/__init__.py",
)


def validate_project_root(project_dir: Path) -> list[str]:
    missing: list[str] = []
    for relative in EXPECTED_PROJECT_FILES:
        if not (project_dir / relative).exists():
            missing.append(relative)
    return missing
