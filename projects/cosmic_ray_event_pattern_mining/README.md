# Cosmic Ray Event Pattern Mining

Portfolio research lab for **Cosmic Ray Event Pattern Mining**.

## Problem framing

Mine rare-event patterns from large astrophysics detector logs.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

Poisson processes, rare event statistics, outlier detection, pattern mining, experimental physics data analysis.

## Data policy

Compatible with open astronomy archives; default table emulates noisy detector/catalog measurements.

## Project structure

- `src/config.py` - project metadata and domain/task configuration
- `src/data.py` - reproducible data generation/loading wrappers
- `src/preprocessing.py` - timestamp ordering, imputation, and numeric cleanup
- `src/features.py` - temporal, physical, interaction, and rolling features
- `src/modeling.py` - supervised or unsupervised models selected from the project task
- `src/evaluation.py` - metric summaries for reports and demos
- `src/visualization.py` - signal, projection, and validation plots
- `src/pipeline.py` - `run_cosmic_ray_event_pattern_mining_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/cosmic_ray_event_pattern_mining.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.cosmic_ray_event_pattern_mining.src.pipeline import run_cosmic_ray_event_pattern_mining_pipeline; a = run_cosmic_ray_event_pattern_mining_pipeline(Path('projects/cosmic_ray_event_pattern_mining')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/cosmic_ray_event_pattern_mining/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/cosmic_ray_event_pattern_mining/notebooks/cosmic_ray_event_pattern_mining.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
