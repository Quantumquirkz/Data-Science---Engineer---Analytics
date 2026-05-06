from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=8,
    slug='high_frequency_trading_microstructure_analyzer',
    title='High-Frequency Trading Microstructure Analyzer',
    description='Analyze order book dynamics and price micro-movements from tick-level market data.',
    theoretical_stack='Stochastic processes, time series, queueing intuition, statistical inference, market microstructure, algorithmic data processing',
    domain='finance',
    task_kind='regression',
    target_name='target_value',
    public_data_note='Public-first when stable market samples are available; synthetic fallback for offline demos.',
    random_seed=1737,
)
