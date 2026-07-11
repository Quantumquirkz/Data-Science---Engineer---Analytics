---
name: portfolio-documentation-generate
description: Generate or update repository, project, context, or portfolio documentation using evidence from the current codebase and Diataxis-style coverage.
---

# Portfolio Documentation Generate

Use this skill for README files, project docs, `.context` updates, architecture
explanations, diagrams, and portfolio narratives.

## Required Context

Read:

- `.context/README.md`
- `.context/repository-overview.md`
- `.agents/agents/analytics-storyteller.md`
- `.agents/rules/documentation-rules.md`

Then inspect the files being documented. Do not write docs from memory alone.

## Documentation Modes

Use the Diataxis lens:

- **Tutorial**: guided learning path.
- **How-to**: task-oriented instructions.
- **Reference**: exact structure, commands, APIs, or module descriptions.
- **Explanation**: reasoning, concepts, architecture, and tradeoffs.

Project READMEs usually need a blend of how-to, explanation, and reference.

## Workflow

1. **Inspect**
   - Read relevant code, notebooks, and existing docs.
   - Identify stale or missing claims.

2. **Map audience**
   - Learner.
   - Technical reviewer.
   - Collaborator.
   - Future AI agent.

3. **Write structure**
   - Problem.
   - Data.
   - Method.
   - Execution.
   - Outputs.
   - Limitations.

4. **Add diagrams**
   - Use Mermaid for architecture or workflow.
   - Keep labels short.

5. **Validate**
   - Check links and paths.
   - Validate JSON/YAML if created.
   - Mention commands not run.

## Output Expectations

Documentation must be:

- Evidence-based.
- Written in clear English unless otherwise requested.
- Specific to this repository.
- Free of invented metrics or fake results.
- Honest about limitations.

## Exit Criteria

The documentation task is complete only when the updated files exist, are linked
or discoverable, and do not contradict the inspected code.
