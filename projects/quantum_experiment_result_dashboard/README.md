# Quantum Experiment Result Dashboard

Portfolio research lab for **Quantum Experiment Result Dashboard**.

## Problem framing

Create an analytics interface for visualizing outcomes of quantum or optics experiments using openly shared research datasets.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

Probability amplitudes intuition, statistical visualization, experimental design, uncertainty reporting, dashboarding.

## Data policy

Uses a reproducible synthetic dataset by default, with public-data replacement points documented.

## Project structure

- `src/config.py` - project metadata and domain/task configuration
- `src/data.py` - reproducible data generation/loading wrappers
- `src/preprocessing.py` - timestamp ordering, imputation, and numeric cleanup
- `src/features.py` - temporal, physical, interaction, and rolling features
- `src/modeling.py` - supervised or unsupervised models selected from the project task
- `src/evaluation.py` - metric summaries for reports and demos
- `src/visualization.py` - signal, projection, and validation plots
- `src/pipeline.py` - `run_quantum_experiment_result_dashboard_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/quantum_experiment_result_dashboard.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.quantum_experiment_result_dashboard.src.pipeline import run_quantum_experiment_result_dashboard_pipeline; a = run_quantum_experiment_result_dashboard_pipeline(Path('projects/quantum_experiment_result_dashboard')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/quantum_experiment_result_dashboard/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/quantum_experiment_result_dashboard/notebooks/quantum_experiment_result_dashboard.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
