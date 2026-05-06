from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=77,
    slug='blood_flow_proxy_prediction',
    title='Blood Flow Proxy Prediction',
    description='Predict blood flow metrics from partial physiological measurements using public biomedical datasets or simulation outputs.',
    theoretical_stack='fluid dynamics intuition, inverse problems, regression, uncertainty quantification, biomedical modeling',
    domain='biomedical',
    task_kind='forecasting',
    target_name='target_value',
    public_data_note='Uses privacy-safe synthetic proxies by default; public biomedical datasets can replace the source table.',
    random_seed=1806,
)
