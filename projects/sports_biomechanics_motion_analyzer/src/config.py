from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=35,
    slug='sports_biomechanics_motion_analyzer',
    title='Sports Biomechanics Motion Analyzer',
    description='Analyze athlete motion capture or wearable sensor benchmark data to detect inefficiencies or injury risk without collecting new hardware signals.',
    theoretical_stack='Mechanics, kinematics, multivariate statistics, time series analysis, classification',
    domain='biomedical',
    task_kind='event_detection',
    target_name='target_label',
    public_data_note='Uses privacy-safe synthetic proxies by default; public biomedical datasets can replace the source table.',
    random_seed=1764,
)
