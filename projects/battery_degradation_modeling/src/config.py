from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=20,
    slug='battery_degradation_modeling',
    title='Battery Degradation Modeling',
    description='Predict battery health and remaining useful life from public battery cycle datasets collected in prior experiments.',
    theoretical_stack='Electrochemistry intuition, survival analysis, time series, regression, degradation modeling, uncertainty quantification',
    domain='energy',
    task_kind='forecasting',
    target_name='target_value',
    public_data_note='Mix public energy benchmarks with reproducible synthetic telemetry for offline runs.',
    random_seed=1749,
)
