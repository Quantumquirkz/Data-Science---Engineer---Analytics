from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=7,
    slug='atmospheric_pressure_anomaly_mapper',
    title='Atmospheric Pressure Anomaly Mapper',
    description='Identify and visualize unusual pressure systems using large meteorological datasets.',
    theoretical_stack='Spatial statistics, interpolation, geostatistics, clustering, anomaly detection, atmospheric physics',
    domain='geoscience',
    task_kind='anomaly',
    target_name='target_label',
    public_data_note='Designed for public scientific repositories, with generated proxy fields for reproducibility.',
    random_seed=1736,
)
