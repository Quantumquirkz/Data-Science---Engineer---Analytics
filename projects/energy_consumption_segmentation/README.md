# Energy Consumption Segmentation

Portfolio research lab for **Energy Consumption Segmentation**.

## Problem framing

Cluster households or facilities based on their energy-use signatures.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

Clustering, distance metrics, dimensionality reduction, time series features, unsupervised learning.

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
- `src/pipeline.py` - `run_energy_consumption_segmentation_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/energy_consumption_segmentation.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.energy_consumption_segmentation.src.pipeline import run_energy_consumption_segmentation_pipeline; a = run_energy_consumption_segmentation_pipeline(Path('projects/energy_consumption_segmentation')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/energy_consumption_segmentation/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/energy_consumption_segmentation/notebooks/energy_consumption_segmentation.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
