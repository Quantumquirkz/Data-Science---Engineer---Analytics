from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=92,
    slug='large_scale_recommendation_for_learning_paths',
    title='Large-Scale Recommendation for Learning Paths',
    description='Recommend educational or research paths based on content similarity and user progress.',
    theoretical_stack='recommendation systems, embeddings, ranking, graph analytics, user modeling',
    domain='network',
    task_kind='event_detection',
    target_name='target_label',
    public_data_note='Uses generated graph/flow proxies by default; public logs or network datasets can be mapped into the same schema.',
    random_seed=1821,
)
