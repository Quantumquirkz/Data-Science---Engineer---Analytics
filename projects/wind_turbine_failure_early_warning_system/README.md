# Wind Turbine Failure Early Warning System

Portfolio research lab for **Wind Turbine Failure Early Warning System**.

## Problem framing

Predict turbine faults using public vibration, temperature, and rotational telemetry datasets from wind turbines or rotating machinery benchmarks.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

Signal processing, spectral analysis, reliability theory, anomaly detection, supervised learning.

## Data policy

Uses synthetic process telemetry by default because production datasets are often proprietary.

## Project structure

- `src/config.py` - project metadata and domain/task configuration
- `src/data.py` - reproducible data generation/loading wrappers
- `src/preprocessing.py` - timestamp ordering, imputation, and numeric cleanup
- `src/features.py` - temporal, physical, interaction, and rolling features
- `src/modeling.py` - supervised or unsupervised models selected from the project task
- `src/evaluation.py` - metric summaries for reports and demos
- `src/visualization.py` - signal, projection, and validation plots
- `src/pipeline.py` - `run_wind_turbine_failure_early_warning_system_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/wind_turbine_failure_early_warning_system.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.wind_turbine_failure_early_warning_system.src.pipeline import run_wind_turbine_failure_early_warning_system_pipeline; a = run_wind_turbine_failure_early_warning_system_pipeline(Path('projects/wind_turbine_failure_early_warning_system')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/wind_turbine_failure_early_warning_system/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/wind_turbine_failure_early_warning_system/notebooks/wind_turbine_failure_early_warning_system.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
