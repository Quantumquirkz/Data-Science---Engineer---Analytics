from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=41,
    slug='hospital_queue_dynamics_analyzer',
    title='Hospital Queue Dynamics Analyzer',
    description='Model waiting times, resource bottlenecks, and patient flow in emergency departments.',
    theoretical_stack='Queueing theory, stochastic processes, simulation, operations research, statistical analysis',
    domain='manufacturing',
    task_kind='event_detection',
    target_name='target_label',
    public_data_note='Uses synthetic process telemetry by default because production datasets are often proprietary.',
    random_seed=1770,
)
