# Power grid load forecasting

Portfolio lab for **regional hourly load** (default: Germany `DE_load_actual_entsoe_transparency` from [Open Power System Data](https://open-power-system-data.org/time_series/)) combined with **Open-Meteo** weather, **calendar / holiday** features (via `holidays`), and simple **HDD/CDD** proxies.

Models include **naive and calendar baselines**, **Ridge**, **HistGradientBoosting**, **LightGBM quantile** (10% / 50% / 90%), an **ensemble** with nonnegative weights fit by minimizing validation MSE (`scipy.optimize.minimize`), and a **SARIMAX** benchmark: fixed-origin multi-step forecast of **realized** load over the validation window (exogenous temperature + calendar harmonics), trained on at most the last **8760** train hours for speed.

**Direct horizons:** 24 h and 168 h (`target_load_*` with strict temporal split). **Seasonal decomposition** (additive, 24 h period) is saved for EDA under `data/processed/reports/`.

## Data caveats

The OPSD URL `.../time_series/latest/...csv` redirects to a **versioned snapshot** (often covering roughly **2015–2019**). Defaults use **2017–2018** so the first run succeeds without retuning. For newer years, point `DatasetConfig.opsd_csv_url` at a newer OPSD release.

## Project structure

- `src/data.py` — OPSD chunked CSV + Open-Meteo, merge, temporal split
- `src/preprocessing.py` — hourly grid, light fill
- `src/features.py` — lags, rolling means, holidays, HDD/CDD, targets
- `src/modeling.py` — baselines, sklearn/LightGBM, SARIMAX, ensemble weights
- `src/evaluation.py` — RMSE, MAE, sMAPE, pinball, interval coverage
- `src/visualization.py` — forecast ribbon, residuals, metric heatmap, decomposition plot
- `src/pipeline.py` — `run_power_grid_load_pipeline`
- `src/inference.py` — load bundle / validation predictions
- `app.py` — Gradio demo
- `notebooks/power_grid_load_forecasting.ipynb` — walkthrough

## How to run

From the repository root (set `PYTHONPATH` to the repo root):

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.power_grid_load_forecasting.src.pipeline import run_power_grid_load_pipeline; a = run_power_grid_load_pipeline(Path('projects/power_grid_load_forecasting')); print(a.model_artifacts.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/power_grid_load_forecasting/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/power_grid_load_forecasting/notebooks/power_grid_load_forecasting.ipynb`.

## Suggested extensions

- Walk-forward SARIMAX or state-space models with Kalman updates
- Quantile stacking and CRPS
- Additional calendar events (school breaks) and lagged temperature
- Newer OPSD CSV or ENTSO-E transparency for up-to-date training windows
