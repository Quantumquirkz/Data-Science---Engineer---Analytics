# Data

This project defaults to a reproducible generated dataset saved under `data/processed/`.

Policy: Compatible with open astronomy archives; default table emulates noisy detector/catalog measurements.

Expected replacement schema for public data:

- `timestamp`
- `x_coord`, `y_coord`
- `sensor_a`, `sensor_b`, `sensor_c`
- `external_forcing`
- `physics_signal`
- `target_label`

Keep raw public downloads outside git unless they are small and redistributable.
