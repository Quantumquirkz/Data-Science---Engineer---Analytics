# Earthquake Signal Classification

This lab turns a geophysical signal-processing idea into a reproducible
portfolio project. It classifies waveform segments into:

- `noise`
- `microseisms`
- `earthquakes`

The implementation emphasizes interpretability, probabilistic outputs, and a
clean separation between data creation, preprocessing, features, modeling,
evaluation, and demo delivery.

## Why this project exists

A small, self-contained public benchmark with exactly these three labels is not
easy to package locally. Because of that, the lab uses a **curated reproducible
subset strategy**:

- `INSTANCE` motivates the `earthquakes` and `noise` taxonomy.
- The Zenodo ambient-noise classification scheme motivates the
  `microseisms` proxy through `surface-wave dominated` windows.
- `STEAD` is documented as a natural external validation extension.

The shipped dataset is a deterministic, geophysics-inspired benchmark subset
generated from those label definitions so the full project can run end to end in
this repository without a fragile multi-gigabyte download.

## Project structure

- `src/data.py` - deterministic portfolio dataset generation and provenance
- `src/preprocessing.py` - detrending, tapering, band-pass filtering, normalization
- `src/features.py` - temporal, spectral, and wavelet-style multiscale features
- `src/modeling.py` - logistic-regression baseline and calibrated random forest
- `src/evaluation.py` - multiclass metrics, confusion matrix, confidence analysis
- `src/visualization.py` - waveform, spectral, confusion, and feature plots
- `src/pipeline.py` - orchestration, persistence, and single-waveform inference
- `src/inference.py` - CSV loading helper for demo-time scoring
- `app.py` - Gradio demo
- `notebooks/` - guided walkthrough notebook
- `data/processed/` - generated subset, metrics, predictions, and trained model

## Methodology

### Preprocessing

Each waveform is:

1. detrended;
2. tapered with a Tukey window;
3. band-pass filtered in a seismic range;
4. standardized to stabilize downstream features.

### Feature engineering

The feature set is organized around the requested analytical stack:

- **Temporal**: RMS, energy, zero-crossing rate, crest factor, quantiles,
  kurtosis, skewness, effective duration, activity density.
- **Frequency**: Welch PSD, dominant frequency, spectral centroid, bandwidth,
  entropy, flatness, and power by seismic bands.
- **Time-frequency / wavelets**: multilevel Haar-style wavelet energies,
  approximation energy, and wavelet entropy.

### Models

Two supervised probabilistic classifiers are trained:

- **Baseline**: multinomial `LogisticRegression`
- **Main model**: `CalibratedClassifierCV(RandomForestClassifier)`

This gives a direct comparison between an interpretable linear baseline and a
stronger nonlinear model with calibrated probabilities.

## Evaluation

The project reports:

- accuracy
- macro F1
- weighted F1
- per-class precision / recall / F1
- confusion matrix
- log loss
- multiclass Brier score
- confidence concentration and low-confidence share

The most important failure mode to inspect is confusion between
`microseisms` and `noise`, since weak low-frequency activity can resemble
ambient background.

## How to run

From the repository root:

```bash
uv run python -c "from pathlib import Path; from projects.seismic_signal_classification.src.pipeline import run_seismic_classification_pipeline; artifacts = run_seismic_classification_pipeline(Path('projects/seismic_signal_classification')); print(artifacts.model_artifacts.summary_table.round(3).to_string(index=False))"
```

To launch the demo:

```bash
uv run python projects/seismic_signal_classification/app.py
```

To explore the notebook:

```bash
uv run jupyter lab
```

Then open `projects/seismic_signal_classification/notebooks/seismic_signal_classification.ipynb`.

## Dataset notes

The generated subset is deterministic and saved locally the first time the
pipeline runs. Provenance links are stored in
`data/processed/dataset_provenance.csv`.

This keeps the lab reproducible while still documenting the real public sources
that motivated the taxonomy:

- [INSTANCE](https://doi.org/10.13127/instance)
- [Ambient noise classification scheme](https://zenodo.org/records/7494745)
- [STEAD](https://doi.org/10.1109/ACCESS.2019.2947848)

## Suggested extensions

- multistation or multisite generalization with group-aware validation
- streaming early-warning classification on rolling windows
- sequential models over longer coda structure
- integration with geophysical dashboards and station metadata
- stronger probabilistic calibration and conformal prediction
