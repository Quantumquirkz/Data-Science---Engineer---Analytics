from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=15,
    slug='protein_folding_embedding_explorer',
    title='Protein Folding Embedding Explorer',
    description='Analyze high-dimensional protein representations and cluster structural patterns.',
    theoretical_stack='Geometry in high dimensions, manifold learning, dimensionality reduction, clustering, bioinformatics data analysis',
    domain='biomedical',
    task_kind='clustering',
    target_name='target_value',
    public_data_note='Uses privacy-safe synthetic proxies by default; public biomedical datasets can replace the source table.',
    random_seed=1744,
)
