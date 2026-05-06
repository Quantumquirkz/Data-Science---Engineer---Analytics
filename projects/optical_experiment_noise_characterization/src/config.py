from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=52,
    slug='optical_experiment_noise_characterization',
    title='Optical Experiment Noise Characterization',
    description='Quantify noise sources in repeated optical measurements and identify dominant contributors using openly published optics datasets or synthetic noise experiments.',
    theoretical_stack='Error analysis, statistical estimation, noise models, experimental physics methodology',
    domain='signal',
    task_kind='regression',
    target_name='target_value',
    public_data_note='Uses synthetic spectral/time-series measurements with documented public-data extension points.',
    random_seed=1781,
)
