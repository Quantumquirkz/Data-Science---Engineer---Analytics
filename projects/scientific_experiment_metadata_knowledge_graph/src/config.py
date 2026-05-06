from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=76,
    slug='scientific_experiment_metadata_knowledge_graph',
    title='Scientific Experiment Metadata Knowledge Graph',
    description='Build a knowledge graph linking experiments, instruments, variables, and outcomes from published papers, open metadata, and public repositories.',
    theoretical_stack='graph theory, ontology design, information retrieval, data modeling, graph analytics',
    domain='network',
    task_kind='knowledge_graph',
    target_name='target_value',
    public_data_note='Uses generated graph/flow proxies by default; public logs or network datasets can be mapped into the same schema.',
    random_seed=1805,
)
