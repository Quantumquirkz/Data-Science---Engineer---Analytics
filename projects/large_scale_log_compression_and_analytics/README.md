# Large-Scale Log Compression and Analytics

Portfolio research lab for **Large-Scale Log Compression and Analytics**.

## Problem framing

Build a pipeline to compress, index, and analyze massive machine-generated logs.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

Information theory, streaming algorithms, distributed data processing, anomaly detection.

## Data policy

Uses synthetic process telemetry by default because production datasets are often proprietary.

## Project structure

- `src/config.py` - project metadata and domain/task configuration
- `src/data.py` - reproducible data generation/loading wrappers
- `src/preprocessing.py` - timestamp ordering, imputation, and numeric cleanup
- `src/features.py` - temporal, physical, interaction, and rolling features
- `src/modeling.py` - supervised or unsupervised models selected from the project task
- `src/evaluation.py` - metric summaries for reports and demos
- `src/visualization.py` - signal, projection, and validation plots
- `src/pipeline.py` - `run_large_scale_log_compression_and_analytics_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/large_scale_log_compression_and_analytics.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.large_scale_log_compression_and_analytics.src.pipeline import run_large_scale_log_compression_and_analytics_pipeline; a = run_large_scale_log_compression_and_analytics_pipeline(Path('projects/large_scale_log_compression_and_analytics')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/large_scale_log_compression_and_analytics/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/large_scale_log_compression_and_analytics/notebooks/large_scale_log_compression_and_analytics.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
