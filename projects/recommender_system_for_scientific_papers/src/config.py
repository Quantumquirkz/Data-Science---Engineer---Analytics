from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=47,
    slug='recommender_system_for_scientific_papers',
    title='Recommender System for Scientific Papers',
    description='Recommend papers based on topic similarity, citation graph structure, and user interests.',
    theoretical_stack='Graph embeddings, information retrieval, NLP embeddings, ranking, recommendation systems',
    domain='network',
    task_kind='recommendation',
    target_name='target_label',
    public_data_note='Uses generated graph/flow proxies by default; public logs or network datasets can be mapped into the same schema.',
    random_seed=1776,
)
