# Engineering Conventions

These conventions describe how future work should fit into
`Quantumquirkz/data-intelligence-engineering`.

## General Principles

- Keep project logic modular and reusable.
- Prefer explicit data contracts over hidden notebook state.
- Keep notebooks as narratives, not as the only implementation.
- Preserve reproducibility through `uv`, `pyproject.toml`, and `uv.lock`.
- Make assumptions visible in documentation, configuration, and function names.
- Treat each project as both a learning artifact and a portfolio artifact.

## Project Structure Conventions

New portfolio projects should generally use:

```text
projects/<snake_case_project_name>/
  README.md
  app.py
  data/
    README.md
  notebooks/
    <snake_case_project_name>.ipynb
  src/
    __init__.py
    config.py
    data.py
    preprocessing.py
    features.py
    modeling.py
    evaluation.py
    visualization.py
    inference.py
    pipeline.py
```

Use additional modules only when a domain concept deserves a clear boundary.
Examples include `drift_detection.py`, `simulation.py`, `optimization.py`,
`signal_processing.py`, or `bayesian_modeling.py`.

## Naming

- Directories: `snake_case`.
- Python modules: `snake_case.py`.
- Functions: verb-oriented `snake_case`, such as `load_dataset`,
  `build_features`, `train_model`, or `run_pipeline`.
- Project notebooks: match the project directory name where possible.
- Public-facing titles: human-readable title case in project `README.md` files.

## Data Conventions

- Prefer public datasets, generated synthetic data, or small samples.
- Avoid committing large raw data unless there is a clear repository reason.
- Document data provenance in `data/README.md`.
- Keep generated outputs out of source control unless they are intentionally
  small, stable examples.
- Validate assumptions about missingness, units, time zones, schemas, and
  target leakage.

## Modeling Conventions

Modeling code should make the following explicit:

- Baseline method.
- Main model or analytical method.
- Feature set.
- Train/test or validation strategy.
- Metrics.
- Random seeds where stochastic behavior matters.
- Known limitations.

For scientific or simulation projects, document numerical assumptions such as:

- Time step or spatial resolution.
- Boundary conditions.
- Stability constraints.
- Error metrics.
- Approximation limits.

## Evaluation Conventions

Evaluation should be domain-aware:

- Classification: precision, recall, F1, confusion matrix, calibration when
  useful.
- Regression: MAE, RMSE, R2, residual diagnostics, error distribution.
- Forecasting: horizon-specific metrics, backtesting, leakage checks.
- Anomaly detection: false alarm rate, detection delay, precision/recall under
  event labels.
- Simulation: conservation checks, analytical comparisons, convergence behavior.

## Documentation Conventions

Each project `README.md` should explain:

- What the project does.
- Why the problem matters.
- Data source or simulation strategy.
- Methodology.
- Project structure.
- How to run the app or notebook.
- Metrics and expected outputs.
- Suggested extensions.

## Mermaid Usage

Mermaid diagrams are encouraged for:

- Workflow diagrams.
- Architecture maps.
- Data lineage.
- Model pipelines.
- Domain method taxonomies.

Keep diagram node labels concise and avoid syntax that may fail in standard
Markdown Mermaid renderers.

## Reliability And Maintenance

Future changes should avoid:

- Duplicating project logic in notebooks and apps.
- Introducing dependencies without adding them to `pyproject.toml`.
- Hardcoding absolute local paths.
- Assuming network availability inside core project logic.
- Committing secrets, credentials, tokens, or private datasets.
- Rewriting unrelated files during focused changes.

## Recommended Validation Commands

Common checks from the repository root:

```bash
uv sync
uv run python -c "import pandas, gradio; print('environment ready')"
uv run jupyter lab
```

Project-specific smoke checks should import and run the relevant pipeline
function when available.
