from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=85,
    slug='structural_health_monitoring_platform',
    title='Structural Health Monitoring Platform',
    description='Monitor bridges or buildings using public structural health monitoring datasets with strain, vibration, and displacement measurements.',
    theoretical_stack='mechanics, time series, signal processing, anomaly detection, reliability theory',
    domain='manufacturing',
    task_kind='anomaly',
    target_name='target_label',
    public_data_note='Uses synthetic process telemetry by default because production datasets are often proprietary.',
    random_seed=1814,
)
