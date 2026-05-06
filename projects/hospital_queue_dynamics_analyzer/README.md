# Hospital Queue Dynamics Analyzer

Portfolio research lab for **Hospital Queue Dynamics Analyzer**.

## Problem framing

Model waiting times, resource bottlenecks, and patient flow in emergency departments.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

Queueing theory, stochastic processes, simulation, operations research, statistical analysis.

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
- `src/pipeline.py` - `run_hospital_queue_dynamics_analyzer_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/hospital_queue_dynamics_analyzer.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.hospital_queue_dynamics_analyzer.src.pipeline import run_hospital_queue_dynamics_analyzer_pipeline; a = run_hospital_queue_dynamics_analyzer_pipeline(Path('projects/hospital_queue_dynamics_analyzer')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/hospital_queue_dynamics_analyzer/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/hospital_queue_dynamics_analyzer/notebooks/hospital_queue_dynamics_analyzer.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
