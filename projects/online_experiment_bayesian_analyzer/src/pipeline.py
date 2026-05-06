from __future__ import annotations

from pathlib import Path

from projects._portfolio_common import PipelineArtifacts, run_portfolio_pipeline
from .config import SPEC


def run_online_experiment_bayesian_analyzer_pipeline(
    project_root: Path,
    n_samples: int = 720,
    random_seed: int | None = None,
) -> PipelineArtifacts:
    return run_portfolio_pipeline(
        project_root=project_root,
        spec=SPEC,
        n_samples=n_samples,
        random_seed=random_seed,
    )


run_pipeline = run_online_experiment_bayesian_analyzer_pipeline
