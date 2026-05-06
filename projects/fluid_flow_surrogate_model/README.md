# Fluid Flow Surrogate Model

Portfolio research lab for **Fluid Flow Surrogate Model**.

## Problem framing

Train a machine learning model to approximate outputs of expensive fluid dynamics simulations.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

Numerical methods, surrogate modeling, interpolation, regression, dimensionality reduction, computational fluid dynamics intuition.

## Data policy

Simulation-first project with reproducible stochastic scenarios.

## Project structure

- `src/config.py` - project metadata and domain/task configuration
- `src/data.py` - reproducible data generation/loading wrappers
- `src/preprocessing.py` - timestamp ordering, imputation, and numeric cleanup
- `src/features.py` - temporal, physical, interaction, and rolling features
- `src/modeling.py` - supervised or unsupervised models selected from the project task
- `src/evaluation.py` - metric summaries for reports and demos
- `src/visualization.py` - signal, projection, and validation plots
- `src/pipeline.py` - `run_fluid_flow_surrogate_model_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/fluid_flow_surrogate_model.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.fluid_flow_surrogate_model.src.pipeline import run_fluid_flow_surrogate_model_pipeline; a = run_fluid_flow_surrogate_model_pipeline(Path('projects/fluid_flow_surrogate_model')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/fluid_flow_surrogate_model/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/fluid_flow_surrogate_model/notebooks/fluid_flow_surrogate_model.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
