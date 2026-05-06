from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=50,
    slug='electromagnetic_interference_pattern_detector',
    title='Electromagnetic Interference Pattern Detector',
    description='Detect interference patterns in electronic systems using frequency-domain data.',
    theoretical_stack='Fourier transforms, spectral analysis, classification, filtering, electromagnetism basics',
    domain='geoscience',
    task_kind='event_detection',
    target_name='target_label',
    public_data_note='Designed for public scientific repositories, with generated proxy fields for reproducibility.',
    random_seed=1779,
)
