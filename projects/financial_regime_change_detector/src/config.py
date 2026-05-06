from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=90,
    slug='financial_regime_change_detector',
    title='Financial Regime Change Detector',
    description='Detect transitions between market regimes using multivariate market signals.',
    theoretical_stack='hidden Markov models, time series, change-point detection, probabilistic inference',
    domain='finance',
    task_kind='event_detection',
    target_name='target_label',
    public_data_note='Public-first when stable market samples are available; synthetic fallback for offline demos.',
    random_seed=1819,
)
