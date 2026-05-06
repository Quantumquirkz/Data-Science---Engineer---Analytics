from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=25,
    slug='weather_front_boundary_detection',
    title='Weather Front Boundary Detection',
    description='Detect moving weather fronts from gridded atmospheric data.',
    theoretical_stack='Gradient fields, numerical differentiation, image segmentation, spatial statistics, meteorological modeling',
    domain='energy',
    task_kind='segmentation',
    target_name='target_label',
    public_data_note='Mix public energy benchmarks with reproducible synthetic telemetry for offline runs.',
    random_seed=1754,
)
