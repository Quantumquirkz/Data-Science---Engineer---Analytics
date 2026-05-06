from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=22,
    slug='experimental_physics_outlier_lab',
    title='Experimental Physics Outlier Lab',
    description='Build tools to identify suspicious measurements in repeated physics experiments using open lab datasets or synthetic repeated-measurement tables.',
    theoretical_stack='Error propagation, robust statistics, hypothesis testing, control charts, experimental uncertainty',
    domain='general',
    task_kind='anomaly',
    target_name='target_label',
    public_data_note='Uses a reproducible synthetic dataset by default, with public-data replacement points documented.',
    random_seed=1751,
)
