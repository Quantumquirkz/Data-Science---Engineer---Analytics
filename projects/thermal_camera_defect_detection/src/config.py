from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=59,
    slug='thermal_camera_defect_detection',
    title='Thermal Camera Defect Detection',
    description='Detect hidden structural or electrical defects from public thermal image datasets and benchmark inspection sequences.',
    theoretical_stack='Heat transfer intuition, image processing, anomaly detection, spatiotemporal modeling',
    domain='manufacturing',
    task_kind='anomaly',
    target_name='target_label',
    public_data_note='Uses synthetic process telemetry by default because production datasets are often proprietary.',
    random_seed=1788,
)
