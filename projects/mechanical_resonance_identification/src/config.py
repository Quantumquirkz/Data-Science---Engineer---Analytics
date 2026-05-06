from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=64,
    slug='mechanical_resonance_identification',
    title='Mechanical Resonance Identification',
    description='Identify resonant frequencies in large collections of vibration signals.',
    theoretical_stack='spectral analysis, Fourier transforms, peak detection, statistical testing, mechanical systems',
    domain='signal',
    task_kind='event_detection',
    target_name='target_label',
    public_data_note='Uses synthetic spectral/time-series measurements with documented public-data extension points.',
    random_seed=1793,
)
