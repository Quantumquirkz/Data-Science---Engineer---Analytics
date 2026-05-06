from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=86,
    slug='computational_topology_for_data_shapes',
    title='Computational Topology for Data Shapes',
    description='Study the shape of high-dimensional datasets using topological summaries.',
    theoretical_stack='topology, geometry, persistent homology intuition, manifold learning, unsupervised analysis',
    domain='general',
    task_kind='regression',
    target_name='target_value',
    public_data_note='Uses a reproducible synthetic dataset by default, with public-data replacement points documented.',
    random_seed=1815,
)
