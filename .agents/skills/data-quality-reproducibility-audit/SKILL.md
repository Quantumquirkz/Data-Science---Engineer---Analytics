---
name: data-quality-reproducibility-audit
description: Audit project data quality, command reproducibility, notebook/app run paths, schemas, missingness, dependencies, and documented execution steps.
---

# Data Quality And Reproducibility Audit

Use this skill when the user asks whether a project is reproducible, whether
data assumptions are safe, or whether documented commands actually work.

## Required Context

Read:

- `.agents/agents/qa-reproducibility-auditor.md`
- `.agents/rules/data-and-privacy-rules.md`
- `.agents/rules/review-and-release-rules.md`
- Relevant project `README.md` and `data/README.md`.

## Audit Workflow

1. **Inventory**
   - List relevant files.
   - Identify app, notebook, pipeline, and data entry points.

2. **Data checks**
   - Confirm `data/README.md` exists.
   - Check source/provenance notes.
   - Inspect small samples if present.
   - Flag undocumented raw datasets.

3. **Command checks**
   - Compare README commands to actual paths.
   - Prefer targeted smoke checks over broad expensive runs.
   - Use `uv run` unless the project documents another path.

4. **Import checks**
   - Import pipeline modules.
   - Run small deterministic pipeline functions when feasible.
   - Compile changed Python files when useful.

5. **Notebook/app checks**
   - Verify notebook file exists.
   - Verify app command points to an existing file.
   - Do not execute long notebooks unless requested.

## Common Commands

```bash
uv run python -c "import pandas, gradio; print('environment ready')"
uv run python -m compileall projects/<project_name>
uv run python projects/<project_name>/app.py
```

For app commands, avoid leaving long-running servers open unless the user wants
to interact with the app.

## Output Format

```markdown
## Audit Result
Pass / Partial / Fail

## Checks Run
- `<command>` - result

## Findings
1. [Severity] <Finding>
   Evidence:
   Impact:
   Fix:

## Data Quality Notes
- 

## Reproducibility Notes
- 

## Not Run
- <Check> because <reason>
```

## Exit Criteria

The audit is complete only when commands attempted, evidence, data risks, and
unverified areas are explicitly reported.
