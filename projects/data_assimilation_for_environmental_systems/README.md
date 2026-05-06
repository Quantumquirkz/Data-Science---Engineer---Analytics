# Data Assimilation for Environmental Systems

Portfolio research lab for **Data Assimilation for Environmental Systems**.

## Problem framing

Fuse simulation outputs and observed data to improve state estimation.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

Kalman filtering, Bayesian inference, differential equations, uncertainty propagation, state-space models.

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
- `src/pipeline.py` - `run_data_assimilation_for_environmental_systems_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/data_assimilation_for_environmental_systems.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.data_assimilation_for_environmental_systems.src.pipeline import run_data_assimilation_for_environmental_systems_pipeline; a = run_data_assimilation_for_environmental_systems_pipeline(Path('projects/data_assimilation_for_environmental_systems')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/data_assimilation_for_environmental_systems/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/data_assimilation_for_environmental_systems/notebooks/data_assimilation_for_environmental_systems.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
