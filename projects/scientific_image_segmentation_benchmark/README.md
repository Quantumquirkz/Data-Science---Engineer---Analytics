# Scientific Image Segmentation Benchmark

Portfolio research lab for **Scientific Image Segmentation Benchmark**.

## Problem framing

Compare segmentation methods on microscopy, materials, or astronomy images.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

image processing, segmentation, optimization, evaluation metrics, deep learning.

## Data policy

Compatible with open astronomy archives; default table emulates noisy detector/catalog measurements.

## Project structure

- `src/config.py` - project metadata and domain/task configuration
- `src/data.py` - reproducible data generation/loading wrappers
- `src/preprocessing.py` - timestamp ordering, imputation, and numeric cleanup
- `src/features.py` - temporal, physical, interaction, and rolling features
- `src/modeling.py` - supervised or unsupervised models selected from the project task
- `src/evaluation.py` - metric summaries for reports and demos
- `src/visualization.py` - signal, projection, and validation plots
- `src/pipeline.py` - `run_scientific_image_segmentation_benchmark_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/scientific_image_segmentation_benchmark.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.scientific_image_segmentation_benchmark.src.pipeline import run_scientific_image_segmentation_benchmark_pipeline; a = run_scientific_image_segmentation_benchmark_pipeline(Path('projects/scientific_image_segmentation_benchmark')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/scientific_image_segmentation_benchmark/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/scientific_image_segmentation_benchmark/notebooks/scientific_image_segmentation_benchmark.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
