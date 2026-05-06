# Autonomous Vehicle Sensor Fusion Project

Portfolio research lab for **Autonomous Vehicle Sensor Fusion Project**.

## Problem framing

Fuse camera, LiDAR, GPS, and inertial data for improved localization or perception using autonomous driving benchmark datasets rather than collecting sensor data yourself.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

Bayesian fusion, Kalman filters, geometry, computer vision, probabilistic robotics.

## Data policy

Uses simulated telemetry by default; benchmark logs can be adapted later.

## Project structure

- `src/config.py` - project metadata and domain/task configuration
- `src/data.py` - reproducible data generation/loading wrappers
- `src/preprocessing.py` - timestamp ordering, imputation, and numeric cleanup
- `src/features.py` - temporal, physical, interaction, and rolling features
- `src/modeling.py` - supervised or unsupervised models selected from the project task
- `src/evaluation.py` - metric summaries for reports and demos
- `src/visualization.py` - signal, projection, and validation plots
- `src/pipeline.py` - `run_autonomous_vehicle_sensor_fusion_project_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/autonomous_vehicle_sensor_fusion_project.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.autonomous_vehicle_sensor_fusion_project.src.pipeline import run_autonomous_vehicle_sensor_fusion_project_pipeline; a = run_autonomous_vehicle_sensor_fusion_project_pipeline(Path('projects/autonomous_vehicle_sensor_fusion_project')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/autonomous_vehicle_sensor_fusion_project/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/autonomous_vehicle_sensor_fusion_project/notebooks/autonomous_vehicle_sensor_fusion_project.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
