from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=29,
    slug='large_scale_sensor_missing_data_imputation',
    title='Large-Scale Sensor Missing Data Imputation',
    description='Impute missing values across thousands of sensor streams with temporal and spatial structure using public IoT, weather, or industrial telemetry datasets.',
    theoretical_stack='Matrix completion, time series interpolation, probabilistic modeling, optimization, low-rank approximation',
    domain='environment',
    task_kind='reconstruction',
    target_name='target_value',
    public_data_note='Public meteorological or geospatial data can be swapped in; default demo uses synthetic spatial fields.',
    random_seed=1758,
)
