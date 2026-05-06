# Smart Grid Fault Localization

Portfolio research lab for **Smart Grid Fault Localization**.

## Problem framing

Localize likely faults in a smart grid using public power system benchmarks, simulated grids, and sparse telemetry logs.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

graph inference, state estimation, optimization, signal analysis, electrical systems intuition.

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
- `src/pipeline.py` - `run_smart_grid_fault_localization_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/smart_grid_fault_localization.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.smart_grid_fault_localization.src.pipeline import run_smart_grid_fault_localization_pipeline; a = run_smart_grid_fault_localization_pipeline(Path('projects/smart_grid_fault_localization')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/smart_grid_fault_localization/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/smart_grid_fault_localization/notebooks/smart_grid_fault_localization.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
