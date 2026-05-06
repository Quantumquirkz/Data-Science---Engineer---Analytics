# Satellite Orbit Perturbation Analysis

Portfolio research lab for **Satellite Orbit Perturbation Analysis**.

## Problem framing

Analyze orbit perturbations from drag, gravity irregularities, and control corrections.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

celestial mechanics, numerical methods, estimation, perturbation analysis, simulation.

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
- `src/pipeline.py` - `run_satellite_orbit_perturbation_analysis_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/satellite_orbit_perturbation_analysis.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.satellite_orbit_perturbation_analysis.src.pipeline import run_satellite_orbit_perturbation_analysis_pipeline; a = run_satellite_orbit_perturbation_analysis_pipeline(Path('projects/satellite_orbit_perturbation_analysis')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/satellite_orbit_perturbation_analysis/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/satellite_orbit_perturbation_analysis/notebooks/satellite_orbit_perturbation_analysis.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
