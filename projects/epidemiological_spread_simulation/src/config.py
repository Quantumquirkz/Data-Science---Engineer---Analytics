from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=32,
    slug='epidemiological_spread_simulation',
    title='Epidemiological Spread Simulation',
    description='Model and analyze disease spread using compartmental and network approaches.',
    theoretical_stack='Differential equations, graph theory, stochastic simulation, parameter estimation, causal reasoning',
    domain='biomedical',
    task_kind='regression',
    target_name='target_value',
    public_data_note='Uses privacy-safe synthetic proxies by default; public biomedical datasets can replace the source table.',
    random_seed=1761,
)
