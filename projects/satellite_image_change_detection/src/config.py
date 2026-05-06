from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=16,
    slug='satellite_image_change_detection',
    title='Satellite Image Change Detection',
    description='Detect land-use or environmental changes from multi-temporal satellite imagery.',
    theoretical_stack='Image processing, remote sensing, change detection, linear algebra, convolutional learning basics',
    domain='environment',
    task_kind='event_detection',
    target_name='target_label',
    public_data_note='Public meteorological or geospatial data can be swapped in; default demo uses synthetic spatial fields.',
    random_seed=1745,
)
