from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=60,
    slug='large_scale_astronomy_catalog_linker',
    title='Large-Scale Astronomy Catalog Linker',
    description='Match records across multiple astronomical catalogs with uncertain coordinates and metadata.',
    theoretical_stack='Probabilistic matching, spherical geometry, indexing, record linkage, statistical inference',
    domain='astronomy',
    task_kind='knowledge_graph',
    target_name='target_value',
    public_data_note='Compatible with open astronomy archives; default table emulates noisy detector/catalog measurements.',
    random_seed=1789,
)
