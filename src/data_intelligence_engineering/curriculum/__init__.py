"""Curriculum indexing helpers for role-based learning paths."""

from .index import TRACKS
from .index import discover_levels
from .index import level_matrix
from .index import levels_by_track
from .index import load_mission_registry
from .index import missions_by_track_level
from .index import missions_for_project
from .index import projects_by_template
from .index import projects_by_track
from .index import validate_curriculum

__all__ = [
    "TRACKS",
    "discover_levels",
    "level_matrix",
    "levels_by_track",
    "load_mission_registry",
    "missions_by_track_level",
    "missions_for_project",
    "projects_by_template",
    "projects_by_track",
    "validate_curriculum",
]
