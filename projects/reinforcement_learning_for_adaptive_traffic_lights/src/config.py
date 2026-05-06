from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=33,
    slug='reinforcement_learning_for_adaptive_traffic_lights',
    title='Reinforcement Learning for Adaptive Traffic Lights',
    description='Train an adaptive system to optimize urban traffic signal timing.',
    theoretical_stack='Markov decision processes, optimization, control theory, reinforcement learning, simulation design',
    domain='manufacturing',
    task_kind='optimization',
    target_name='target_value',
    public_data_note='Uses synthetic process telemetry by default because production datasets are often proprietary.',
    random_seed=1762,
)
