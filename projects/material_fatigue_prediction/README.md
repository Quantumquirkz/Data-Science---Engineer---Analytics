# Material Fatigue Prediction

Portfolio research lab for **Material Fatigue Prediction**.

## Problem framing

Predict fatigue failure under repeated stress cycles from published materials datasets and benchmark fatigue databases.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

Reliability theory, survival analysis, regression, fracture mechanics intuition, uncertainty modeling.

## Data policy

Uses a reproducible synthetic dataset by default, with public-data replacement points documented.

## Project structure

- `src/config.py` - project metadata and domain/task configuration
- `src/data.py` - reproducible data generation/loading wrappers
- `src/preprocessing.py` - timestamp ordering, imputation, and numeric cleanup
- `src/features.py` - temporal, physical, interaction, and rolling features
- `src/modeling.py` - supervised or unsupervised models selected from the project task
- `src/evaluation.py` - metric summaries for reports and demos
- `src/visualization.py` - signal, projection, and validation plots
- `src/pipeline.py` - `run_material_fatigue_prediction_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/material_fatigue_prediction.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.material_fatigue_prediction.src.pipeline import run_material_fatigue_prediction_pipeline; a = run_material_fatigue_prediction_pipeline(Path('projects/material_fatigue_prediction')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/material_fatigue_prediction/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/material_fatigue_prediction/notebooks/material_fatigue_prediction.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
