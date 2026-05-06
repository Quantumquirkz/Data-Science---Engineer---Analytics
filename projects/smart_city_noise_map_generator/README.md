# Smart City Noise Map Generator

Portfolio research lab for **Smart City Noise Map Generator**.

## Problem framing

Build dynamic urban noise maps using open city sound datasets, municipality sensor archives, and spatial interpolation.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

Geostatistics, interpolation, signal smoothing, spatial analytics, environmental modeling.

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
- `src/pipeline.py` - `run_smart_city_noise_map_generator_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/smart_city_noise_map_generator.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.smart_city_noise_map_generator.src.pipeline import run_smart_city_noise_map_generator_pipeline; a = run_smart_city_noise_map_generator_pipeline(Path('projects/smart_city_noise_map_generator')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/smart_city_noise_map_generator/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/smart_city_noise_map_generator/notebooks/smart_city_noise_map_generator.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
