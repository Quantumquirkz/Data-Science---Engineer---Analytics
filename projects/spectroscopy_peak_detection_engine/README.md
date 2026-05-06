# Spectroscopy Peak Detection Engine

Portfolio research lab for **Spectroscopy Peak Detection Engine**.

## Problem framing

Detect and quantify peaks in spectroscopy signals for material or chemical analysis.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

Signal smoothing, peak estimation, numerical optimization, noise modeling, spectral analysis.

## Data policy

Uses synthetic spectral/time-series measurements with documented public-data extension points.

## Project structure

- `src/config.py` - project metadata and domain/task configuration
- `src/data.py` - reproducible data generation/loading wrappers
- `src/preprocessing.py` - timestamp ordering, imputation, and numeric cleanup
- `src/features.py` - temporal, physical, interaction, and rolling features
- `src/modeling.py` - supervised or unsupervised models selected from the project task
- `src/evaluation.py` - metric summaries for reports and demos
- `src/visualization.py` - signal, projection, and validation plots
- `src/pipeline.py` - `run_spectroscopy_peak_detection_engine_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/spectroscopy_peak_detection_engine.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.spectroscopy_peak_detection_engine.src.pipeline import run_spectroscopy_peak_detection_engine_pipeline; a = run_spectroscopy_peak_detection_engine_pipeline(Path('projects/spectroscopy_peak_detection_engine')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/spectroscopy_peak_detection_engine/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/spectroscopy_peak_detection_engine/notebooks/spectroscopy_peak_detection_engine.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
