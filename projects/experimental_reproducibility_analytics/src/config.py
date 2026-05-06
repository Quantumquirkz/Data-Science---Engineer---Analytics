from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=99,
    slug='experimental_reproducibility_analytics',
    title='Experimental Reproducibility Analytics',
    description='Analyze repeated experiments to quantify reproducibility and hidden variability using open scientific datasets with repeated trials.',
    theoretical_stack='variance decomposition, statistical inference, uncertainty quantification, experimental design',
    domain='general',
    task_kind='regression',
    target_name='target_value',
    public_data_note='Uses a reproducible synthetic dataset by default, with public-data replacement points documented.',
    random_seed=1828,
)
