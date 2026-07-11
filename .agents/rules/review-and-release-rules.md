# Review And Release Rules

This repository is a portfolio and learning system, so "release" usually means
that the work is ready to be committed, pushed, demonstrated, or reviewed.

## Review Priorities

Review in this order:

1. Correctness and data validity.
2. Reproducibility.
3. Security and privacy.
4. Maintainability.
5. Performance.
6. Documentation.
7. Style.

## Required Evidence

A finished change should have evidence:

- Files changed.
- Commands run.
- Tests or smoke checks passed.
- Checks not run and why.
- Known residual risk.

## Code Review Output

Lead with findings. Each finding should include:

- Severity.
- File and line when available.
- What breaks.
- Why it matters.
- Suggested fix.

## Release Readiness

Before calling work complete, verify:

- The requested artifact exists.
- It is linked or discoverable.
- JSON/YAML/Markdown syntax is valid when applicable.
- Commands in docs are plausible or tested.
- No unrelated user changes were reverted.
