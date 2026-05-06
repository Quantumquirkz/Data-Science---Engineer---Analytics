from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=23,
    slug='energy_consumption_segmentation',
    title='Energy Consumption Segmentation',
    description='Cluster households or facilities based on their energy-use signatures.',
    theoretical_stack='Clustering, distance metrics, dimensionality reduction, time series features, unsupervised learning',
    domain='energy',
    task_kind='segmentation',
    target_name='target_label',
    public_data_note='Mix public energy benchmarks with reproducible synthetic telemetry for offline runs.',
    random_seed=1752,
)
