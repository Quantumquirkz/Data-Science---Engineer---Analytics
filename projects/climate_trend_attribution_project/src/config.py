from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=37,
    slug='climate_trend_attribution_project',
    title='Climate Trend Attribution Project',
    description='Separate long-term climate trends from seasonal and random effects in large datasets.',
    theoretical_stack='Statistical decomposition, hypothesis testing, regression, time series, environmental inference',
    domain='environment',
    task_kind='forecasting',
    target_name='target_value',
    public_data_note='Public meteorological or geospatial data can be swapped in; default demo uses synthetic spatial fields.',
    random_seed=1766,
)
