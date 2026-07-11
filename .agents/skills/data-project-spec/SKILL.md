---
name: data-project-spec
description: Turn a vague data, analytics, scientific computing, or ML idea into a scoped repository-ready project specification for this portfolio.
---

# Data Project Spec

Use this skill when the user wants a new project, wants to refine a project
idea, or asks for a plan before implementation.

## Goal

Produce a precise, executable project specification that fits
`Quantumquirkz/data-intelligence-engineering`.

## Required Context

Read:

- `.context/repository-overview.md`
- `.context/architecture.md`
- `.context/project-taxonomy.md`
- `.agents/agents/data-product-strategist.md`
- `.agents/agents/data-platform-architect.md`
- `.agents/rules/scientific-ml-quality-rules.md`

Inspect `docs/PROJECTS.md` and `projects/` to avoid duplicating existing work
unless the user explicitly wants a variant.

## Workflow

1. **Frame the problem**
   - Define the domain, user, decision, and expected impact.
   - State whether the project is analytical, predictive, simulation-based,
     dashboard-oriented, or ML engineering-oriented.

2. **Define data strategy**
   - Identify public, synthetic, benchmark, or simulated data options.
   - Document expected schema, units, target variable, and known risks.
   - Flag privacy, licensing, or availability constraints.

3. **Define method strategy**
   - Include a baseline.
   - Include the main analytical or modeling method.
   - Include evaluation metrics and validation strategy.
   - State scientific assumptions and failure modes.

4. **Map repository structure**
   - Use `projects/<snake_case_name>/`.
   - Include `README.md`, `app.py`, `data/README.md`, `notebooks/`, and `src/`.
   - Decide whether `projects/_portfolio_common/` is useful or unnecessary.

5. **Define deliverables**
   - Reusable pipeline.
   - Notebook walkthrough.
   - Optional Gradio demo.
   - Metrics and plots.
   - README and limitations.

## Output Template

```markdown
# Project Spec: <Title>

## Thesis
<One paragraph explaining the project and why it matters.>

## Scope
- In scope:
- Out of scope:

## Data Strategy
- Source:
- Schema:
- Quality risks:
- Privacy/licensing:

## Methodology
- Baseline:
- Main method:
- Features:
- Validation:
- Metrics:

## Repository Structure
<Proposed tree.>

## Execution Plan
1.
2.
3.

## Acceptance Criteria
- <Runnable command or artifact exists.>
- <Metric/report exists.>
- <Docs updated.>

## Risks And Limitations
- 
```

## Exit Criteria

The spec is complete only when it names the project location, data strategy,
baseline, evaluation method, deliverables, and acceptance criteria.
