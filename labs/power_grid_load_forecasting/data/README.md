# Data — Power grid load forecasting

## Sources

1. **Open Power System Data (OPSD)** — [Time series package](https://open-power-system-data.org/time_series/), consolidated hourly table (`time_series_60min_singleindex.csv`).  
   - Default column: `DE_load_actual_entsoe_transparency` (Germany load, MW).  
   - The `latest` URL redirects to a **versioned snapshot** (often with data through roughly **2019**). Default pipeline dates target that window; use a newer OPSD release URL via `DatasetConfig.opsd_csv_url` for recent years.  
   - License: [ODbL](https://opendatacommons.org/licenses/odbl/) (check OPSD site for current terms).

2. **Open-Meteo Historical Weather API** — [Archive API](https://open-meteo.com/en/docs/historical-weather-api).  
   - Hourly `temperature_2m`, `relative_humidity_2m`, `wind_speed_10m` for a representative point (default: Berlin).

## Cached artifacts

After the first pipeline run, `data/processed/` typically contains:

- `opsd_load_filtered.parquet` — hourly load for the configured window (UTC index).
- `open_meteo_hourly.parquet` — weather for the same window.
- `load_weather_hourly.parquet` — merged table used downstream.
- `dataset_provenance.csv` — URLs and parameters.

Delete these files to force a fresh download (OPSD CSV is large; first run can take several minutes).
