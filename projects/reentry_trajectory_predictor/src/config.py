from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=69,
    slug='reentry_trajectory_predictor',
    title='Reentry Trajectory Predictor',
    description='Predict reentry trajectories under uncertain atmospheric drag conditions.',
    theoretical_stack='mechanics, numerical integration, stochastic uncertainty, state estimation, simulation',
    domain='geoscience',
    task_kind='forecasting',
    target_name='target_value',
    public_data_note='Designed for public scientific repositories, with generated proxy fields for reproducibility.',
    random_seed=1798,
)
