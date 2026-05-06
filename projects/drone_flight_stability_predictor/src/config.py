from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=44,
    slug='drone_flight_stability_predictor',
    title='Drone Flight Stability Predictor',
    description='Predict unstable flight conditions from public drone flight logs, UAV benchmark datasets, or simulation telemetry.',
    theoretical_stack='Control systems, signal processing, dynamical systems, classification, time series forecasting',
    domain='manufacturing',
    task_kind='forecasting',
    target_name='target_value',
    public_data_note='Uses synthetic process telemetry by default because production datasets are often proprietary.',
    random_seed=1773,
)
