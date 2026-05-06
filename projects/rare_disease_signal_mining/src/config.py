from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=84,
    slug='rare_disease_signal_mining',
    title='Rare Disease Signal Mining',
    description='Detect weak disease signals in very imbalanced healthcare or genomic datasets.',
    theoretical_stack='imbalanced learning, rare event statistics, feature selection, probabilistic modeling',
    domain='biomedical',
    task_kind='rare_event',
    target_name='target_label',
    public_data_note='Uses privacy-safe synthetic proxies by default; public biomedical datasets can replace the source table.',
    random_seed=1813,
)
