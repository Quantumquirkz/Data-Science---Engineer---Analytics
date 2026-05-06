from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=81,
    slug='particle_collision_feature_extraction_pipeline',
    title='Particle Collision Feature Extraction Pipeline',
    description='Build a scalable pipeline to preprocess and analyze high-energy collision event features.',
    theoretical_stack='feature engineering, distributed analytics, dimensionality reduction, classification, particle physics intuition',
    domain='energy',
    task_kind='regression',
    target_name='target_value',
    public_data_note='Mix public energy benchmarks with reproducible synthetic telemetry for offline runs.',
    random_seed=1810,
)
