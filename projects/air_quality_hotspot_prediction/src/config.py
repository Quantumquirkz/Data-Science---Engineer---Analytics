from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=21,
    slug='air_quality_hotspot_prediction',
    title='Air Quality Hotspot Prediction',
    description='Predict pollution hotspots from meteorological, spatial, and traffic data.',
    theoretical_stack='Spatial modeling, diffusion intuition, regression, geostatistics, environmental analytics',
    domain='environment',
    task_kind='forecasting',
    target_name='target_value',
    public_data_note='Public meteorological or geospatial data can be swapped in; default demo uses synthetic spatial fields.',
    random_seed=1750,
)
