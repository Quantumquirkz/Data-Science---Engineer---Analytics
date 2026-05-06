from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=82,
    slug='satellite_orbit_perturbation_analysis',
    title='Satellite Orbit Perturbation Analysis',
    description='Analyze orbit perturbations from drag, gravity irregularities, and control corrections.',
    theoretical_stack='celestial mechanics, numerical methods, estimation, perturbation analysis, simulation',
    domain='astronomy',
    task_kind='optimization',
    target_name='target_value',
    public_data_note='Compatible with open astronomy archives; default table emulates noisy detector/catalog measurements.',
    random_seed=1811,
)
