# Solar Irradiance Forecasting

Portfolio lab for **short-term GHI forecasting** (1 h, 3 h, 6 h) using Open-Meteo archive data (weather + shortwave radiation), lagged irradiance, cloud features, and basic solar geometry (elevation, extraterrestrial horizontal irradiance, clearness index).

Uncertainty is handled with **LightGBM quantile regression** (10%, 50%, 90%) and reported **pinball loss** plus empirical **80% interval coverage** on a strict temporal validation window (last N months).

## Project structure

- `src/data.py` — Open-Meteo fetch, Parquet cache, temporal split
- `src/preprocessing.py` — hourly grid, light forward/back fill
- `src/features.py` — lags, rolling means, solar position, clearness, targets
- `src/modeling.py` — persistence, hourly-median, Ridge, HGBR, LightGBM quantiles
- `src/evaluation.py` — RMSE, MAE, sMAPE, pinball, interval coverage
- `src/visualization.py` — forecast ribbon, residuals by hour, RMSE heatmap
- `src/pipeline.py` — `run_solar_irradiance_pipeline`
- `src/inference.py` — load bundle / validation predictions
- `app.py` — Gradio demo
- `notebooks/solar_irradiance_forecasting.ipynb` — guided walkthrough

## How to run

From the repository root:

```bash
uv run python -c "from pathlib import Path; from projects.solar_irradiance_forecasting.src.pipeline import run_solar_irradiance_pipeline; a = run_solar_irradiance_pipeline(Path('projects/solar_irradiance_forecasting')); print(a.model_artifacts.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
uv run python projects/solar_irradiance_forecasting/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/solar_irradiance_forecasting/notebooks/solar_irradiance_forecasting.ipynb`.

## Data

The first run downloads hourly data into `data/processed/open_meteo_hourly.parquet`. See `data/README.md`.

## Suggested extensions

- Sub-hourly horizons with minutely archives or satellite cloud motion vectors
- Probabilistic scores (CRPS) and calibration plots
- `statsmodels` state-space or SARIMAX with exogenous NWP fields
- Multi-site training and grouped backtesting
