from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=70,
    slug='demand_forecasting_for_cold_chain_logistics',
    title='Demand Forecasting for Cold Chain Logistics',
    description='Forecast demand and spoilage risk in temperature-sensitive supply chains.',
    theoretical_stack='time series, optimization, survival analysis, operations research, uncertainty modeling',
    domain='network',
    task_kind='forecasting',
    target_name='target_value',
    public_data_note='Uses generated graph/flow proxies by default; public logs or network datasets can be mapped into the same schema.',
    random_seed=1799,
)
