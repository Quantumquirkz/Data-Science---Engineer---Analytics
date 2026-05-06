from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=74,
    slug='industrial_sound_event_detector',
    title='Industrial Sound Event Detector',
    description='Detect mechanical faults from public industrial sound recordings and machine-condition monitoring datasets.',
    theoretical_stack='signal processing, spectrogram analysis, classification, anomaly detection, acoustic physics',
    domain='manufacturing',
    task_kind='anomaly',
    target_name='target_label',
    public_data_note='Uses synthetic process telemetry by default because production datasets are often proprietary.',
    random_seed=1803,
)
