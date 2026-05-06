from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=72,
    slug='multi_agent_evacuation_simulation',
    title='Multi-Agent Evacuation Simulation',
    description='Simulate evacuation dynamics in buildings or stadiums under different constraints.',
    theoretical_stack='agent-based modeling, graph search, crowd dynamics, optimization, simulation',
    domain='network',
    task_kind='simulation',
    target_name='target_value',
    public_data_note='Uses generated graph/flow proxies by default; public logs or network datasets can be mapped into the same schema.',
    random_seed=1801,
)
