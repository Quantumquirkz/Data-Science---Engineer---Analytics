# Structural Health Monitoring Platform

Portfolio research lab for **Structural Health Monitoring Platform**.

## Problem framing

Monitor bridges or buildings using public structural health monitoring datasets with strain, vibration, and displacement measurements.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

mechanics, time series, signal processing, anomaly detection, reliability theory.

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
- `src/pipeline.py` - `run_structural_health_monitoring_platform_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/structural_health_monitoring_platform.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.structural_health_monitoring_platform.src.pipeline import run_structural_health_monitoring_platform_pipeline; a = run_structural_health_monitoring_platform_pipeline(Path('projects/structural_health_monitoring_platform')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/structural_health_monitoring_platform/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/structural_health_monitoring_platform/notebooks/structural_health_monitoring_platform.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
