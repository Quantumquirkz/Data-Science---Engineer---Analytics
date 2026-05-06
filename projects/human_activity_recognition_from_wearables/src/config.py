from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=80,
    slug='human_activity_recognition_from_wearables',
    title='Human Activity Recognition from Wearables',
    description='Recognize physical activities from public accelerometer and gyroscope datasets collected from wearables or smartphones.',
    theoretical_stack='time series classification, signal processing, feature extraction, deep learning basics',
    domain='manufacturing',
    task_kind='classification',
    target_name='target_label',
    public_data_note='Uses synthetic process telemetry by default because production datasets are often proprietary.',
    random_seed=1809,
)
