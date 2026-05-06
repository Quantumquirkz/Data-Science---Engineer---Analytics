from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=55,
    slug='airplane_turbulence_pattern_mining',
    title='Airplane Turbulence Pattern Mining',
    description='Identify turbulence signatures from public flight telemetry archives and environmental conditions.',
    theoretical_stack='Fluid dynamics intuition, signal analysis, anomaly detection, supervised learning',
    domain='environment',
    task_kind='anomaly',
    target_name='target_label',
    public_data_note='Public meteorological or geospatial data can be swapped in; default demo uses synthetic spatial fields.',
    random_seed=1784,
)
