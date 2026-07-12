# Data Science L05: Supervised Machine Learning

Status: **implemented**

## Start From Zero

This level is for someone who wants to learn from data under uncertainty and build defensible models. You do not need to already know the advanced vocabulary. Start with the plain question:

**What pattern is real, what prediction is useful, and how uncertain are we?**

In simple terms, this level helps you build baselines, train models, and evaluate generalization.

The first principle is: **data science starts with observations, hypotheses, assumptions, and a testable definition of success**.

## Why This Level Exists

A beginner often tries to memorize tools first. That fails because tools only make sense after the learner understands what problem the tool is helping with. In this level, the goal is to build the mental model before using the project as evidence.

For this track, the practical goal is to learn how to frame a question, define a target, estimate patterns, validate them, and explain what remains uncertain.

## Prerequisites

Complete or skim data_science:L04 first, then return here if a word feels unfamiliar.

You should be comfortable with these basic actions before moving on:

- Open a Markdown file and read it slowly.
- Open a notebook and run cells from top to bottom.
- Explain a result in your own words before trusting it.

## The Concept In Plain Language

L05 is the **Baseline** stage. At this stage you learn to build a first complete artifact and compare it against a stronger method.

A useful everyday example: a city observes air quality and weather to estimate where pollution hotspots may appear tomorrow.

At this level, focus on three ideas:

- **Feature-target split**: explain what this means before you try to automate it.
- **Metrics**: identify where it appears in a table, notebook, model, system, or equation.
- **Overfitting**: describe how it can mislead you if you ignore it.

## Step-By-Step Learning Path

1. Read the level title and rewrite it as a question.
2. Identify the object being studied: a row, a file, a model input, a state variable, or a decision.
3. Name the input information and the output you expect.
4. Write one assumption that must be true for the result to be useful.
5. Open the notebook and run the first code cell.
6. Open the project README and find where the same idea appears in real project structure.
7. Write a short reflection: what is clear, what is confusing, and what you would test next.

## Worked Micro-Example

Imagine predicting tomorrow's air quality. You first define the target, then decide which weather features are available before tomorrow, and finally check whether overfitting could leak future information.

Turn that into a small reasoning chain:

1. **Observation**: what is directly visible or recorded?
2. **Representation**: how is it written as a table, file, feature, equation, or function?
3. **Operation**: what calculation, transformation, model, or simulation is applied?
4. **Evidence**: what output would convince you that the operation worked?
5. **Limitation**: what could still be wrong even if the code runs?

## Mathematical Spine, Slowly

\[P(A\mid B) = \frac{P(B\mid A)P(A)}{P(B)}, \qquad \hat{y} = f_\theta(x)\]

Do not treat the formula as decoration. Read it as a compact language for the track:

Bayes' rule updates belief when evidence arrives. A prediction function maps inputs x to an estimated output, but only under assumptions learned from data.

At this level you only need to know what each symbol is trying to represent. Later levels will make the derivations more formal.

## Common Beginner Mistakes

- Starting with a library or model before defining the question.
- Treating a notebook output as true just because the cell ran.
- Ignoring units, time, missing data, sampling, schema, or assumptions.
- Using advanced words without being able to give a simple example.
- Forgetting that every project result has a boundary where it stops applying.

## Guided Practice

Use this checklist with the notebook and project:

- I can say what `p028` / `fraud_detection_in_scientific_grant_data` is trying to teach.
- I can identify the input, output, and one hidden assumption.
- I can explain `Feature-target split` using a small example.
- I can explain `Metrics` using the project files or notebook.
- I can explain why `Overfitting` matters.
- I can write one limitation without weakening the value of the project.

## Mission Anchor

- Project ID: `p028`
- Project slug: `fraud_detection_in_scientific_grant_data`
- Mission ID: `p028-ds-l05-m01`
- Central notebook: [`notebooks/tracks/data_science/L05/data_science_l05_supervised_machine_learning.ipynb`](../../../../../notebooks/tracks/data_science/L05/data_science_l05_supervised_machine_learning.ipynb)
- Project notebook: `projects/fraud_detection_in_scientific_grant_data/notebooks/fraud_detection_in_scientific_grant_data.ipynb`
- Run command:

```bash
PYTHONPATH=src:. uv run python -m projects.fraud_detection_in_scientific_grant_data.src.pipeline
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

The next level is data_science:L06, where this idea becomes more technical.
