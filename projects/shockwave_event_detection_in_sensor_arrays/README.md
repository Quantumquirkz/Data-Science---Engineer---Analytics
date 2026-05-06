# Shockwave Event Detection in Sensor Arrays

Portfolio research lab for **Shockwave Event Detection in Sensor Arrays**.

## Problem framing

Detect and localize shockwave-like events across distributed sensor arrays using benchmark waveform datasets or synthetic propagation simulations.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

wave propagation intuition, time delay estimation, signal processing, localization, statistical detection.

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
- `src/pipeline.py` - `run_shockwave_event_detection_in_sensor_arrays_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/shockwave_event_detection_in_sensor_arrays.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.shockwave_event_detection_in_sensor_arrays.src.pipeline import run_shockwave_event_detection_in_sensor_arrays_pipeline; a = run_shockwave_event_detection_in_sensor_arrays_pipeline(Path('projects/shockwave_event_detection_in_sensor_arrays')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/shockwave_event_detection_in_sensor_arrays/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/shockwave_event_detection_in_sensor_arrays/notebooks/shockwave_event_detection_in_sensor_arrays.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
