from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=11,
    slug='smart_building_thermal_dynamics_model',
    title='Smart Building Thermal Dynamics Model',
    description='Estimate indoor temperature evolution from open building energy datasets, occupancy proxies, and weather data.',
    theoretical_stack='Differential equations, control systems, thermal physics, time series regression, parameter estimation',
    domain='energy',
    task_kind='optimization',
    target_name='target_value',
    public_data_note='Mix public energy benchmarks with reproducible synthetic telemetry for offline runs.',
    random_seed=1740,
)
