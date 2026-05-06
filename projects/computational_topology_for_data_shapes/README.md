# Computational Topology for Data Shapes

Portfolio research lab for **Computational Topology for Data Shapes**.

## Problem framing

Study the shape of high-dimensional datasets using topological summaries.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

topology, geometry, persistent homology intuition, manifold learning, unsupervised analysis.

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
- `src/pipeline.py` - `run_computational_topology_for_data_shapes_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/computational_topology_for_data_shapes.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.computational_topology_for_data_shapes.src.pipeline import run_computational_topology_for_data_shapes_pipeline; a = run_computational_topology_for_data_shapes_pipeline(Path('projects/computational_topology_for_data_shapes')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/computational_topology_for_data_shapes/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/computational_topology_for_data_shapes/notebooks/computational_topology_for_data_shapes.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
