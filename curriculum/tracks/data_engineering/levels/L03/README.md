# Data Engineering L03: Databases And Data Modeling

Status: **implemented**

## Role Question

How does data move, stay valid, and remain trustworthy at scale?

## Level Intent

Choose tables, keys, and grain that preserve semantics.

This level is part of a **self-paced, no-grade learning system**. The learner decides the pace. Evidence matters more than completion counters.

## Theory Spine

\[
\text{throughput} = \frac{\text{records processed}}{\text{time}}, \qquad \text{latency} = t_{out} - t_{in}
\]

Interpret the equation as a compact statement of what the level treats as signal, state, or evidence.

## Lesson Focus

- Normalization
- Join integrity
- Entity boundaries

## What To Practice

- Read the linked notebook or project README and restate the problem in your own words.
- Identify what can be measured directly and what must be estimated.
- Explain one assumption that, if false, would change the conclusion.

## Mission Anchor

- Project ID: `p041`
- Mission ID: `p041-de-l03-m01`
- Delivery surface: `README + notebook + project execution command`

## Evidence Without Grades

A learner can mark this level as `exploring`, `practiced`, `demonstrated`, or `extended`.

`demonstrated` means:

1. The learner can explain the core concept without copying definitions.
2. The learner can run the linked notebook or command.
3. The learner can describe assumptions, units, and likely errors.

## Notebook Surface

Open [`notebooks/tracks/data_engineering/L03/data_engineering_l03_databases_and_data_modeling.ipynb`](../../../../notebooks/tracks/data_engineering/L03/data_engineering_l03_databases_and_data_modeling.ipynb).

## Colab And uv

Use `uv` locally for reproducible execution. Use Colab when local compute or package installation is a barrier, but keep the same scientific narrative and assumptions.
