from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=51,
    slug='large_scale_log_compression_and_analytics',
    title='Large-Scale Log Compression and Analytics',
    description='Build a pipeline to compress, index, and analyze massive machine-generated logs.',
    theoretical_stack='Information theory, streaming algorithms, distributed data processing, anomaly detection',
    domain='manufacturing',
    task_kind='compression',
    target_name='target_value',
    public_data_note='Uses synthetic process telemetry by default because production datasets are often proprietary.',
    random_seed=1780,
)
