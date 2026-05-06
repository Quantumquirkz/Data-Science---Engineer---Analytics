from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=62,
    slug='seafloor_mapping_interpolation_project',
    title='Seafloor Mapping Interpolation Project',
    description='Reconstruct seafloor depth maps from public bathymetry datasets and sparse sonar benchmark measurements.',
    theoretical_stack='interpolation, inverse problems, spatial statistics, numerical approximation, geophysical modeling',
    domain='geoscience',
    task_kind='reconstruction',
    target_name='target_value',
    public_data_note='Designed for public scientific repositories, with generated proxy fields for reproducibility.',
    random_seed=1791,
)
