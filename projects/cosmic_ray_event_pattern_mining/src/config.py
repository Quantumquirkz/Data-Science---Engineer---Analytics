from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=18,
    slug='cosmic_ray_event_pattern_mining',
    title='Cosmic Ray Event Pattern Mining',
    description='Mine rare-event patterns from large astrophysics detector logs.',
    theoretical_stack='Poisson processes, rare event statistics, outlier detection, pattern mining, experimental physics data analysis',
    domain='astronomy',
    task_kind='rare_event',
    target_name='target_label',
    public_data_note='Compatible with open astronomy archives; default table emulates noisy detector/catalog measurements.',
    random_seed=1747,
)
