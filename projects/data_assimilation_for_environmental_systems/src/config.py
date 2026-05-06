from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=87,
    slug='data_assimilation_for_environmental_systems',
    title='Data Assimilation for Environmental Systems',
    description='Fuse simulation outputs and observed data to improve state estimation.',
    theoretical_stack='Kalman filtering, Bayesian inference, differential equations, uncertainty propagation, state-space models',
    domain='environment',
    task_kind='reconstruction',
    target_name='target_value',
    public_data_note='Public meteorological or geospatial data can be swapped in; default demo uses synthetic spatial fields.',
    random_seed=1816,
)
