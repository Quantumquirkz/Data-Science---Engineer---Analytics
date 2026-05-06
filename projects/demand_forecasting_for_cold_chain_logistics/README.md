# Demand Forecasting for Cold Chain Logistics

Portfolio research lab for **Demand Forecasting for Cold Chain Logistics**.

## Problem framing

Forecast demand and spoilage risk in temperature-sensitive supply chains.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

time series, optimization, survival analysis, operations research, uncertainty modeling.

## Data policy

Uses generated graph/flow proxies by default; public logs or network datasets can be mapped into the same schema.

## Project structure

- `src/config.py` - project metadata and domain/task configuration
- `src/data.py` - reproducible data generation/loading wrappers
- `src/preprocessing.py` - timestamp ordering, imputation, and numeric cleanup
- `src/features.py` - temporal, physical, interaction, and rolling features
- `src/modeling.py` - supervised or unsupervised models selected from the project task
- `src/evaluation.py` - metric summaries for reports and demos
- `src/visualization.py` - signal, projection, and validation plots
- `src/pipeline.py` - `run_demand_forecasting_for_cold_chain_logistics_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/demand_forecasting_for_cold_chain_logistics.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.demand_forecasting_for_cold_chain_logistics.src.pipeline import run_demand_forecasting_for_cold_chain_logistics_pipeline; a = run_demand_forecasting_for_cold_chain_logistics_pipeline(Path('projects/demand_forecasting_for_cold_chain_logistics')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/demand_forecasting_for_cold_chain_logistics/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/demand_forecasting_for_cold_chain_logistics/notebooks/demand_forecasting_for_cold_chain_logistics.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
