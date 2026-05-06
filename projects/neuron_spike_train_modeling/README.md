# Neuron Spike Train Modeling

Portfolio research lab for **Neuron Spike Train Modeling**.

## Problem framing

Model neural spike trains and infer activity patterns from electrophysiology data.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

point processes, stochastic modeling, time series, information theory, statistical neuroscience.

## Data policy

Uses privacy-safe synthetic proxies by default; public biomedical datasets can replace the source table.

## Project structure

- `src/config.py` - project metadata and domain/task configuration
- `src/data.py` - reproducible data generation/loading wrappers
- `src/preprocessing.py` - timestamp ordering, imputation, and numeric cleanup
- `src/features.py` - temporal, physical, interaction, and rolling features
- `src/modeling.py` - supervised or unsupervised models selected from the project task
- `src/evaluation.py` - metric summaries for reports and demos
- `src/visualization.py` - signal, projection, and validation plots
- `src/pipeline.py` - `run_neuron_spike_train_modeling_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/neuron_spike_train_modeling.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.neuron_spike_train_modeling.src.pipeline import run_neuron_spike_train_modeling_pipeline; a = run_neuron_spike_train_modeling_pipeline(Path('projects/neuron_spike_train_modeling')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/neuron_spike_train_modeling/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/neuron_spike_train_modeling/notebooks/neuron_spike_train_modeling.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
