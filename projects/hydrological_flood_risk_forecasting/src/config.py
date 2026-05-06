from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=49,
    slug='hydrological_flood_risk_forecasting',
    title='Hydrological Flood Risk Forecasting',
    description='Forecast flood risk using rainfall, river level, and terrain information.',
    theoretical_stack='Time series, hydrology basics, spatial analysis, regression, extreme value statistics',
    domain='environment',
    task_kind='forecasting',
    target_name='target_value',
    public_data_note='Public meteorological or geospatial data can be swapped in; default demo uses synthetic spatial fields.',
    random_seed=1778,
)
