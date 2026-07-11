"""Shared repository infrastructure for data-intelligence-engineering."""

from .catalog.project_registry import (
    FEATURED_PROJECTS,
    discover_project_records,
    registry_aliases,
    registry_by_id,
    registry_by_slug,
    resolve_project,
    validate_registry,
)
from .catalog.schemas import ProjectRecord, ProjectSpec
from .core.pipeline import PipelineArtifacts, run_portfolio_pipeline

__all__ = [
    "FEATURED_PROJECTS",
    "PipelineArtifacts",
    "ProjectRecord",
    "ProjectSpec",
    "discover_project_records",
    "registry_aliases",
    "registry_by_id",
    "registry_by_slug",
    "resolve_project",
    "run_portfolio_pipeline",
    "validate_registry",
]
