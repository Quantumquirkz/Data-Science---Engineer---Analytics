# Ocean Buoy Wave Energy Estimator

Portfolio research lab for **Ocean Buoy Wave Energy Estimator**.

## Problem framing

Estimate wave energy potential from open buoy measurements and environmental signals from oceanographic repositories.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

Spectral analysis, stochastic wave modeling, signal decomposition, regression, ocean dynamics basics.

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
- `src/pipeline.py` - `run_ocean_buoy_wave_energy_estimator_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/ocean_buoy_wave_energy_estimator.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.ocean_buoy_wave_energy_estimator.src.pipeline import run_ocean_buoy_wave_energy_estimator_pipeline; a = run_ocean_buoy_wave_energy_estimator_pipeline(Path('projects/ocean_buoy_wave_energy_estimator')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/ocean_buoy_wave_energy_estimator/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/ocean_buoy_wave_energy_estimator/notebooks/ocean_buoy_wave_energy_estimator.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
