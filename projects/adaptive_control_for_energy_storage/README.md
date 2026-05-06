# Adaptive Control for Energy Storage

Portfolio research lab for **Adaptive Control for Energy Storage**.

## Problem framing

Develop a data-driven controller for charging and discharging battery storage systems using public battery benchmarks and simulated storage environments.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

control theory, optimization, reinforcement learning, time series, dynamical systems.

## Data policy

Mix public energy benchmarks with reproducible synthetic telemetry for offline runs.

## Project structure

- `src/config.py` - project metadata and domain/task configuration
- `src/data.py` - reproducible data generation/loading wrappers
- `src/preprocessing.py` - timestamp ordering, imputation, and numeric cleanup
- `src/features.py` - temporal, physical, interaction, and rolling features
- `src/modeling.py` - supervised or unsupervised models selected from the project task
- `src/evaluation.py` - metric summaries for reports and demos
- `src/visualization.py` - signal, projection, and validation plots
- `src/pipeline.py` - `run_adaptive_control_for_energy_storage_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/adaptive_control_for_energy_storage.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.adaptive_control_for_energy_storage.src.pipeline import run_adaptive_control_for_energy_storage_pipeline; a = run_adaptive_control_for_energy_storage_pipeline(Path('projects/adaptive_control_for_energy_storage')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/adaptive_control_for_energy_storage/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/adaptive_control_for_energy_storage/notebooks/adaptive_control_for_energy_storage.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
