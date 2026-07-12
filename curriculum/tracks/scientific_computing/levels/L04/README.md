# Scientific Computing L04: Differential Equations And Numerical Error

Status: **implemented**

## Role Question

How do equations, numerical methods, and simulations become trustworthy computational evidence?

## Level Intent

Solve evolving systems while tracking discretization error.

This level is part of a **self-paced, no-grade learning system**. The learner decides the pace. Evidence matters more than completion counters.

## Theory Spine

\[
\frac{d\mathbf{x}}{dt} = f(\mathbf{x}, t), \qquad \epsilon_h = \lVert x - x_h \rVert
\]

Interpret the equation as a compact statement of what the level treats as signal, state, or evidence.

## Lesson Focus

- Euler stepping
- Stability
- Convergence

## What To Practice

- Read the linked notebook or project README and restate the problem in your own words.
- Identify what can be measured directly and what must be estimated.
- Explain one assumption that, if false, would change the conclusion.

## Mission Anchor

- Project ID: `p027`
- Mission ID: `p027-sc-l04-m01`
- Delivery surface: `README + notebook + project execution command`

## Evidence Without Grades

A learner can mark this level as `exploring`, `practiced`, `demonstrated`, or `extended`.

`demonstrated` means:

1. The learner can explain the core concept without copying definitions.
2. The learner can run the linked notebook or command.
3. The learner can describe assumptions, units, and likely errors.

## Notebook Surface

Open [`notebooks/tracks/scientific_computing/L04/scientific_computing_l04_differential_equations_and_numerical_error.ipynb`](../../../../notebooks/tracks/scientific_computing/L04/scientific_computing_l04_differential_equations_and_numerical_error.ipynb).

## Colab And uv

Use `uv` locally for reproducible execution. Use Colab when local compute or package installation is a barrier, but keep the same scientific narrative and assumptions.
