from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=96,
    slug='high_dimensional_feature_selection_lab',
    title='High-Dimensional Feature Selection Lab',
    description='Build and compare feature selection pipelines for wide datasets with many correlated variables.',
    theoretical_stack='linear algebra, regularization, information theory, statistical learning, model selection',
    domain='general',
    task_kind='regression',
    target_name='target_value',
    public_data_note='Uses a reproducible synthetic dataset by default, with public-data replacement points documented.',
    random_seed=1825,
)
