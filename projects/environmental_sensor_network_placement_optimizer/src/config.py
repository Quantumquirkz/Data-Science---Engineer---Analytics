from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=78,
    slug='environmental_sensor_network_placement_optimizer',
    title='Environmental Sensor Network Placement Optimizer',
    description='Optimize where sensors should be placed to maximize information coverage using simulated environments or public geospatial layers rather than deploying hardware.',
    theoretical_stack='information theory, combinatorial optimization, spatial statistics, experimental design',
    domain='environment',
    task_kind='optimization',
    target_name='target_value',
    public_data_note='Public meteorological or geospatial data can be swapped in; default demo uses synthetic spatial fields.',
    random_seed=1807,
)
