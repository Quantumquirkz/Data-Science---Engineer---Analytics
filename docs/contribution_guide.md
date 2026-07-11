# Contribution Guide

## New shared code

Place repository-wide reusable logic in `src/data_intelligence_engineering/`.

## New project code

Place domain-specific logic inside the relevant project directory under
`projects/<slug>/src/`.

## New projects

Use `scripts/new_project.py` as the starting scaffold and then register the
project in the central registry if needed.

## Validation

Use:

- `scripts/validate_project_structure.py`
- `scripts/run_smoke_checks.py`

before treating structural changes as complete.
