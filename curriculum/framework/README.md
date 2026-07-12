# Curriculum Framework

This repository now treats learning as a **mission graph** instead of a flat reading list.

## Design Principles

- Teaching-first: explanations, notebooks, and project READMEs are the primary surface.
- Open source first: a learner should be able to study from cloned files without platform lock-in.
- No grades: the repository does not centralize scoring, ranking, or punitive gating.
- Ten levels per discipline: each role has its own complete route from foundations to capstone practice.
- Shared project worlds: one project can host different missions for analytics, science, engineering, and computational reasoning.

## Evidence States

Use these local, optional states instead of grades:

- `not_started`
- `exploring`
- `practiced`
- `demonstrated`
- `extended`

## Runtime Contract

All teaching content assumes two canonical execution surfaces:

- `uv` for local reproducible work
- Colab for lightweight cloud notebook execution

## Mathematical Contract

A complete learning artifact should support three depths:

\[
\text{applied} \subset \text{graduate} \subset \text{research preparation}
\]

This means the same topic should be understandable operationally, derivable formally, and extensible critically.

## Teaching Quality Contract

A level is not considered complete only because a file exists. Every implemented
level must help a learner who starts from zero.

Required level README sections:

- `Start From Zero`
- `Step-By-Step Learning Path`
- `Worked Micro-Example`
- `Guided Practice`
- `Before You Move On`

Required notebook behavior:

- At least 10 teaching cells.
- Plain-language vocabulary before tools.
- A small executable cell that does not require large data.
- A guided reasoning exercise.
- A self-check section with no grades.

These requirements are enforced by `validate_curriculum()` and
`scripts/validate_project_structure.py`.
