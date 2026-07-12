from __future__ import annotations

"""Curriculum indexes derived from project metadata and level manifests."""

from collections import defaultdict
import json
from pathlib import Path

from data_intelligence_engineering.catalog.project_registry import discover_project_records
from data_intelligence_engineering.catalog.project_registry import resolve_project
from data_intelligence_engineering.catalog.schemas import ProjectRecord
from data_intelligence_engineering.curriculum.models import LevelRecord
from data_intelligence_engineering.curriculum.models import MissionRecord


TRACKS: tuple[str, ...] = (
    "data_analytics",
    "data_science",
    "data_engineering",
    "ml_engineering",
    "scientific_computing",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _curriculum_root() -> Path:
    return _repo_root() / "curriculum"


def _read_json_yaml(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _string_tuple(value: object) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, list):
        return tuple(str(item) for item in value)
    return (str(value),)


def _read_notebook(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _word_count(text: str) -> int:
    return len([word for word in text.replace("`", " ").split() if word.strip()])


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


def discover_levels(curriculum_root: Path | None = None) -> tuple[LevelRecord, ...]:
    """Return every declared track level from the teaching manifests."""

    root = curriculum_root or _curriculum_root()
    records: list[LevelRecord] = []
    for track in TRACKS:
        levels_root = root / "tracks" / track / "levels"
        if not levels_root.exists():
            continue
        for syllabus_path in sorted(levels_root.glob("L*/syllabus.yaml")):
            payload = _read_json_yaml(syllabus_path)
            notebook_paths = tuple((root.parent / relative).resolve() for relative in payload.get("notebook_paths", []))
            records.append(
                LevelRecord(
                    track=str(payload["track"]),
                    level=str(payload["level"]),
                    level_number=int(payload["level_number"]),
                    title=str(payload["title"]),
                    summary=str(payload["summary"]),
                    prerequisites=_string_tuple(payload.get("prerequisites")),
                    competencies=_string_tuple(payload.get("competencies")),
                    mission_ids=_string_tuple(payload.get("mission_ids")),
                    project_ids=_string_tuple(payload.get("project_ids")),
                    notebook_paths=notebook_paths,
                    syllabus_path=syllabus_path,
                    readme_path=syllabus_path.with_name("README.md"),
                    status=str(payload.get("status", "planned")),
                )
            )
    return tuple(sorted(records, key=lambda item: (item.track, item.level_number)))


def levels_by_track(curriculum_root: Path | None = None) -> dict[str, tuple[LevelRecord, ...]]:
    grouped: dict[str, list[LevelRecord]] = defaultdict(list)
    for record in discover_levels(curriculum_root=curriculum_root):
        grouped[record.track].append(record)
    return {track: tuple(sorted(records, key=lambda item: item.level_number)) for track, records in grouped.items()}


def level_matrix(curriculum_root: Path | None = None) -> tuple[tuple[str, tuple[str, ...]], ...]:
    grouped = levels_by_track(curriculum_root=curriculum_root)
    return tuple((track, tuple(level.title for level in grouped.get(track, ()))) for track in TRACKS)


def load_mission_registry(curriculum_root: Path | None = None) -> tuple[MissionRecord, ...]:
    root = curriculum_root or _curriculum_root()
    registry_path = root / "missions" / "mission_registry.yaml"
    payload = _read_json_yaml(registry_path)
    missions: list[MissionRecord] = []
    for item in payload.get("missions", []):
        notebook = item.get("notebook_path")
        missions.append(
            MissionRecord(
                id=str(item["id"]),
                title=str(item["title"]),
                summary=str(item["summary"]),
                track=str(item["track"]),
                level=str(item["level"]),
                project_id=str(item["project_id"]),
                notebook_path=(root.parent / str(notebook)).resolve() if notebook else None,
                project_notebook=str(item["project_notebook"]) if item.get("project_notebook") else None,
                evidence=_string_tuple(item.get("evidence")),
                competencies=_string_tuple(item.get("competencies")),
                command=str(item["command"]) if item.get("command") else None,
            )
        )
    return tuple(missions)


def missions_by_track_level(curriculum_root: Path | None = None) -> dict[tuple[str, str], tuple[MissionRecord, ...]]:
    grouped: dict[tuple[str, str], list[MissionRecord]] = defaultdict(list)
    for mission in load_mission_registry(curriculum_root=curriculum_root):
        grouped[(mission.track, mission.level)].append(mission)
    return {key: tuple(value) for key, value in grouped.items()}


def missions_for_project(identifier: str, curriculum_root: Path | None = None) -> tuple[MissionRecord, ...]:
    project = resolve_project(identifier)
    return tuple(mission for mission in load_mission_registry(curriculum_root=curriculum_root) if mission.project_id == project.id)


def validate_curriculum(curriculum_root: Path | None = None) -> tuple[str, ...]:
    """Return structural validation failures for the level and mission layer."""

    failures: list[str] = []
    level_records = discover_levels(curriculum_root=curriculum_root)
    mission_records = load_mission_registry(curriculum_root=curriculum_root)
    grouped_levels = levels_by_track(curriculum_root=curriculum_root)
    for track in TRACKS:
        levels = grouped_levels.get(track, ())
        if len(levels) != 10:
            failures.append(f"{track}: expected 10 levels, found {len(levels)}")
        expected = list(range(1, len(levels) + 1))
        actual = [record.level_number for record in levels]
        if actual and actual != expected:
            failures.append(f"{track}: non-contiguous levels {actual}")
        for record in levels:
            if not record.readme_path.exists():
                failures.append(f"{track} {record.level}: missing README.md")
                continue
            readme_text = record.readme_path.read_text(encoding="utf-8")
            required_sections = (
                "## Start From Zero",
                "## Step-By-Step Learning Path",
                "## Worked Micro-Example",
                "## Guided Practice",
                "## Before You Move On",
            )
            for section in required_sections:
                if section not in readme_text:
                    failures.append(f"{track} {record.level}: missing teaching section {section}")
            if _word_count(readme_text) < 650:
                failures.append(f"{track} {record.level}: README is too short for step-by-step teaching")
            for notebook_path in record.notebook_paths:
                if not notebook_path.exists():
                    failures.append(f"{track} {record.level}: missing notebook {notebook_path.relative_to(_repo_root())}")
                    continue
                notebook = _read_notebook(notebook_path)
                cells = notebook.get("cells", [])
                if not isinstance(cells, list) or len(cells) < 10:
                    failures.append(f"{track} {record.level}: notebook has fewer than 10 teaching cells")
                    continue
                markdown_text = "\n".join(
                    "".join(cell.get("source", []))
                    for cell in cells
                    if isinstance(cell, dict) and cell.get("cell_type") == "markdown"
                )
                if "Start from zero" not in markdown_text or "Self-check without grades" not in markdown_text:
                    failures.append(f"{track} {record.level}: notebook lacks zero-background teaching prompts")
            for project_id in record.project_ids:
                try:
                    resolve_project(project_id)
                except KeyError:
                    failures.append(f"{track} {record.level}: unknown project {project_id}")

    seen_ids: set[str] = set()
    mission_ids = {mission.id for mission in mission_records}
    level_lookup = {(record.track, record.level) for record in level_records}
    for record in level_records:
        if record.status != "implemented":
            failures.append(f"{record.track} {record.level}: status is {record.status}, expected implemented")
        if not record.notebook_paths:
            failures.append(f"{record.track} {record.level}: missing central notebook path")
        for mission_id in record.mission_ids:
            if mission_id not in mission_ids:
                failures.append(f"{record.track} {record.level}: unknown mission {mission_id}")
    for mission in mission_records:
        if mission.id in seen_ids:
            failures.append(f"duplicate mission id: {mission.id}")
        seen_ids.add(mission.id)
        if (mission.track, mission.level) not in level_lookup:
            failures.append(f"{mission.id}: unknown track/level {mission.track}/{mission.level}")
        try:
            resolve_project(mission.project_id)
        except KeyError:
            failures.append(f"{mission.id}: unknown project {mission.project_id}")
        if not mission.command:
            failures.append(f"{mission.id}: missing run command")
        if not mission.notebook_path:
            failures.append(f"{mission.id}: missing central notebook path")
        if mission.notebook_path and not mission.notebook_path.exists():
            failures.append(f"{mission.id}: missing notebook {mission.notebook_path.relative_to(_repo_root())}")
    return tuple(failures)
