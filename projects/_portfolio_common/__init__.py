"""Shared machinery for generated portfolio projects."""

from .spec import ProjectSpec
from .pipeline import PipelineArtifacts, run_portfolio_pipeline

__all__ = ["PipelineArtifacts", "ProjectSpec", "run_portfolio_pipeline"]
