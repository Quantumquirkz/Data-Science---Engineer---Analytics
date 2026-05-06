# Scientific Experiment Metadata Knowledge Graph

Portfolio research lab for **Scientific Experiment Metadata Knowledge Graph**.

## Problem framing

Build a knowledge graph linking experiments, instruments, variables, and outcomes from published papers, open metadata, and public repositories.

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

graph theory, ontology design, information retrieval, data modeling, graph analytics.

## Data policy

Uses generated graph/flow proxies by default; public logs or network datasets can be mapped into the same schema.

## Project structure

- `src/config.py` - project metadata and domain/task configuration
- `src/data.py` - reproducible data generation/loading wrappers
- `src/preprocessing.py` - timestamp ordering, imputation, and numeric cleanup
- `src/features.py` - temporal, physical, interaction, and rolling features
- `src/modeling.py` - supervised or unsupervised models selected from the project task
- `src/evaluation.py` - metric summaries for reports and demos
- `src/visualization.py` - signal, projection, and validation plots
- `src/pipeline.py` - `run_scientific_experiment_metadata_knowledge_graph_pipeline`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/scientific_experiment_metadata_knowledge_graph.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.scientific_experiment_metadata_knowledge_graph.src.pipeline import run_scientific_experiment_metadata_knowledge_graph_pipeline; a = run_scientific_experiment_metadata_knowledge_graph_pipeline(Path('projects/scientific_experiment_metadata_knowledge_graph')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/scientific_experiment_metadata_knowledge_graph/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/scientific_experiment_metadata_knowledge_graph/notebooks/scientific_experiment_metadata_knowledge_graph.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
