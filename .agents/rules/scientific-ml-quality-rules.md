# Scientific And ML Quality Rules

These rules apply to statistical modeling, ML engineering, scientific computing,
simulation, and analytics conclusions.

## Baselines

Every serious modeling project needs a baseline. A baseline can be:

- Naive forecast.
- Majority class.
- Linear or logistic model.
- Simple physical approximation.
- Historical average.
- Rule-based detector.

## Validation

- Use time-aware splits for forecasting and monitoring.
- Avoid random splits when temporal leakage is possible.
- Use stratification when class balance matters.
- Use cross-validation only when it respects the data-generating process.

## Metrics

Metrics must match the decision problem:

- Classification: precision, recall, F1, ROC-AUC, PR-AUC, calibration.
- Regression: MAE, RMSE, R2, residual diagnostics.
- Forecasting: horizon-specific error and backtesting.
- Anomaly detection: false alarm rate, detection delay, event precision/recall.
- Simulation: analytical comparison, conservation checks, convergence behavior.

## Claims

- Do not make causal claims from purely observational prediction.
- Do not imply production readiness without deployment and monitoring evidence.
- State limitations and failure modes.
- Treat uncertainty as part of the result.
