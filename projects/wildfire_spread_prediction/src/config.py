from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=63,
    slug='wildfire_spread_prediction',
    title='Wildfire Spread Prediction',
    description='Predict the likely spread of wildfires using weather, terrain, and vegetation data.',
    theoretical_stack='dynamical systems, PDE intuition, spatial modeling, probabilistic forecasting, environmental science',
    domain='environment',
    task_kind='forecasting',
    target_name='target_value',
    public_data_note='Public meteorological or geospatial data can be swapped in; default demo uses synthetic spatial fields.',
    random_seed=1792,
)
