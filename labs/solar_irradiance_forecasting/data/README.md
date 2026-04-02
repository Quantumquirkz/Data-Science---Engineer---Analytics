# Data notes

This lab downloads and caches hourly weather and irradiance from the **Open-Meteo Archive API** (no API key) under `data/processed/`:

- `open_meteo_hourly.parquet` — cached raw hourly table
- `features_dataset.parquet` — engineered features with train/validation split labels
- `reports/` — metrics, prediction tables, run summary JSON
- `models/` — pickled model bundle (LightGBM quantile models + metadata)

The first pipeline run performs the HTTP fetch; later runs reuse the Parquet cache. Delete the cache file to force a refresh.

For US-specific or higher-accuracy studies, consider [NSRDB](https://nsrdb.nrel.gov/) or [NASA POWER](https://power.larc.nasa.gov/) and adapt `src/data.py`.
