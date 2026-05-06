from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=14,
    slug='magnetic_field_sensor_reconstruction',
    title='Magnetic Field Sensor Reconstruction',
    description='Reconstruct missing or corrupted magnetic field measurements from open magnetic observatory records or simulated distributed sensor data.',
    theoretical_stack='Inverse problems, interpolation, linear algebra, regularization, electromagnetic field basics',
    domain='geoscience',
    task_kind='simulation',
    target_name='target_value',
    public_data_note='Designed for public scientific repositories, with generated proxy fields for reproducibility.',
    random_seed=1743,
)
