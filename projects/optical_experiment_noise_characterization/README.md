# Optical Experiment Noise Characterization

Portfolio research lab for **Optical Experiment Noise Characterization**.

## Problem framing

Quantify noise sources in repeated optical measurements and identify dominant contributors using openly published optics datasets or synthetic noise experiments.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

Error analysis, statistical estimation, noise models, experimental physics methodology.

## Data policy

Uses synthetic spectral/time-series measurements with documented public-data extension points.

## Project structure

- `src/config.py` - project metadata and domain/task configuration
- `src/data.py` - reproducible data generation/loading wrappers
- `src/preprocessing.py` - timestamp ordering, imputation, and numeric cleanup
- `src/features.py` - temporal, physical, interaction, and rolling features
- `src/modeling.py` - supervised or unsupervised models selected from the project task
- `src/evaluation.py` - metric summaries for reports and demos
- `src/visualization.py` - signal, projection, and validation plots
- `src/pipeline.py` - `run_optical_experiment_noise_characterization_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/optical_experiment_noise_characterization.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.optical_experiment_noise_characterization.src.pipeline import run_optical_experiment_noise_characterization_pipeline; a = run_optical_experiment_noise_characterization_pipeline(Path('projects/optical_experiment_noise_characterization')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/optical_experiment_noise_characterization/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/optical_experiment_noise_characterization/notebooks/optical_experiment_noise_characterization.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
