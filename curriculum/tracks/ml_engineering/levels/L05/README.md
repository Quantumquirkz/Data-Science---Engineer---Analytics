# ML Engineering L05: Model Packaging And Serving

Status: **implemented**

## Start From Zero

This level is for someone who wants to turn models into reproducible, testable, monitored software systems. You do not need to already know the advanced vocabulary. Start with the plain question:

**How does a model become a reliable, reproducible, inspectable software system?**

In simple terms, this level helps you turn models into callable systems with stable inference contracts.

The first principle is: **ML engineering starts when a model becomes part of a system that other people or processes depend on**.

## Why This Level Exists

A beginner often tries to memorize tools first. That fails because tools only make sense after the learner understands what problem the tool is helping with. In this level, the goal is to build the mental model before using the project as evidence.

For this track, the practical goal is to learn how training code, model artifacts, inference contracts, testing, deployment, and monitoring fit together.

## Prerequisites

Complete or skim ml_engineering:L04 first, then return here if a word feels unfamiliar.

You should be comfortable with these basic actions before moving on:

- Open a Markdown file and read it slowly.
- Open a notebook and run cells from top to bottom.
- Explain a result in your own words before trusting it.

## The Concept In Plain Language

L05 is the **Baseline** stage. At this stage you learn to build a first complete artifact and compare it against a stronger method.

A useful everyday example: a sensor-drift detector must not only score data, it must run repeatedly, expose inputs clearly, and warn when behavior changes.

At this level, focus on three ideas:

- **Input schemas**: explain what this means before you try to automate it.
- **Prediction interfaces**: identify where it appears in a table, notebook, model, system, or equation.
- **Cold-start costs**: describe how it can mislead you if you ignore it.

## Step-By-Step Learning Path

1. Read the level title and rewrite it as a question.
2. Identify the object being studied: a row, a file, a model input, a state variable, or a decision.
3. Name the input information and the output you expect.
4. Write one assumption that must be true for the result to be useful.
5. Open the notebook and run the first code cell.
6. Open the project README and find where the same idea appears in real project structure.
7. Write a short reflection: what is clear, what is confusing, and what you would test next.

## Worked Micro-Example

Imagine a trained model inside an app. You need to know where the package boundary is, how to call it, and how cold-start costs affects repeated runs.

Turn that into a small reasoning chain:

1. **Observation**: what is directly visible or recorded?
2. **Representation**: how is it written as a table, file, feature, equation, or function?
3. **Operation**: what calculation, transformation, model, or simulation is applied?
4. **Evidence**: what output would convince you that the operation worked?
5. **Limitation**: what could still be wrong even if the code runs?

## Mathematical Spine, Slowly

\[\mathcal{L}(\theta) = \frac{1}{n}\sum_{i=1}^n \ell(f_\theta(x_i), y_i), \qquad \text{SLO}=\{\text{latency},\text{availability},\text{quality}\}\]

Do not treat the formula as decoration. Read it as a compact language for the track:

The loss summarizes model error during training. Service objectives describe the operational promises the system must keep after training.

At this level you only need to know what each symbol is trying to represent. Later levels will make the derivations more formal.

## Common Beginner Mistakes

- Starting with a library or model before defining the question.
- Treating a notebook output as true just because the cell ran.
- Ignoring units, time, missing data, sampling, schema, or assumptions.
- Using advanced words without being able to give a simple example.
- Forgetting that every project result has a boundary where it stops applying.

## Guided Practice

Use this checklist with the notebook and project:

- I can say what `p059` / `physics_informed_weather_nowcasting` is trying to teach.
- I can identify the input, output, and one hidden assumption.
- I can explain `Input schemas` using a small example.
- I can explain `Prediction interfaces` using the project files or notebook.
- I can explain why `Cold-start costs` matters.
- I can write one limitation without weakening the value of the project.

## Mission Anchor

- Project ID: `p059`
- Project slug: `physics_informed_weather_nowcasting`
- Mission ID: `p059-mle-l05-m01`
- Central notebook: [`notebooks/tracks/ml_engineering/L05/ml_engineering_l05_model_packaging_and_serving.ipynb`](../../../../../notebooks/tracks/ml_engineering/L05/ml_engineering_l05_model_packaging_and_serving.ipynb)
- Project notebook: `projects/physics_informed_weather_nowcasting/notebooks/physics_informed_weather_nowcasting.ipynb`
- Run command:

```bash
PYTHONPATH=src:. uv run python -m projects.physics_informed_weather_nowcasting.src.pipeline
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

The next level is ml_engineering:L06, where this idea becomes more technical.
