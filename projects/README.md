# Projects

This directory is the canonical home for the 100 portfolio projects.

## Identity Model

- Physical folders remain slug-based: `projects/<slug>/`.
- Stable project IDs live in each `project.yaml`: `p001` through `p100`.
- `projects/registry.yaml` is the cross-project index.
- Tooling resolves both IDs and slugs through the central registry.
- The repository does not duplicate project folders for aliases.

## Required Project Shape

```text
projects/<slug>/
  project.yaml
  README.md
  app.py
  data/
  notebooks/
  src/
```

Some projects also include `tests/`, `reports/`, `pipelines/`, or
domain-specific modules when the project requires them.

## Template Families

- `analytics_project` - exploratory analysis, dashboards, reporting, and
  communication.
- `data_science_project` - statistics, features, modeling, evaluation, and
  interpretation.
- `data_engineering_project` - ingestion, validation, transformations, and
  scalable data workflows.
- `ml_engineering_project` - training pipelines, inference interfaces, and
  operational patterns.
- `scientific_computing_project` - simulation, numerical methods, and
  scientific visualization.
- `capstone_project` - multi-role end-to-end systems.

## Compatibility

Existing imports such as `projects.<slug>.src...` remain valid. New discovery
and documentation should use project metadata instead of assuming only a flat
filesystem scan.
