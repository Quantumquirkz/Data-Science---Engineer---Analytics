# Smart Farming Irrigation Optimizer

Portfolio research lab for **Smart Farming Irrigation Optimizer**.

## Problem framing

Optimize irrigation schedules using open weather, soil moisture, and crop condition datasets or agricultural simulations.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

control theory, optimization, environmental modeling, forecasting, decision systems.

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
- `src/pipeline.py` - `run_smart_farming_irrigation_optimizer_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/smart_farming_irrigation_optimizer.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.smart_farming_irrigation_optimizer.src.pipeline import run_smart_farming_irrigation_optimizer_pipeline; a = run_smart_farming_irrigation_optimizer_pipeline(Path('projects/smart_farming_irrigation_optimizer')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/smart_farming_irrigation_optimizer/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/smart_farming_irrigation_optimizer/notebooks/smart_farming_irrigation_optimizer.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
