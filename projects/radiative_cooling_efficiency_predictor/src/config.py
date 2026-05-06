from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=10,
    slug='radiative_cooling_efficiency_predictor',
    title='Radiative Cooling Efficiency Predictor',
    description='Model cooling performance of materials under varying thermal and radiative conditions using published experimental datasets or simulation outputs.',
    theoretical_stack='Heat transfer, radiative physics, regression, optimization, uncertainty analysis, experimental modeling',
    domain='simulation',
    task_kind='forecasting',
    target_name='target_value',
    public_data_note='Simulation-first project with reproducible stochastic scenarios.',
    random_seed=1739,
)
