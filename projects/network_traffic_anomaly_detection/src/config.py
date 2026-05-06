from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=9,
    slug='network_traffic_anomaly_detection',
    title='Network Traffic Anomaly Detection',
    description='Detect suspicious traffic spikes or abnormal communication patterns in large-scale network logs.',
    theoretical_stack='Graph theory, anomaly detection, information theory, clustering, streaming algorithms, statistical monitoring',
    domain='network',
    task_kind='anomaly',
    target_name='target_label',
    public_data_note='Uses generated graph/flow proxies by default; public logs or network datasets can be mapped into the same schema.',
    random_seed=1738,
)
