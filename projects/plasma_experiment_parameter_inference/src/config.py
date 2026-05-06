from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=57,
    slug='plasma_experiment_parameter_inference',
    title='Plasma Experiment Parameter Inference',
    description='Infer plasma model parameters from published observational datasets, open tokamak benchmarks, or simulated measurements.',
    theoretical_stack='Inverse problems, nonlinear optimization, differential equations, uncertainty quantification',
    domain='general',
    task_kind='simulation',
    target_name='target_value',
    public_data_note='Uses a reproducible synthetic dataset by default, with public-data replacement points documented.',
    random_seed=1786,
)
