# ML Engineering L06: Experiment Tracking And Registry

Status: **implemented**

## Role Question

How does a model become a reliable, reproducible, inspectable software system?

## Level Intent

Version runs, metrics, and models without losing comparability.

This level is part of a **self-paced, no-grade learning system**. The learner decides the pace. Evidence matters more than completion counters.

## Theory Spine

\[
\mathcal{L}(\theta) = \frac{1}{n}\sum_{i=1}^n \ell\left(f_\theta(x_i), y_i\right), \qquad \text{SLO} = \{\text{latency}, \text{availability}, \text{quality}\}
\]

Interpret the equation as a compact statement of what the level treats as signal, state, or evidence.

## Lesson Focus

- Run lineage
- Model registry semantics
- Promotion criteria

## What To Practice

- Read the linked notebook or project README and restate the problem in your own words.
- Identify what can be measured directly and what must be estimated.
- Explain one assumption that, if false, would change the conclusion.

## Mission Anchor

- Project ID: `p068`
- Mission ID: `p068-mle-l06-m01`
- Delivery surface: `README + notebook + project execution command`

## Evidence Without Grades

A learner can mark this level as `exploring`, `practiced`, `demonstrated`, or `extended`.

`demonstrated` means:

1. The learner can explain the core concept without copying definitions.
2. The learner can run the linked notebook or command.
3. The learner can describe assumptions, units, and likely errors.

## Notebook Surface

Open [`notebooks/tracks/ml_engineering/L06/ml_engineering_l06_experiment_tracking_and_registry.ipynb`](../../../../notebooks/tracks/ml_engineering/L06/ml_engineering_l06_experiment_tracking_and_registry.ipynb).

## Colab And uv

Use `uv` locally for reproducible execution. Use Colab when local compute or package installation is a barrier, but keep the same scientific narrative and assumptions.
