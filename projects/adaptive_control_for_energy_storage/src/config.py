from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=94,
    slug='adaptive_control_for_energy_storage',
    title='Adaptive Control for Energy Storage',
    description='Develop a data-driven controller for charging and discharging battery storage systems using public battery benchmarks and simulated storage environments.',
    theoretical_stack='control theory, optimization, reinforcement learning, time series, dynamical systems',
    domain='energy',
    task_kind='optimization',
    target_name='target_value',
    public_data_note='Mix public energy benchmarks with reproducible synthetic telemetry for offline runs.',
    random_seed=1823,
)
