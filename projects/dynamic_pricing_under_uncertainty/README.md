# Dynamic Pricing Under Uncertainty

Portfolio research lab for **Dynamic Pricing Under Uncertainty**.

## Problem framing

Optimize prices using historical demand and uncertain future conditions.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

optimization, stochastic modeling, causal inference basics, reinforcement learning, econometrics.

## Data policy

Public-first when stable market samples are available; synthetic fallback for offline demos.

## Project structure

- `src/config.py` - project metadata and domain/task configuration
- `src/data.py` - reproducible data generation/loading wrappers
- `src/preprocessing.py` - timestamp ordering, imputation, and numeric cleanup
- `src/features.py` - temporal, physical, interaction, and rolling features
- `src/modeling.py` - supervised or unsupervised models selected from the project task
- `src/evaluation.py` - metric summaries for reports and demos
- `src/visualization.py` - signal, projection, and validation plots
- `src/pipeline.py` - `run_dynamic_pricing_under_uncertainty_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/dynamic_pricing_under_uncertainty.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.dynamic_pricing_under_uncertainty.src.pipeline import run_dynamic_pricing_under_uncertainty_pipeline; a = run_dynamic_pricing_under_uncertainty_pipeline(Path('projects/dynamic_pricing_under_uncertainty')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/dynamic_pricing_under_uncertainty/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/dynamic_pricing_under_uncertainty/notebooks/dynamic_pricing_under_uncertainty.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
