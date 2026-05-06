from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=79,
    slug='large_scale_text_mining_of_scientific_literature',
    title='Large-Scale Text Mining of Scientific Literature',
    description='Extract themes, trends, and emerging concepts from thousands of scientific papers.',
    theoretical_stack='NLP, topic modeling, embeddings, dimensionality reduction, information retrieval',
    domain='general',
    task_kind='forecasting',
    target_name='target_value',
    public_data_note='Uses a reproducible synthetic dataset by default, with public-data replacement points documented.',
    random_seed=1808,
)
