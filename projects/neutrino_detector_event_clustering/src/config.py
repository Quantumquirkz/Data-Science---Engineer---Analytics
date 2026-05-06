from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=45,
    slug='neutrino_detector_event_clustering',
    title='Neutrino Detector Event Clustering',
    description='Cluster detector events to separate noise from meaningful high-energy interactions.',
    theoretical_stack='Unsupervised learning, mixture models, rare event analysis, statistical physics intuition',
    domain='energy',
    task_kind='rare_event',
    target_name='target_label',
    public_data_note='Mix public energy benchmarks with reproducible synthetic telemetry for offline runs.',
    random_seed=1774,
)
