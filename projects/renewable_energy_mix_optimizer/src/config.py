from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=54,
    slug='renewable_energy_mix_optimizer',
    title='Renewable Energy Mix Optimizer',
    description='Optimize the allocation of solar, wind, and storage resources over time.',
    theoretical_stack='Linear programming, stochastic optimization, energy systems, forecasting, constraints modeling',
    domain='energy',
    task_kind='forecasting',
    target_name='target_value',
    public_data_note='Mix public energy benchmarks with reproducible synthetic telemetry for offline runs.',
    random_seed=1783,
)
