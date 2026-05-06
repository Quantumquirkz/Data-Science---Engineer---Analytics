from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=48,
    slug='semiconductor_process_variation_analyzer',
    title='Semiconductor Process Variation Analyzer',
    description='Analyze manufacturing variation and defect propagation in semiconductor process data.',
    theoretical_stack='Statistical quality control, multivariate analysis, anomaly detection, process modeling',
    domain='manufacturing',
    task_kind='anomaly',
    target_name='target_label',
    public_data_note='Uses synthetic process telemetry by default because production datasets are often proprietary.',
    random_seed=1777,
)
