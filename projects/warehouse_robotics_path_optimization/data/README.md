# Data

This project defaults to a reproducible generated dataset saved under `data/processed/`.

Policy: Uses generated graph/flow proxies by default; public logs or network datasets can be mapped into the same schema.

Expected replacement schema for public data:

- `timestamp`
- `x_coord`, `y_coord`
- `sensor_a`, `sensor_b`, `sensor_c`
- `external_forcing`
- `physics_signal`
- `target_value`

Keep raw public downloads outside git unless they are small and redistributable.
