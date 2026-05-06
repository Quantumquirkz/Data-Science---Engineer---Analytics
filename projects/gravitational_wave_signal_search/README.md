# Gravitational Wave Signal Search

Portfolio research lab for **Gravitational Wave Signal Search**.

## Problem framing

Search for faint gravitational wave-like patterns in noisy time series.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

matched filtering, signal detection theory, spectral methods, rare-event detection, statistical inference.

## Data policy

Compatible with open astronomy archives; default table emulates noisy detector/catalog measurements.

## Project structure

- `src/config.py` - project metadata and domain/task configuration
- `src/data.py` - reproducible data generation/loading wrappers
- `src/preprocessing.py` - timestamp ordering, imputation, and numeric cleanup
- `src/features.py` - temporal, physical, interaction, and rolling features
- `src/modeling.py` - supervised or unsupervised models selected from the project task
- `src/evaluation.py` - metric summaries for reports and demos
- `src/visualization.py` - signal, projection, and validation plots
- `src/pipeline.py` - `run_gravitational_wave_signal_search_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/gravitational_wave_signal_search.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.gravitational_wave_signal_search.src.pipeline import run_gravitational_wave_signal_search_pipeline; a = run_gravitational_wave_signal_search_pipeline(Path('projects/gravitational_wave_signal_search')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/gravitational_wave_signal_search/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/gravitational_wave_signal_search/notebooks/gravitational_wave_signal_search.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
