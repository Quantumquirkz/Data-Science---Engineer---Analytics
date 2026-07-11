# Data Intelligence Engineering Agent Guide

Repository: `Quantumquirkz/data-intelligence-engineering`  
Author: Jhuomar Boskoll Quintero

This file is the root operating guide for AI-assisted work in this repository.
It adapts the role-and-skill workflow pattern from `garrytan/gstack` to a Python
portfolio-lab focused on data science, data engineering, analytics, ML
engineering, and scientific computing.

## First Context To Read

Before making non-trivial changes, read:

1. `.context/README.md`
2. `.context/repository-overview.md`
3. `.context/architecture.md`
4. `.context/engineering-conventions.md`
5. The relevant project `README.md` and `src/` modules.

Use `rg` and `rg --files` for discovery. Do not assume a project follows the
template perfectly until you inspect it.

## Operating Principles

- Protect the user's existing work. Do not revert unrelated changes.
- Prefer complete, reproducible, maintainable changes over fragile shortcuts.
- Put reusable logic in `src/`; keep notebooks as narratives and validation
  surfaces.
- Preserve `uv` as the dependency and execution path.
- Treat data provenance, leakage, missingness, units, and schema assumptions as
  first-class engineering concerns.
- For modeling work, include baselines, validation strategy, metrics, seeds, and
  limitations.
- For scientific or simulation work, document numerical assumptions, stability
  constraints, and error behavior.
- For generated documentation, match the current repository state rather than a
  hypothetical ideal.

## Local Agent System

The local role, rule, and skill system lives in `.agents/`.

- `.agents/agents/` contains specialist role definitions.
- `.agents/rules/` contains reusable operating rules.
- `.agents/skills/` contains task workflows in `SKILL.md` format.
- `.agents/README.md` explains routing and expected usage.

## How To Invoke Agents, Rules, And Skills In Every Prompt

For best results, every prompt about this repository should explicitly name the
agent role, rule packs, and skill workflow that should govern the work. Use this
shape:

```text
Use agent: <agent-name>.
Apply rules: <rule-file-1>, <rule-file-2>.
Invoke skill: <skill-name>.
Task: <specific request>.
Evidence required: <commands, files, or artifacts that prove completion>.
```

Example:

```text
Use agent: ML Research Scientist.
Apply rules: scientific-ml-quality-rules, data-and-privacy-rules.
Invoke skill: ml-experiment-review.
Task: Review projects/sensor_drift_detection for leakage, metrics, and validation gaps.
Evidence required: cite files/lines and list any commands run.
```

If the user does not name an agent, rule, or skill, the assistant must infer the
smallest appropriate combination from the request, state the routing briefly,
and then continue. Do not stop merely to ask which agent to use unless the task
is genuinely ambiguous and the wrong routing would cause risky edits.

Invocation names:

- Agents are invoked by title, for example `Data Platform Architect`.
- Rules are invoked by file stem, for example `scientific-ml-quality-rules`.
- Skills are invoked by skill name, for example `data-project-spec`.

The correct execution order is:

1. Read `AGENTS.md`.
2. Read the selected agent file from `.agents/agents/`.
3. Read the selected rule files from `.agents/rules/`.
4. Read the selected skill `SKILL.md` from `.agents/skills/`.
5. Inspect the relevant repository files.
6. Perform the task.
7. Validate with evidence.
8. Report which agent, rules, and skill were used.

## Skill Routing

When a user request matches a local skill, follow that skill's `SKILL.md`.
If multiple skills apply, use the smallest sequence that covers the task.

Use these routes:

- New project, vague idea, or project backlog item:
  `.agents/skills/data-project-spec/SKILL.md`
- Architecture, pipeline, module boundaries, performance, or data flow review:
  `.agents/skills/data-pipeline-architecture-review/SKILL.md`
- Model training, evaluation, experiment design, leakage, or metric review:
  `.agents/skills/ml-experiment-review/SKILL.md`
- Data validation, reproducibility, notebook execution, or smoke testing:
  `.agents/skills/data-quality-reproducibility-audit/SKILL.md`
- README, docs, portfolio narrative, diagrams, or context generation:
  `.agents/skills/portfolio-documentation-generate/SKILL.md`
- Secrets, privacy, data governance, dependency risk, or threat modeling:
  `.agents/skills/security-data-governance-audit/SKILL.md`
- End-to-end app/notebook/pipeline QA:
  `.agents/skills/project-qa-smoke-test/SKILL.md`

## Review Posture

For reviews, lead with concrete findings ordered by severity. Include file and
line references when available. Focus on defects, data leakage, reproducibility
breaks, invalid metrics, unstable numerical behavior, privacy issues, and stale
documentation. If there are no findings, say that directly and mention residual
risk or unrun checks.

## Validation Baseline

Prefer targeted validation over running the entire repository when the change is
local. Common commands:

```bash
uv run python -c "import pandas, gradio; print('environment ready')"
uv run python -m compileall projects
uv run jupyter lab
```

For a specific project, use its pipeline or app command from the project
`README.md`. If a command cannot run because dependencies or data are missing,
report that fact with the exact command attempted.

## Destructive Actions

Never run destructive commands such as `git reset --hard`, force push, broad
deletes, dataset overwrites, or environment removal unless the user explicitly
requests that action and the target is unambiguous.
