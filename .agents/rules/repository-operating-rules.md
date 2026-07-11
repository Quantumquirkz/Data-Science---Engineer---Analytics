# Repository Operating Rules

These rules apply to all AI-assisted work in this repository.

## Source Of Truth

- Current files in the worktree are authoritative.
- `.context/` explains repository intent and architecture.
- `README.md`, `docs/PROJECTS.md`, and project `README.md` files explain public
  behavior and project purpose.
- `pyproject.toml` and `uv.lock` define the dependency environment.

## Worktree Safety

- Do not revert user changes.
- Do not clean, reset, delete, or overwrite unrelated files.
- Treat existing dirty files as user work unless proven otherwise.
- Keep edits scoped to the requested outcome.

## Implementation Rules

- Prefer repository patterns over new abstractions.
- Keep project logic in `src/` modules.
- Keep notebooks narrative and exploratory.
- Use `uv run` for execution examples.
- Do not add dependencies without updating `pyproject.toml`.
- Do not hardcode local absolute paths.

## File Organization

New portfolio projects should follow:

```text
projects/<project_name>/
  README.md
  app.py
  data/README.md
  notebooks/<project_name>.ipynb
  src/
```

Use `projects/_portfolio_common/` only for generic shared utilities.
