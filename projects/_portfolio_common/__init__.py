"""Compatibility layer for generated portfolio projects."""

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from data_intelligence_engineering.catalog.schemas import ProjectSpec
from data_intelligence_engineering.core.pipeline import PipelineArtifacts, run_portfolio_pipeline

__all__ = ["PipelineArtifacts", "ProjectSpec", "run_portfolio_pipeline"]
