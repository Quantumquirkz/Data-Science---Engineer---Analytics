from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=65,
    slug='online_experiment_bayesian_analyzer',
    title='Online Experiment Bayesian Analyzer',
    description='Build a Bayesian analytics tool for A/B tests with streaming observations.',
    theoretical_stack='Bayesian inference, posterior updating, decision theory, sequential analysis, experimentation',
    domain='general',
    task_kind='regression',
    target_name='target_value',
    public_data_note='Uses a reproducible synthetic dataset by default, with public-data replacement points documented.',
    random_seed=1794,
)
