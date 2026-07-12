# Scientific Computing L04: Differential Equations And Numerical Error

Status: **implemented**

## Start From Zero

This level is for someone who wants to use computation to reason about physical, biological, mathematical, or engineered systems. You do not need to already know the advanced vocabulary. Start with the plain question:

**How do equations, numerical methods, and simulations become trustworthy computational evidence?**

In simple terms, this level helps you solve evolving systems while tracking discretization error.

The first principle is: **scientific computing starts with state variables, units, laws or assumptions, and numerical error**.

## Why This Level Exists

A beginner often tries to memorize tools first. That fails because tools only make sense after the learner understands what problem the tool is helping with. In this level, the goal is to build the mental model before using the project as evidence.

For this track, the practical goal is to learn how quantities, equations, numerical approximations, simulation, uncertainty, and validation become computational evidence.

## Prerequisites

Complete or skim scientific_computing:L03 first, then return here if a word feels unfamiliar.

You should be comfortable with these basic actions before moving on:

- Open a Markdown file and read it slowly.
- Open a notebook and run cells from top to bottom.
- Explain a result in your own words before trusting it.

## The Concept In Plain Language

L04 is the **Assumptions** stage. At this stage you learn to make hidden assumptions visible and test whether they matter.

A useful everyday example: an orbit simulator updates position and velocity step by step, then checks whether the simulated motion still respects expected physics.

At this level, focus on three ideas:

- **Euler stepping**: explain what this means before you try to automate it.
- **Stability**: identify where it appears in a table, notebook, model, system, or equation.
- **Convergence**: describe how it can mislead you if you ignore it.

## Step-By-Step Learning Path

1. Read the level title and rewrite it as a question.
2. Identify the object being studied: a row, a file, a model input, a state variable, or a decision.
3. Name the input information and the output you expect.
4. Write one assumption that must be true for the result to be useful.
5. Open the notebook and run the first code cell.
6. Open the project README and find where the same idea appears in real project structure.
7. Write a short reflection: what is clear, what is confusing, and what you would test next.

## Worked Micro-Example

Imagine simulating a moving object. You name the state variables, attach units, and ask how convergence changes the trustworthiness of the computed trajectory.

Turn that into a small reasoning chain:

1. **Observation**: what is directly visible or recorded?
2. **Representation**: how is it written as a table, file, feature, equation, or function?
3. **Operation**: what calculation, transformation, model, or simulation is applied?
4. **Evidence**: what output would convince you that the operation worked?
5. **Limitation**: what could still be wrong even if the code runs?

## Mathematical Spine, Slowly

\[\frac{d\mathbf{x}}{dt} = f(\mathbf{x}, t), \qquad \epsilon_h = \lVert x - x_h \rVert\]

Do not treat the formula as decoration. Read it as a compact language for the track:

A differential equation describes how a state changes over time. Numerical error measures the gap between the ideal solution and the computed approximation.

At this level you only need to know what each symbol is trying to represent. Later levels will make the derivations more formal.

## Common Beginner Mistakes

- Starting with a library or model before defining the question.
- Treating a notebook output as true just because the cell ran.
- Ignoring units, time, missing data, sampling, schema, or assumptions.
- Using advanced words without being able to give a simple example.
- Forgetting that every project result has a boundary where it stops applying.

## Guided Practice

Use this checklist with the notebook and project:

- I can say what `p027` / `fluid_flow_surrogate_model` is trying to teach.
- I can identify the input, output, and one hidden assumption.
- I can explain `Euler stepping` using a small example.
- I can explain `Stability` using the project files or notebook.
- I can explain why `Convergence` matters.
- I can write one limitation without weakening the value of the project.

## Mission Anchor

- Project ID: `p027`
- Project slug: `fluid_flow_surrogate_model`
- Mission ID: `p027-sc-l04-m01`
- Central notebook: [`notebooks/tracks/scientific_computing/L04/scientific_computing_l04_differential_equations_and_numerical_error.ipynb`](../../../../../notebooks/tracks/scientific_computing/L04/scientific_computing_l04_differential_equations_and_numerical_error.ipynb)
- Project notebook: `projects/fluid_flow_surrogate_model/notebooks/fluid_flow_surrogate_model.ipynb`
- Run command:

```bash
PYTHONPATH=src:. uv run python -m projects.fluid_flow_surrogate_model.src.pipeline
```

## Evidence Without Grades

This repository does not grade you. Use evidence states instead:

- `exploring`: I can follow the words, but I still need help.
- `practiced`: I ran the notebook and answered the prompts.
- `demonstrated`: I can explain the level to someone else using the project.
- `extended`: I changed an assumption, tried a variant, or connected the idea to another project.

A strong `demonstrated` answer has four parts: a plain-language explanation, a small example, one project reference, and one limitation.

## Before You Move On

You are ready to continue when you can answer these questions without copying text:

1. What is the main question of this level?
2. What does the project use as evidence?
3. What assumption could break the conclusion?
4. What would you inspect first if the result looked suspicious?

The next level is scientific_computing:L05, where this idea becomes more technical.
