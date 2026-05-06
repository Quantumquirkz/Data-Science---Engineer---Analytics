# Environmental Sensor Network Placement Optimizer

Portfolio research lab for **Environmental Sensor Network Placement Optimizer**.

## Problem framing

Optimize where sensors should be placed to maximize information coverage using simulated environments or public geospatial layers rather than deploying hardware.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

information theory, combinatorial optimization, spatial statistics, experimental design.

## Data policy

Public meteorological or geospatial data can be swapped in; default demo uses synthetic spatial fields.

## Project structure

- `src/config.py` - project metadata and domain/task configuration
- `src/data.py` - reproducible data generation/loading wrappers
- `src/preprocessing.py` - timestamp ordering, imputation, and numeric cleanup
- `src/features.py` - temporal, physical, interaction, and rolling features
- `src/modeling.py` - supervised or unsupervised models selected from the project task
- `src/evaluation.py` - metric summaries for reports and demos
- `src/visualization.py` - signal, projection, and validation plots
- `src/pipeline.py` - `run_environmental_sensor_network_placement_optimizer_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/environmental_sensor_network_placement_optimizer.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.environmental_sensor_network_placement_optimizer.src.pipeline import run_environmental_sensor_network_placement_optimizer_pipeline; a = run_environmental_sensor_network_placement_optimizer_pipeline(Path('projects/environmental_sensor_network_placement_optimizer')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/environmental_sensor_network_placement_optimizer/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/environmental_sensor_network_placement_optimizer/notebooks/environmental_sensor_network_placement_optimizer.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
