from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=39,
    slug='supply_chain_as_a_dynamic_network',
    title='Supply Chain as a Dynamic Network',
    description='Model supply chain disruptions and flow optimization under uncertainty.',
    theoretical_stack='Graph theory, optimization, stochastic modeling, network flow, operations research',
    domain='network',
    task_kind='event_detection',
    target_name='target_label',
    public_data_note='Uses generated graph/flow proxies by default; public logs or network datasets can be mapped into the same schema.',
    random_seed=1768,
)
