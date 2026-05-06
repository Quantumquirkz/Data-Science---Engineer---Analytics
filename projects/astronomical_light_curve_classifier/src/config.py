from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=38,
    slug='astronomical_light_curve_classifier',
    title='Astronomical Light Curve Classifier',
    description='Classify stars, exoplanet transits, or variable objects from light curve data.',
    theoretical_stack='Time series, frequency-domain methods, supervised learning, probabilistic classification, astrophysics basics',
    domain='general',
    task_kind='classification',
    target_name='target_label',
    public_data_note='Uses a reproducible synthetic dataset by default, with public-data replacement points documented.',
    random_seed=1767,
)
