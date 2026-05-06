from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=12,
    slug='wind_turbine_failure_early_warning_system',
    title='Wind Turbine Failure Early Warning System',
    description='Predict turbine faults using public vibration, temperature, and rotational telemetry datasets from wind turbines or rotating machinery benchmarks.',
    theoretical_stack='Signal processing, spectral analysis, reliability theory, anomaly detection, supervised learning',
    domain='manufacturing',
    task_kind='forecasting',
    target_name='target_value',
    public_data_note='Uses synthetic process telemetry by default because production datasets are often proprietary.',
    random_seed=1741,
)
