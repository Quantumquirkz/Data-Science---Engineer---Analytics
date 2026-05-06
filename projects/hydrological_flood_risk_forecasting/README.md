# Hydrological Flood Risk Forecasting

Portfolio research lab for **Hydrological Flood Risk Forecasting**.

## Problem framing

Forecast flood risk using rainfall, river level, and terrain information.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

Time series, hydrology basics, spatial analysis, regression, extreme value statistics.

## Data policy

Public meteorological or geospatial data can be swapped in; default demo uses synthetic spatial fields.

## Project structure

- `src/config.py` - project metadata and domain/task configuration
- `src/data.py` - reproducible data generation/loading wrappers
- `src/preprocessing.py` - timestamp ordering, imputation, and numeric cleanup
- `src/features.py` - temporal, physical, interaction, and rolling features
- `src/modeling.py` - supervised or unsupervised models selected from the project task
- `src/evaluation.py` - metric summaries for reports and demos
- `src/visualization.py` - signal, projection, and validation plots
- `src/pipeline.py` - `run_hydrological_flood_risk_forecasting_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/hydrological_flood_risk_forecasting.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.hydrological_flood_risk_forecasting.src.pipeline import run_hydrological_flood_risk_forecasting_pipeline; a = run_hydrological_flood_risk_forecasting_pipeline(Path('projects/hydrological_flood_risk_forecasting')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/hydrological_flood_risk_forecasting/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/hydrological_flood_risk_forecasting/notebooks/hydrological_flood_risk_forecasting.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
