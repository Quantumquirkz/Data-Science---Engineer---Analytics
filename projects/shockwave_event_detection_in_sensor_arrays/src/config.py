from __future__ import annotations

from projects._portfolio_common import ProjectSpec


SPEC = ProjectSpec(
    number=93,
    slug='shockwave_event_detection_in_sensor_arrays',
    title='Shockwave Event Detection in Sensor Arrays',
    description='Detect and localize shockwave-like events across distributed sensor arrays using benchmark waveform datasets or synthetic propagation simulations.',
    theoretical_stack='wave propagation intuition, time delay estimation, signal processing, localization, statistical detection',
    domain='manufacturing',
    task_kind='event_detection',
    target_name='target_label',
    public_data_note='Uses synthetic process telemetry by default because production datasets are often proprietary.',
    random_seed=1822,
)
