# Documentation Rules

Documentation should make the repository easier to run, evaluate, and trust.

## Required Project README Sections

Use these sections unless a project has a good reason to differ:

- Project title.
- What the project does.
- Why it matters.
- Data source or simulation strategy.
- Methodology.
- Project structure.
- How to run.
- Metrics or outputs.
- Limitations.
- Suggested extensions.

## Diagrams

Use Mermaid for:

- Workflow diagrams.
- Architecture diagrams.
- Data lineage.
- Model pipelines.
- Domain taxonomies.

Keep Mermaid labels simple and renderer-compatible.

## Notebook Narratives

Notebooks should:

- Explain the question.
- Load data through project modules when possible.
- Show intermediate diagnostics.
- Report metrics.
- Link back to reusable code.

## Staleness Rule

When code, commands, dependencies, or project structure change, update the
nearest README or `.context/` document that would otherwise become stale.
