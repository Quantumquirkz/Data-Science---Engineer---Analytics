from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=75,
    slug='dynamic_pricing_under_uncertainty',
    title='Dynamic Pricing Under Uncertainty',
    description='Optimize prices using historical demand and uncertain future conditions.',
    theoretical_stack='optimization, stochastic modeling, causal inference basics, reinforcement learning, econometrics',
    domain='finance',
    task_kind='optimization',
    target_name='target_value',
    public_data_note='Public-first when stable market samples are available; synthetic fallback for offline demos.',
    random_seed=1804,
)
