from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=19,
    slug='ocean_buoy_wave_energy_estimator',
    title='Ocean Buoy Wave Energy Estimator',
    description='Estimate wave energy potential from open buoy measurements and environmental signals from oceanographic repositories.',
    theoretical_stack='Spectral analysis, stochastic wave modeling, signal decomposition, regression, ocean dynamics basics',
    domain='energy',
    task_kind='regression',
    target_name='target_value',
    public_data_note='Mix public energy benchmarks with reproducible synthetic telemetry for offline runs.',
    random_seed=1748,
)
