from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=28,
    slug='fraud_detection_in_scientific_grant_data',
    title='Fraud Detection in Scientific Grant Data',
    description='Detect suspicious funding patterns and anomalies in grant allocation datasets.',
    theoretical_stack='Graph analytics, anomaly detection, statistical inference, network analysis, explainable ML',
    domain='network',
    task_kind='anomaly',
    target_name='target_label',
    public_data_note='Uses generated graph/flow proxies by default; public logs or network datasets can be mapped into the same schema.',
    random_seed=1757,
)
