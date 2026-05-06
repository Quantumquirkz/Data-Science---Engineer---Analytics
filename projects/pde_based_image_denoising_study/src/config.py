from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=34,
    slug='pde_based_image_denoising_study',
    title='PDE-Based Image Denoising Study',
    description='Apply differential-equation-based denoising and compare against learned filters.',
    theoretical_stack='PDEs, variational methods, numerical solvers, image processing, benchmarking',
    domain='manufacturing',
    task_kind='regression',
    target_name='target_value',
    public_data_note='Uses synthetic process telemetry by default because production datasets are often proprietary.',
    random_seed=1763,
)
