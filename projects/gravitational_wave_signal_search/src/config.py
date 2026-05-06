from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=67,
    slug='gravitational_wave_signal_search',
    title='Gravitational Wave Signal Search',
    description='Search for faint gravitational wave-like patterns in noisy time series.',
    theoretical_stack='matched filtering, signal detection theory, spectral methods, rare-event detection, statistical inference',
    domain='astronomy',
    task_kind='rare_event',
    target_name='target_label',
    public_data_note='Compatible with open astronomy archives; default table emulates noisy detector/catalog measurements.',
    random_seed=1796,
)
