from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=42,
    slug='ocean_current_field_compression',
    title='Ocean Current Field Compression',
    description='Compress and reconstruct ocean current fields from massive spatiotemporal datasets.',
    theoretical_stack='PCA, tensor decomposition, dimensionality reduction, numerical approximation, fluid dynamics intuition',
    domain='geoscience',
    task_kind='compression',
    target_name='target_value',
    public_data_note='Designed for public scientific repositories, with generated proxy fields for reproducibility.',
    random_seed=1771,
)
