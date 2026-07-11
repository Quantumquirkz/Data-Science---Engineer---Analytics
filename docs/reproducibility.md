# Reproducibility

Repository reproducibility currently relies on:

- `uv` dependency management
- explicit project paths
- project-local data and notebook layouts
- repository-wide artifact lifecycle standards

## Current expectation

- commands should run from the repository root
- project pipelines should live in `src/` modules under each project
- notebooks should remain narrative surfaces, not the only implementation
- shared logic should move into `src/data_intelligence_engineering/`
