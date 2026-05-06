# Radiative Cooling Efficiency Predictor

Portfolio research lab for **Radiative Cooling Efficiency Predictor**.

## Problem framing

Model cooling performance of materials under varying thermal and radiative conditions using published experimental datasets or simulation outputs.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

Heat transfer, radiative physics, regression, optimization, uncertainty analysis, experimental modeling.

## Data policy

Simulation-first project with reproducible stochastic scenarios.

## Project structure

- `src/config.py` - project metadata and domain/task configuration
- `src/data.py` - reproducible data generation/loading wrappers
- `src/preprocessing.py` - timestamp ordering, imputation, and numeric cleanup
- `src/features.py` - temporal, physical, interaction, and rolling features
- `src/modeling.py` - supervised or unsupervised models selected from the project task
- `src/evaluation.py` - metric summaries for reports and demos
- `src/visualization.py` - signal, projection, and validation plots
- `src/pipeline.py` - `run_radiative_cooling_efficiency_predictor_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/radiative_cooling_efficiency_predictor.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.radiative_cooling_efficiency_predictor.src.pipeline import run_radiative_cooling_efficiency_predictor_pipeline; a = run_radiative_cooling_efficiency_predictor_pipeline(Path('projects/radiative_cooling_efficiency_predictor')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/radiative_cooling_efficiency_predictor/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/radiative_cooling_efficiency_predictor/notebooks/radiative_cooling_efficiency_predictor.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
