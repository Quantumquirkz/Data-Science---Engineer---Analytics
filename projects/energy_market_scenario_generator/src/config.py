from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=83,
    slug='energy_market_scenario_generator',
    title='Energy Market Scenario Generator',
    description='Generate plausible future energy market scenarios from historical and exogenous variables.',
    theoretical_stack='stochastic simulation, scenario analysis, time series modeling, optimization, market analytics',
    domain='finance',
    task_kind='regression',
    target_name='target_value',
    public_data_note='Public-first when stable market samples are available; synthetic fallback for offline demos.',
    random_seed=1812,
)
