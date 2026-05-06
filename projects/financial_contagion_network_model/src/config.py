from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=53,
    slug='financial_contagion_network_model',
    title='Financial Contagion Network Model',
    description='Model propagation of distress across connected institutions using network data.',
    theoretical_stack='Graph theory, contagion models, systemic risk, stochastic modeling, simulation',
    domain='finance',
    task_kind='regression',
    target_name='target_value',
    public_data_note='Public-first when stable market samples are available; synthetic fallback for offline demos.',
    random_seed=1782,
)
