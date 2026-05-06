from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=98,
    slug='autonomous_vehicle_sensor_fusion_project',
    title='Autonomous Vehicle Sensor Fusion Project',
    description='Fuse camera, LiDAR, GPS, and inertial data for improved localization or perception using autonomous driving benchmark datasets rather than collecting sensor data yourself.',
    theoretical_stack='Bayesian fusion, Kalman filters, geometry, computer vision, probabilistic robotics',
    domain='robotics',
    task_kind='regression',
    target_name='target_value',
    public_data_note='Uses simulated telemetry by default; benchmark logs can be adapted later.',
    random_seed=1827,
)
