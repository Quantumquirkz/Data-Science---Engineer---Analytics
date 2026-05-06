# Thermal Camera Defect Detection

Portfolio research lab for **Thermal Camera Defect Detection**.

## Problem framing

Detect hidden structural or electrical defects from public thermal image datasets and benchmark inspection sequences.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

Heat transfer intuition, image processing, anomaly detection, spatiotemporal modeling.

## Data policy

Uses synthetic process telemetry by default because production datasets are often proprietary.

## Project structure

- `src/config.py` - project metadata and domain/task configuration
- `src/data.py` - reproducible data generation/loading wrappers
- `src/preprocessing.py` - timestamp ordering, imputation, and numeric cleanup
- `src/features.py` - temporal, physical, interaction, and rolling features
- `src/modeling.py` - supervised or unsupervised models selected from the project task
- `src/evaluation.py` - metric summaries for reports and demos
- `src/visualization.py` - signal, projection, and validation plots
- `src/pipeline.py` - `run_thermal_camera_defect_detection_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/thermal_camera_defect_detection.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.thermal_camera_defect_detection.src.pipeline import run_thermal_camera_defect_detection_pipeline; a = run_thermal_camera_defect_detection_pipeline(Path('projects/thermal_camera_defect_detection')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/thermal_camera_defect_detection/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/thermal_camera_defect_detection/notebooks/thermal_camera_defect_detection.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
