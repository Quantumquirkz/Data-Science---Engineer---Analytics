# Wildfire Spread Prediction

Portfolio research lab for **Wildfire Spread Prediction**.

## Problem framing

Predict the likely spread of wildfires using weather, terrain, and vegetation data.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

dynamical systems, PDE intuition, spatial modeling, probabilistic forecasting, environmental science.

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
- `src/pipeline.py` - `run_wildfire_spread_prediction_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/wildfire_spread_prediction.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.wildfire_spread_prediction.src.pipeline import run_wildfire_spread_prediction_pipeline; a = run_wildfire_spread_prediction_pipeline(Path('projects/wildfire_spread_prediction')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/wildfire_spread_prediction/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/wildfire_spread_prediction/notebooks/wildfire_spread_prediction.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
