from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=46,
    slug='crop_yield_physics_and_data_model',
    title='Crop Yield Physics-and-Data Model',
    description='Estimate crop yield from weather, soil, and remote sensing variables.',
    theoretical_stack='Regression, spatial statistics, environmental modeling, uncertainty estimation, optimization',
    domain='environment',
    task_kind='regression',
    target_name='target_value',
    public_data_note='Public meteorological or geospatial data can be swapped in; default demo uses synthetic spatial fields.',
    random_seed=1775,
)
