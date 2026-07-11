---
name: project-qa-smoke-test
description: Run a targeted end-to-end smoke test for one repository project, including imports, pipeline execution, app path checks, docs commands, and final evidence.
---

# Project QA Smoke Test

Use this skill when the user asks "does this project work?", "QA this project",
"test the app", "verify the pipeline", or similar.

## Required Context

Read:

- `.agents/agents/qa-reproducibility-auditor.md`
- `.agents/rules/review-and-release-rules.md`
- The target project `README.md`.

## Workflow

1. **Resolve target**
   - Identify the project directory.
   - If ambiguous, inspect `projects/` and choose the closest match only when
     the user's intent is clear.

2. **Static checks**
   - Confirm expected files exist.
   - Check README commands.
   - Compile Python files if feasible.

3. **Import checks**
   - Import the project package.
   - Import the pipeline module.
   - Import major modules touched by the current change.

4. **Pipeline smoke check**
   - Run the smallest documented or discoverable pipeline function.
   - Use synthetic or built-in sample data when available.
   - Avoid long model training unless explicitly requested.

5. **App check**
   - Confirm `app.py` exists.
   - If launching a server is required, run it only long enough to verify
     startup unless the user wants an interactive URL.

6. **Report**
   - Include commands.
   - Include pass/fail.
   - Include unverified areas.

## Output Format

```markdown
## QA Smoke Test Result
Pass / Partial / Fail

## Target
`projects/<name>`

## Commands Run
- `<command>` - result

## Findings
1. [Severity] <Finding>
   Evidence:
   Fix:

## Unverified
- 

## Ship Readiness
Ready / Not ready / Ready with caveats
```

## Exit Criteria

The smoke test is complete only when at least one static check and one runtime
or import check have been attempted, or when a clear blocker prevents runtime
validation.
