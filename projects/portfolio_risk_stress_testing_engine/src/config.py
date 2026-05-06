from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=43,
    slug='portfolio_risk_stress_testing_engine',
    title='Portfolio Risk Stress Testing Engine',
    description='Build a framework to stress test portfolios under simulated macro and volatility shocks.',
    theoretical_stack='Probability, covariance modeling, Monte Carlo simulation, optimization, risk analytics',
    domain='finance',
    task_kind='simulation',
    target_name='target_value',
    public_data_note='Public-first when stable market samples are available; synthetic fallback for offline demos.',
    random_seed=1772,
)
