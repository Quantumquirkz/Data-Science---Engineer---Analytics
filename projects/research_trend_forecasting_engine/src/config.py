from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=95,
    slug='research_trend_forecasting_engine',
    title='Research Trend Forecasting Engine',
    description='Forecast emerging research topics from publication, citation, and keyword networks.',
    theoretical_stack='time series, graph mining, NLP, trend analysis, probabilistic forecasting',
    domain='network',
    task_kind='forecasting',
    target_name='target_value',
    public_data_note='Uses generated graph/flow proxies by default; public logs or network datasets can be mapped into the same schema.',
    random_seed=1824,
)
