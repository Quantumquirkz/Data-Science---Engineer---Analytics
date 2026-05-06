from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=88,
    slug='smart_farming_irrigation_optimizer',
    title='Smart Farming Irrigation Optimizer',
    description='Optimize irrigation schedules using open weather, soil moisture, and crop condition datasets or agricultural simulations.',
    theoretical_stack='control theory, optimization, environmental modeling, forecasting, decision systems',
    domain='environment',
    task_kind='forecasting',
    target_name='target_value',
    public_data_note='Public meteorological or geospatial data can be swapped in; default demo uses synthetic spatial fields.',
    random_seed=1817,
)
