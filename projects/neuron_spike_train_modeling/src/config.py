from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=66,
    slug='neuron_spike_train_modeling',
    title='Neuron Spike Train Modeling',
    description='Model neural spike trains and infer activity patterns from electrophysiology data.',
    theoretical_stack='point processes, stochastic modeling, time series, information theory, statistical neuroscience',
    domain='biomedical',
    task_kind='regression',
    target_name='target_value',
    public_data_note='Uses privacy-safe synthetic proxies by default; public biomedical datasets can replace the source table.',
    random_seed=1795,
)
