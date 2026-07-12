from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class LevelRecord:
    """Structured description of one teaching level inside one track."""

    track: str
    level: str
    level_number: int
    title: str
    summary: str
    prerequisites: tuple[str, ...]
    competencies: tuple[str, ...]
    mission_ids: tuple[str, ...]
    project_ids: tuple[str, ...]
    notebook_paths: tuple[Path, ...]
    syllabus_path: Path
    readme_path: Path
    status: str


@dataclass(frozen=True, slots=True)
class MissionRecord:
    """One project-linked learning mission in the teaching graph."""

    id: str
    title: str
    summary: str
    track: str
    level: str
    project_id: str
    notebook_path: Path | None
    project_notebook: str | None
    evidence: tuple[str, ...]
    competencies: tuple[str, ...]
    command: str | None

