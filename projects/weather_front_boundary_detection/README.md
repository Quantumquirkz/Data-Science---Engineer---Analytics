# Weather Front Boundary Detection

Portfolio research lab for **Weather Front Boundary Detection**.

## Problem framing

Detect moving weather fronts from gridded atmospheric data.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

Gradient fields, numerical differentiation, image segmentation, spatial statistics, meteorological modeling.

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
- `src/pipeline.py` - `run_weather_front_boundary_detection_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/weather_front_boundary_detection.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.weather_front_boundary_detection.src.pipeline import run_weather_front_boundary_detection_pipeline; a = run_weather_front_boundary_detection_pipeline(Path('projects/weather_front_boundary_detection')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/weather_front_boundary_detection/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/weather_front_boundary_detection/notebooks/weather_front_boundary_detection.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
