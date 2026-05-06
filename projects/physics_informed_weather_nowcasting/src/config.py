from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=73,
    slug='physics_informed_weather_nowcasting',
    title='Physics-Informed Weather Nowcasting',
    description='Combine short-term radar observations with physical priors to improve nowcasting using open meteorological radar datasets.',
    theoretical_stack='spatiotemporal forecasting, PDE intuition, data assimilation, deep learning, uncertainty estimation',
    domain='environment',
    task_kind='forecasting',
    target_name='target_value',
    public_data_note='Public meteorological or geospatial data can be swapped in; default demo uses synthetic spatial fields.',
    random_seed=1802,
)
