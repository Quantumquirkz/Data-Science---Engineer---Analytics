# Financial Volatility Surface Predictor

Portfolio research lab for **Financial Volatility Surface Predictor**.

## Problem framing

Model volatility surfaces from options market data.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

Stochastic calculus, interpolation, regression, optimization, quantitative finance modeling.

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
- `src/pipeline.py` - `run_financial_volatility_surface_predictor_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/financial_volatility_surface_predictor.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.financial_volatility_surface_predictor.src.pipeline import run_financial_volatility_surface_predictor_pipeline; a = run_financial_volatility_surface_predictor_pipeline(Path('projects/financial_volatility_surface_predictor')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/financial_volatility_surface_predictor/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/financial_volatility_surface_predictor/notebooks/financial_volatility_surface_predictor.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
