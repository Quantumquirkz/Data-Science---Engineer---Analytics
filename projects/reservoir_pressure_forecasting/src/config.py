from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=17,
    slug='reservoir_pressure_forecasting',
    title='Reservoir Pressure Forecasting',
    description='Predict pressure evolution in reservoirs using published extraction records, benchmark reservoir datasets, or synthetic sensor data.',
    theoretical_stack='Fluid mechanics basics, time series, regression, state estimation, Bayesian updating',
    domain='geoscience',
    task_kind='forecasting',
    target_name='target_value',
    public_data_note='Designed for public scientific repositories, with generated proxy fields for reproducibility.',
    random_seed=1746,
)
