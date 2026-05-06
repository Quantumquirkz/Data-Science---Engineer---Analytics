from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=71,
    slug='urban_heat_island_analysis',
    title='Urban Heat Island Analysis',
    description='Quantify and predict urban heat island intensity from spatial and weather data.',
    theoretical_stack='spatial statistics, heat transfer intuition, regression, geospatial analytics, environmental physics',
    domain='environment',
    task_kind='forecasting',
    target_name='target_value',
    public_data_note='Public meteorological or geospatial data can be swapped in; default demo uses synthetic spatial fields.',
    random_seed=1800,
)
