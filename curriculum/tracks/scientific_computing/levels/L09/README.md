# Scientific Computing L09: Multiphysics, Surrogates, And Data Assimilation

Status: **implemented**

## Role Question

How do equations, numerical methods, and simulations become trustworthy computational evidence?

## Level Intent

Blend simulation, statistical updates, and learned surrogates.

This level is part of a **self-paced, no-grade learning system**. The learner decides the pace. Evidence matters more than completion counters.

## Theory Spine

\[
\frac{d\mathbf{x}}{dt} = f(\mathbf{x}, t), \qquad \epsilon_h = \lVert x - x_h \rVert
\]

Interpret the equation as a compact statement of what the level treats as signal, state, or evidence.

## Lesson Focus

- State estimation
- Hybrid modeling
- Assimilation loops

## What To Practice

- Read the linked notebook or project README and restate the problem in your own words.
- Identify what can be measured directly and what must be estimated.
- Explain one assumption that, if false, would change the conclusion.

## Mission Anchor

- Project ID: `p088`
- Mission ID: `p088-sc-l09-m01`
- Delivery surface: `README + notebook + project execution command`

## Evidence Without Grades

A learner can mark this level as `exploring`, `practiced`, `demonstrated`, or `extended`.

`demonstrated` means:

1. The learner can explain the core concept without copying definitions.
2. The learner can run the linked notebook or command.
3. The learner can describe assumptions, units, and likely errors.

## Notebook Surface

Open [`notebooks/tracks/scientific_computing/L09/scientific_computing_l09_multiphysics_surrogates_and_data_assimilation.ipynb`](../../../../notebooks/tracks/scientific_computing/L09/scientific_computing_l09_multiphysics_surrogates_and_data_assimilation.ipynb).

## Colab And uv

Use `uv` locally for reproducible execution. Use Colab when local compute or package installation is a barrier, but keep the same scientific narrative and assumptions.
