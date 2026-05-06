from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=36,
    slug='financial_volatility_surface_predictor',
    title='Financial Volatility Surface Predictor',
    description='Model volatility surfaces from options market data.',
    theoretical_stack='Stochastic calculus, interpolation, regression, optimization, quantitative finance modeling',
    domain='finance',
    task_kind='forecasting',
    target_name='target_value',
    public_data_note='Public-first when stable market samples are available; synthetic fallback for offline demos.',
    random_seed=1765,
)
