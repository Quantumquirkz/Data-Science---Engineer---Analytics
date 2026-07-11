"""Helpers shared by Gradio application entrypoints."""

from __future__ import annotations

from pathlib import Path
import sys


def ensure_repo_root_on_path(project_root: Path) -> Path:
    repo_root = project_root.parents[1]
    if str(repo_root) not in sys.path:
        sys.path.append(str(repo_root))
    if str(repo_root / "src") not in sys.path:
        sys.path.append(str(repo_root / "src"))
    return repo_root
