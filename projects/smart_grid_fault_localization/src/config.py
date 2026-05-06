from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=97,
    slug='smart_grid_fault_localization',
    title='Smart Grid Fault Localization',
    description='Localize likely faults in a smart grid using public power system benchmarks, simulated grids, and sparse telemetry logs.',
    theoretical_stack='graph inference, state estimation, optimization, signal analysis, electrical systems intuition',
    domain='energy',
    task_kind='anomaly',
    target_name='target_label',
    public_data_note='Mix public energy benchmarks with reproducible synthetic telemetry for offline runs.',
    random_seed=1826,
)
