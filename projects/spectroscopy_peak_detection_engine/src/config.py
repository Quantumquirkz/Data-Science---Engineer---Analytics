from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=30,
    slug='spectroscopy_peak_detection_engine',
    title='Spectroscopy Peak Detection Engine',
    description='Detect and quantify peaks in spectroscopy signals for material or chemical analysis.',
    theoretical_stack='Signal smoothing, peak estimation, numerical optimization, noise modeling, spectral analysis',
    domain='signal',
    task_kind='event_detection',
    target_name='target_label',
    public_data_note='Uses synthetic spectral/time-series measurements with documented public-data extension points.',
    random_seed=1759,
)
