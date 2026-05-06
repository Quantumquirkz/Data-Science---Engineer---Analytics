# Data

This project defaults to a reproducible generated dataset saved under `data/processed/`.

Policy: Mix public energy benchmarks with reproducible synthetic telemetry for offline runs.

Expected replacement schema for public data:

- `timestamp`
- `x_coord`, `y_coord`
- `sensor_a`, `sensor_b`, `sensor_c`
- `external_forcing`
- `physics_signal`
- `target_value`

Keep raw public downloads outside git unless they are small and redistributable.
