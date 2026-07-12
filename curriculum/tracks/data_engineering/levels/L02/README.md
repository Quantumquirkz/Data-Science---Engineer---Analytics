# Data Engineering L02: Linux, Python, And Data Formats

Status: **implemented**

## Start From Zero

This level is for someone who wants to move, validate, transform, and serve data reliably. You do not need to already know the advanced vocabulary. Start with the plain question:

**How does data move, stay valid, and remain trustworthy at scale?**

In simple terms, this level helps you inspect CSV, JSON, Parquet, and logs with tooling discipline.

The first principle is: **data engineering starts with movement, structure, contracts, and failure recovery**.

## Why This Level Exists

A beginner often tries to memorize tools first. That fails because tools only make sense after the learner understands what problem the tool is helping with. In this level, the goal is to build the mental model before using the project as evidence.

For this track, the practical goal is to learn how data travels through files, tables, schemas, jobs, storage systems, and quality checks.

## Prerequisites

Complete or skim data_engineering:L01 first, then return here if a word feels unfamiliar.

You should be comfortable with these basic actions before moving on:

- Open a Markdown file and read it slowly.
- Open a notebook and run cells from top to bottom.
- Explain a result in your own words before trusting it.

## The Concept In Plain Language

L02 is the **Basic Tooling** stage. At this stage you learn to translate the vocabulary into simple files, tables, arrays, or modules.

A useful everyday example: a logistics team collects scanner events, cleans them, joins them to routes, and publishes reliable delivery tables every morning.

At this level, focus on three ideas:

- **Serialization formats**: explain what this means before you try to automate it.
- **Compression**: identify where it appears in a table, notebook, model, system, or equation.
- **Schema drift**: describe how it can mislead you if you ignore it.

## Step-By-Step Learning Path

1. Read the level title and rewrite it as a question.
2. Identify the object being studied: a row, a file, a model input, a state variable, or a decision.
3. Name the input information and the output you expect.
4. Write one assumption that must be true for the result to be useful.
5. Open the notebook and run the first code cell.
6. Open the project README and find where the same idea appears in real project structure.
7. Write a short reflection: what is clear, what is confusing, and what you would test next.

## Worked Micro-Example

Imagine a folder of daily log files. You need to know where each file comes from, what schema it claims to follow, and how schema drift would appear when something breaks.

Turn that into a small reasoning chain:

1. **Observation**: what is directly visible or recorded?
2. **Representation**: how is it written as a table, file, feature, equation, or function?
3. **Operation**: what calculation, transformation, model, or simulation is applied?
4. **Evidence**: what output would convince you that the operation worked?
5. **Limitation**: what could still be wrong even if the code runs?

## Mathematical Spine, Slowly

\[\text{throughput} = \frac{\text{records processed}}{\text{time}}, \qquad \text{latency} = t_{out} - t_{in}\]

Do not treat the formula as decoration. Read it as a compact language for the track:

Throughput measures how much work a system completes per unit time. Latency measures how long one item takes to travel through the system.

At this level you only need to know what each symbol is trying to represent. Later levels will make the derivations more formal.

## Common Beginner Mistakes

- Starting with a library or model before defining the question.
- Treating a notebook output as true just because the cell ran.
- Ignoring units, time, missing data, sampling, schema, or assumptions.
- Using advanced words without being able to give a simple example.
- Forgetting that every project result has a boundary where it stops applying.

## Guided Practice

Use this checklist with the notebook and project:

- I can say what `p040` / `large_scale_log_compression_and_analytics` is trying to teach.
- I can identify the input, output, and one hidden assumption.
- I can explain `Serialization formats` using a small example.
- I can explain `Compression` using the project files or notebook.
- I can explain why `Schema drift` matters.
- I can write one limitation without weakening the value of the project.

## Mission Anchor

- Project ID: `p040`
- Project slug: `large_scale_log_compression_and_analytics`
- Mission ID: `p040-de-l02-m01`
- Central notebook: [`notebooks/tracks/data_engineering/L02/data_engineering_l02_linux_python_and_data_formats.ipynb`](../../../../../notebooks/tracks/data_engineering/L02/data_engineering_l02_linux_python_and_data_formats.ipynb)
- Project notebook: `projects/large_scale_log_compression_and_analytics/notebooks/large_scale_log_compression_and_analytics.ipynb`
- Run command:

```bash
PYTHONPATH=src:. uv run python -m projects.large_scale_log_compression_and_analytics.src.pipeline
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

The next level is data_engineering:L03, where this idea becomes more technical.
