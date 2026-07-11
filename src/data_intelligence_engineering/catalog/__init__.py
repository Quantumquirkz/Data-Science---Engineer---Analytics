"""Catalog metadata for repository projects."""

from .project_registry import (
    FEATURED_PROJECTS,
    discover_project_records,
    registry_aliases,
    registry_by_id,
    registry_by_slug,
    resolve_project,
    validate_registry,
)
from .schemas import ProjectRecord, ProjectSpec

__all__ = [
    "FEATURED_PROJECTS",
    "ProjectRecord",
    "ProjectSpec",
    "discover_project_records",
    "registry_aliases",
    "registry_by_id",
    "registry_by_slug",
    "resolve_project",
    "validate_registry",
]
