from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=27,
    slug='gravitational_orbit_simulator',
    title='Gravitational Orbit Simulator',
    description='Simulate orbital trajectories and compare numerical methods for stability and error.',
    theoretical_stack='Classical mechanics, numerical integration, error analysis, dynamical systems, simulation',
    domain='simulation',
    task_kind='simulation',
    target_name='target_value',
    public_data_note='Simulation-first project with reproducible stochastic scenarios.',
    random_seed=1756,
)
