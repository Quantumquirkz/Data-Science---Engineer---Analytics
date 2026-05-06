# Ocean Current Field Compression

Portfolio research lab for **Ocean Current Field Compression**.

## Problem framing

Compress and reconstruct ocean current fields from massive spatiotemporal datasets.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

PCA, tensor decomposition, dimensionality reduction, numerical approximation, fluid dynamics intuition.

## Data policy

Designed for public scientific repositories, with generated proxy fields for reproducibility.

## Project structure

- `src/config.py` - project metadata and domain/task configuration
- `src/data.py` - reproducible data generation/loading wrappers
- `src/preprocessing.py` - timestamp ordering, imputation, and numeric cleanup
- `src/features.py` - temporal, physical, interaction, and rolling features
- `src/modeling.py` - supervised or unsupervised models selected from the project task
- `src/evaluation.py` - metric summaries for reports and demos
- `src/visualization.py` - signal, projection, and validation plots
- `src/pipeline.py` - `run_ocean_current_field_compression_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/ocean_current_field_compression.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.ocean_current_field_compression.src.pipeline import run_ocean_current_field_compression_pipeline; a = run_ocean_current_field_compression_pipeline(Path('projects/ocean_current_field_compression')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/ocean_current_field_compression/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/ocean_current_field_compression/notebooks/ocean_current_field_compression.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
