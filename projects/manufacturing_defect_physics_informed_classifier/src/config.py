from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=26,
    slug='manufacturing_defect_physics_informed_classifier',
    title='Manufacturing Defect Physics-Informed Classifier',
    description='Classify defects in production lines while incorporating process physics constraints using manufacturing benchmark datasets or image archives.',
    theoretical_stack='Classification, constrained optimization, process control, signal features, domain-informed ML',
    domain='manufacturing',
    task_kind='classification',
    target_name='target_label',
    public_data_note='Uses synthetic process telemetry by default because production datasets are often proprietary.',
    random_seed=1755,
)
