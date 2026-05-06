from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=24,
    slug='quantum_experiment_result_dashboard',
    title='Quantum Experiment Result Dashboard',
    description='Create an analytics interface for visualizing outcomes of quantum or optics experiments using openly shared research datasets.',
    theoretical_stack='Probability amplitudes intuition, statistical visualization, experimental design, uncertainty reporting, dashboarding',
    domain='general',
    task_kind='event_detection',
    target_name='target_label',
    public_data_note='Uses a reproducible synthetic dataset by default, with public-data replacement points documented.',
    random_seed=1753,
)
