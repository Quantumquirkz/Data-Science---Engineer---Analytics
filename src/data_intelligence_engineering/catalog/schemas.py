from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ProjectSpec:
    """Configuration that makes one portfolio project domain-specific."""

    number: int
    slug: str
    title: str
    description: str
    theoretical_stack: str
    domain: str
    task_kind: str
    target_name: str
    public_data_note: str
    random_seed: int


@dataclass(frozen=True, slots=True)
class ProjectRecord:
    """Machine-readable metadata for one project in the repository."""

    id: str
    slug: str
    title: str
    summary: str
    tracks: tuple[str, ...]
    difficulty: str
    domain: tuple[str, ...]
    skills: tuple[str, ...]
    template: str
    maturity: str
    data_policy: str
    artifacts: tuple[str, ...]
    commands: dict[str, str]
    canonical_path: Path
    learning_mission_ids: tuple[str, ...] = ()
    legacy_paths: tuple[Path, ...] = ()

    @property
    def domain_group(self) -> str:
        """Compatibility alias for older catalog code."""

        return self.domain[0] if self.domain else "industrial_analytics"

    @property
    def template_type(self) -> str:
        """Compatibility alias for older catalog code."""

        return self.template
