# Traffic Flow as a Physical System

Portfolio research lab for **Traffic Flow as a Physical System**.

## Problem framing

Study urban traffic as a dynamical system and predict congestion patterns.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

Dynamical systems, PDE intuition, graph theory, optimization, time series modeling, simulation.

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
- `src/pipeline.py` - `run_traffic_flow_as_a_physical_system_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/traffic_flow_as_a_physical_system.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.traffic_flow_as_a_physical_system.src.pipeline import run_traffic_flow_as_a_physical_system_pipeline; a = run_traffic_flow_as_a_physical_system_pipeline(Path('projects/traffic_flow_as_a_physical_system')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/traffic_flow_as_a_physical_system/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/traffic_flow_as_a_physical_system/notebooks/traffic_flow_as_a_physical_system.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
