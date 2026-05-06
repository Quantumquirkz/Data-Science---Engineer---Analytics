from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=68,
    slug='real_time_manufacturing_yield_dashboard',
    title='Real-Time Manufacturing Yield Dashboard',
    description='Build a dashboard for monitoring production yield, anomalies, and process drift.',
    theoretical_stack='statistical process control, visualization, streaming analytics, anomaly detection, quality engineering',
    domain='manufacturing',
    task_kind='anomaly',
    target_name='target_label',
    public_data_note='Uses synthetic process telemetry by default because production datasets are often proprietary.',
    random_seed=1797,
)
