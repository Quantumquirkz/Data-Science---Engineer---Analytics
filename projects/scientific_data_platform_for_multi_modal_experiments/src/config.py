from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=100,
    slug='scientific_data_platform_for_multi_modal_experiments',
    title='Scientific Data Platform for Multi-Modal Experiments',
    description='Design a mini platform to ingest, organize, query, and analyze heterogeneous experiment data at scale using public multi-modal scientific datasets.',
    theoretical_stack='data engineering, schema design, distributed processing, metadata modeling, statistics, visualization',
    domain='manufacturing',
    task_kind='knowledge_graph',
    target_name='target_value',
    public_data_note='Uses synthetic process telemetry by default because production datasets are often proprietary.',
    random_seed=1829,
)
