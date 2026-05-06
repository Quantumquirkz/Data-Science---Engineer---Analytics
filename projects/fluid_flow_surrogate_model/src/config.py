from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=6,
    slug='fluid_flow_surrogate_model',
    title='Fluid Flow Surrogate Model',
    description='Train a machine learning model to approximate outputs of expensive fluid dynamics simulations.',
    theoretical_stack='Numerical methods, surrogate modeling, interpolation, regression, dimensionality reduction, computational fluid dynamics intuition',
    domain='simulation',
    task_kind='regression',
    target_name='target_value',
    public_data_note='Simulation-first project with reproducible stochastic scenarios.',
    random_seed=1735,
)
