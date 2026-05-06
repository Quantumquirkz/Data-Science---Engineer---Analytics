# Epidemiological Spread Simulation

Portfolio research lab for **Epidemiological Spread Simulation**.

## Problem framing

Model and analyze disease spread using compartmental and network approaches.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

Differential equations, graph theory, stochastic simulation, parameter estimation, causal reasoning.

## Data policy

Uses privacy-safe synthetic proxies by default; public biomedical datasets can replace the source table.

## Project structure

- `src/config.py` - project metadata and domain/task configuration
- `src/data.py` - reproducible data generation/loading wrappers
- `src/preprocessing.py` - timestamp ordering, imputation, and numeric cleanup
- `src/features.py` - temporal, physical, interaction, and rolling features
- `src/modeling.py` - supervised or unsupervised models selected from the project task
- `src/evaluation.py` - metric summaries for reports and demos
- `src/visualization.py` - signal, projection, and validation plots
- `src/pipeline.py` - `run_epidemiological_spread_simulation_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/epidemiological_spread_simulation.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.epidemiological_spread_simulation.src.pipeline import run_epidemiological_spread_simulation_pipeline; a = run_epidemiological_spread_simulation_pipeline(Path('projects/epidemiological_spread_simulation')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/epidemiological_spread_simulation/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/epidemiological_spread_simulation/notebooks/epidemiological_spread_simulation.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
