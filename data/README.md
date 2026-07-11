# Shared Data Lifecycle

This top-level directory defines the repository-wide data lifecycle policy.

## Storage classes

- `raw/` - immutable source inputs when redistribution is allowed.
- `external/` - downloaded or externally sourced assets kept out of Git by
  default.
- `interim/` - temporary transformed data products.
- `processed/` - finalized derived datasets for reproducible downstream use.
- `samples/` - compact example assets safe to commit.

## Current policy

- Per-project data directories remain valid and are still the baseline for
  self-contained execution.
- This top-level structure is a shared convention and future aggregation
  surface.
- DVC is intentionally not required yet, but the directory boundaries are chosen
  so DVC can be added later without reorganizing the repository again.
