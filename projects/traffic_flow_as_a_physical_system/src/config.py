from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=13,
    slug='traffic_flow_as_a_physical_system',
    title='Traffic Flow as a Physical System',
    description='Study urban traffic as a dynamical system and predict congestion patterns.',
    theoretical_stack='Dynamical systems, PDE intuition, graph theory, optimization, time series modeling, simulation',
    domain='network',
    task_kind='forecasting',
    target_name='target_value',
    public_data_note='Uses generated graph/flow proxies by default; public logs or network datasets can be mapped into the same schema.',
    random_seed=1742,
)
