from __future__ import annotations

"""Curriculum indexes derived from project metadata."""

from collections import defaultdict

from data_intelligence_engineering.catalog.project_registry import discover_project_records
from data_intelligence_engineering.catalog.schemas import ProjectRecord


def projects_by_track() -> dict[str, tuple[ProjectRecord, ...]]:
    """Return project records grouped by learning track."""

    grouped: dict[str, list[ProjectRecord]] = defaultdict(list)
    for record in discover_project_records():
        for track in record.tracks:
            grouped[track].append(record)
    return {track: tuple(sorted(records, key=lambda item: item.id)) for track, records in grouped.items()}


def projects_by_template() -> dict[str, tuple[ProjectRecord, ...]]:
    """Return project records grouped by role-specific template family."""

    grouped: dict[str, list[ProjectRecord]] = defaultdict(list)
    for record in discover_project_records():
        grouped[record.template].append(record)
    return {template: tuple(sorted(records, key=lambda item: item.id)) for template, records in grouped.items()}
