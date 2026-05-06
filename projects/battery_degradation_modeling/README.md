# Battery Degradation Modeling

Portfolio research lab for **Battery Degradation Modeling**.

## Problem framing

Predict battery health and remaining useful life from public battery cycle datasets collected in prior experiments.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

Electrochemistry intuition, survival analysis, time series, regression, degradation modeling, uncertainty quantification.

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
- `src/pipeline.py` - `run_battery_degradation_modeling_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/battery_degradation_modeling.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.battery_degradation_modeling.src.pipeline import run_battery_degradation_modeling_pipeline; a = run_battery_degradation_modeling_pipeline(Path('projects/battery_degradation_modeling')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/battery_degradation_modeling/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/battery_degradation_modeling/notebooks/battery_degradation_modeling.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
