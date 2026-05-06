from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=40,
    slug='warehouse_robotics_path_optimization',
    title='Warehouse Robotics Path Optimization',
    description='Optimize robot routing and collision avoidance in a warehouse environment using simulated layouts, public routing benchmarks, or synthetic traffic data.',
    theoretical_stack='Graph search, combinatorial optimization, control, reinforcement learning, geometry',
    domain='network',
    task_kind='optimization',
    target_name='target_value',
    public_data_note='Uses generated graph/flow proxies by default; public logs or network datasets can be mapped into the same schema.',
    random_seed=1769,
)
