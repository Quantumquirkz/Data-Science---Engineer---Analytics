from __future__ import annotations

from dataclasses import dataclass


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
