# Astronomical Light Curve Classifier

Portfolio research lab for **Astronomical Light Curve Classifier**.

## Problem framing

Classify stars, exoplanet transits, or variable objects from light curve data.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

Time series, frequency-domain methods, supervised learning, probabilistic classification, astrophysics basics.

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
- `src/pipeline.py` - `run_astronomical_light_curve_classifier_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/astronomical_light_curve_classifier.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.astronomical_light_curve_classifier.src.pipeline import run_astronomical_light_curve_classifier_pipeline; a = run_astronomical_light_curve_classifier_pipeline(Path('projects/astronomical_light_curve_classifier')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/astronomical_light_curve_classifier/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/astronomical_light_curve_classifier/notebooks/astronomical_light_curve_classifier.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
