"""Metadata-backed registry for portfolio projects.

The registry resolves both stable project IDs (``p001``) and legacy slugs
(``sensor_drift_detection``).  It intentionally avoids filesystem aliases so
existing slug paths remain valid while the teaching catalog gains stable IDs.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .domains import infer_domain_group
from .schemas import ProjectRecord

FEATURED_PROJECTS: tuple[str, ...] = (
    "sensor_drift_detection",
    "gravitational_orbit_simulator",
    "renewable_energy_mix_optimizer",
    "particle_diffusion_mc",
)

_TAXONOMY_DIRS = {"featured", "generated", "by_domain", "_archive", "_templates", "_portfolio_common"}


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _projects_root() -> Path:
    return _repo_root() / "projects"


def _title_from_slug(slug: str) -> str:
    return slug.replace("_", " ").title()


def _read_title(project_dir: Path) -> str:
    readme_path = project_dir / "README.md"
    if not readme_path.exists():
        return _title_from_slug(project_dir.name)
    for line in readme_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return _title_from_slug(project_dir.name)


def _summary_from_readme(project_dir: Path) -> str:
    readme_path = project_dir / "README.md"
    if not readme_path.exists():
        return f"Learning portfolio project for {_title_from_slug(project_dir.name)}."
    lines = [line.strip() for line in readme_path.read_text(encoding="utf-8").splitlines()]
    for line in lines:
        if line and not line.startswith("#") and not line.startswith("```"):
            return line[:220]
    return f"Learning portfolio project for {_title_from_slug(project_dir.name)}."


def _is_generated_template(project_dir: Path) -> bool:
    config_path = project_dir / "src" / "config.py"
    if not config_path.exists():
        return False
    text = config_path.read_text(encoding="utf-8")
    return "projects._portfolio_common" in text or "ProjectSpec" in text


def _parse_scalar(value: str) -> str:
    value = value.strip()
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value


def _parse_project_yaml(path: Path) -> dict[str, Any]:
    """Parse the small YAML subset used by generated project metadata."""

    data: dict[str, Any] = {}
    current_key: str | None = None
    current_map: dict[str, str] | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()
        if indent == 0 and line.endswith(":"):
            current_key = line[:-1]
            if current_key == "commands":
                current_map = {}
                data[current_key] = current_map
            else:
                current_map = None
                data[current_key] = []
            continue
        if indent == 0 and ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = _parse_scalar(value)
            current_key = None
            current_map = None
            continue
        if current_key and line.startswith("- "):
            values = data.setdefault(current_key, [])
            if not isinstance(values, list):
                raise ValueError(f"Invalid list value for {current_key} in {path}")
            values.append(_parse_scalar(line[2:]))
            continue
        if current_map is not None and ":" in line:
            key, value = line.split(":", 1)
            current_map[key.strip()] = _parse_scalar(value)
            continue
        raise ValueError(f"Unsupported metadata line in {path}: {raw_line}")
    return data


def _tuple_field(metadata: dict[str, Any], key: str) -> tuple[str, ...]:
    value = metadata.get(key, ())
    if isinstance(value, str):
        return (value,)
    return tuple(str(item) for item in value)


def _record_from_metadata(project_dir: Path, metadata: dict[str, Any], fallback_id: str) -> ProjectRecord:
    slug = str(metadata.get("slug") or project_dir.name)
    return ProjectRecord(
        id=str(metadata.get("id") or fallback_id),
        slug=slug,
        title=str(metadata.get("title") or _read_title(project_dir)),
        summary=str(metadata.get("summary") or _summary_from_readme(project_dir)),
        tracks=_tuple_field(metadata, "tracks") or ("data_science",),
        difficulty=str(metadata.get("difficulty") or "intermediate"),
        domain=_tuple_field(metadata, "domain") or (infer_domain_group(slug),),
        skills=_tuple_field(metadata, "skills"),
        template=str(metadata.get("template") or ("generated_template" if _is_generated_template(project_dir) else "data_science_project")),
        maturity=str(metadata.get("maturity") or "active"),
        data_policy=str(metadata.get("data_policy") or "synthetic_or_sample"),
        artifacts=_tuple_field(metadata, "artifacts") or ("notebook", "pipeline"),
        commands=dict(metadata.get("commands") or {}),
        canonical_path=project_dir,
        learning_mission_ids=_tuple_field(metadata, "learning_missions"),
        legacy_paths=(project_dir,),
    )


def discover_project_records(projects_root: Path | None = None) -> list[ProjectRecord]:
    root = projects_root or _projects_root()
    records: list[ProjectRecord] = []
    for index, project_dir in enumerate(sorted(path for path in root.iterdir() if path.is_dir()), start=1):
        slug = project_dir.name
        if slug in _TAXONOMY_DIRS or slug.startswith("_"):
            continue
        metadata_path = project_dir / "project.yaml"
        fallback_id = f"p{index:03d}"
        metadata = _parse_project_yaml(metadata_path) if metadata_path.exists() else {}
        records.append(_record_from_metadata(project_dir, metadata, fallback_id=fallback_id))
    return records


def registry_by_slug(projects_root: Path | None = None) -> dict[str, ProjectRecord]:
    return {record.slug: record for record in discover_project_records(projects_root=projects_root)}


def registry_by_id(projects_root: Path | None = None) -> dict[str, ProjectRecord]:
    return {record.id: record for record in discover_project_records(projects_root=projects_root)}


def registry_aliases(projects_root: Path | None = None) -> dict[str, ProjectRecord]:
    aliases: dict[str, ProjectRecord] = {}
    for record in discover_project_records(projects_root=projects_root):
        aliases[record.id] = record
        aliases[record.slug] = record
    return aliases


def resolve_project(identifier: str, projects_root: Path | None = None) -> ProjectRecord:
    try:
        return registry_aliases(projects_root=projects_root)[identifier]
    except KeyError as exc:
        raise KeyError(f"Unknown project identifier: {identifier}") from exc


@dataclass(frozen=True, slots=True)
class RegistryValidationResult:
    """Validation summary for repository project metadata."""

    records: tuple[ProjectRecord, ...]
    duplicate_ids: tuple[str, ...]
    duplicate_slugs: tuple[str, ...]
    missing_metadata: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.duplicate_ids and not self.duplicate_slugs and not self.missing_metadata


def validate_registry(projects_root: Path | None = None) -> RegistryValidationResult:
    root = projects_root or _projects_root()
    records = tuple(discover_project_records(projects_root=root))
    ids = [record.id for record in records]
    slugs = [record.slug for record in records]
    missing = tuple(
        project_dir.name
        for project_dir in sorted(path for path in root.iterdir() if path.is_dir())
        if project_dir.name not in _TAXONOMY_DIRS and not project_dir.name.startswith("_") and not (project_dir / "project.yaml").exists()
    )
    return RegistryValidationResult(
        records=records,
        duplicate_ids=tuple(sorted({item for item in ids if ids.count(item) > 1})),
        duplicate_slugs=tuple(sorted({item for item in slugs if slugs.count(item) > 1})),
        missing_metadata=missing,
    )
