from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=61,
    slug='human_mobility_pattern_clustering',
    title='Human Mobility Pattern Clustering',
    description='Discover mobility archetypes from GPS, transport card, or mobile telemetry data.',
    theoretical_stack='clustering, graph analytics, Markov models, geospatial analysis, dimensionality reduction',
    domain='network',
    task_kind='clustering',
    target_name='target_value',
    public_data_note='Uses generated graph/flow proxies by default; public logs or network datasets can be mapped into the same schema.',
    random_seed=1790,
)
