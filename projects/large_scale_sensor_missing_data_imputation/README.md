# Large-Scale Sensor Missing Data Imputation

Portfolio research lab for **Large-Scale Sensor Missing Data Imputation**.

## Problem framing

Impute missing values across thousands of sensor streams with temporal and spatial structure using public IoT, weather, or industrial telemetry datasets.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

Matrix completion, time series interpolation, probabilistic modeling, optimization, low-rank approximation.

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
- `src/pipeline.py` - `run_large_scale_sensor_missing_data_imputation_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/large_scale_sensor_missing_data_imputation.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.large_scale_sensor_missing_data_imputation.src.pipeline import run_large_scale_sensor_missing_data_imputation_pipeline; a = run_large_scale_sensor_missing_data_imputation_pipeline(Path('projects/large_scale_sensor_missing_data_imputation')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/large_scale_sensor_missing_data_imputation/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/large_scale_sensor_missing_data_imputation/notebooks/large_scale_sensor_missing_data_imputation.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
