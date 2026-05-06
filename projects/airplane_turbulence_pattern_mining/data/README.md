# Data

This project defaults to a reproducible generated dataset saved under `data/processed/`.

Policy: Public meteorological or geospatial data can be swapped in; default demo uses synthetic spatial fields.

Expected replacement schema for public data:

- `timestamp`
- `x_coord`, `y_coord`
- `sensor_a`, `sensor_b`, `sensor_c`
- `external_forcing`
- `physics_signal`
- `target_label`

Keep raw public downloads outside git unless they are small and redistributable.
