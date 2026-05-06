# Particle Collision Feature Extraction Pipeline

Portfolio research lab for **Particle Collision Feature Extraction Pipeline**.

## Problem framing

Build a scalable pipeline to preprocess and analyze high-energy collision event features.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

feature engineering, distributed analytics, dimensionality reduction, classification, particle physics intuition.

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
- `src/pipeline.py` - `run_particle_collision_feature_extraction_pipeline_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/particle_collision_feature_extraction_pipeline.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.particle_collision_feature_extraction_pipeline.src.pipeline import run_particle_collision_feature_extraction_pipeline_pipeline; a = run_particle_collision_feature_extraction_pipeline_pipeline(Path('projects/particle_collision_feature_extraction_pipeline')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/particle_collision_feature_extraction_pipeline/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/particle_collision_feature_extraction_pipeline/notebooks/particle_collision_feature_extraction_pipeline.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
