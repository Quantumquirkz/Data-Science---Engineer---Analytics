# Sensor Drift Detection in Industrial Systems

This lab builds a reproducible portfolio project for detecting long-term drift in
industrial sensor streams. The implementation uses synthetic telemetry with
ground-truth drift labels so the full pipeline can be evaluated end to end.

## What the project does

- Simulates temperature, pressure, or vibration signals with realistic noise
- Injects gradual drift, abrupt calibration shifts, and sparse outliers
- Builds rolling-window features against a historical baseline
- Compares two detector families:
  - distribution shift with `KS + Wasserstein`
  - statistical process control with `EWMA`
- Scores alerts with persistence rules to reduce false alarms
- Produces evaluation metrics and portfolio-friendly visualizations

## Project structure

- `src/data.py` - synthetic sensor generation and drift injection
- `src/features.py` - rolling-window feature engineering
- `src/drift_detection.py` - distribution-shift and EWMA detectors
- `src/evaluation.py` - precision, recall, F1, false alarm rate, detection delay
- `src/visualization.py` - charts for signal, alarms, and method comparison
- `src/pipeline.py` - orchestration helper for the full workflow
- `app.py` - Gradio demo for interactive exploration
- `notebooks/` - notebook walkthrough for the full lab
- `data/` - optional outputs or exported sample datasets

## Methodology

The workflow is designed to separate normal operational noise from persistent
sensor drift:

1. Simulate a baseline regime with low-frequency seasonality and noise.
2. Inject gradual drift and abrupt offset changes after the baseline period.
3. Aggregate the signal into rolling windows.
4. Compare monitoring windows against baseline windows using:
   - `KS statistic` for shape changes
   - `Wasserstein distance` for magnitude shifts
   - `EWMA` on rolling means for interpretable SPC monitoring
5. Trigger drift alarms only after repeated consecutive windows exceed the
   threshold.

## Key features

Each rolling window includes:

- `mean`, `median`, `std`, `variance`, `range`
- `p10`, `p25`, `p75`, `p90`, `IQR`
- `skewness`, `kurtosis`
- local `slope`
- `lag-1 autocorrelation`
- `RMS`, `energy`, and average absolute change

## Evaluation

The lab labels windows using injected drift episodes and reports:

- precision
- recall
- F1
- false alarm rate
- detection delay in windows

## How to run

From the repository root:

```bash
uv run python labs/sensor_drift_detection/app.py
```

For a quick non-UI sanity check:

```bash
uv run python -c "from labs.sensor_drift_detection.src.pipeline import run_sensor_drift_pipeline; raw_df, windows_df, metrics_df, metadata = run_sensor_drift_pipeline(); print(metrics_df.round(3).to_string(index=False))"
```

Open the notebook in JupyterLab if you want a guided walkthrough:

```bash
uv run jupyter lab
```

Then open `labs/sensor_drift_detection/notebooks/sensor_drift_detection.ipynb`.

## Suggested extensions

- multivariate drift across correlated sensors
- live streaming ingestion instead of batch windows
- threshold tuning by operating regime
- residual-based drift detection with predictive models
- online recalibration and adaptive baselines
