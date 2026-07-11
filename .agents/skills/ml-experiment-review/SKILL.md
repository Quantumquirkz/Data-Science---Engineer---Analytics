---
name: ml-experiment-review
description: Review ML, statistics, forecasting, anomaly detection, or simulation experiments for leakage, baselines, metrics, validation, uncertainty, and scientific validity.
---

# ML Experiment Review

Use this skill when evaluating a model, notebook, experiment, metric, or
scientific claim.

## Required Context

Read:

- `.agents/agents/ml-research-scientist.md`
- `.agents/rules/scientific-ml-quality-rules.md`
- The relevant project `README.md`.
- The relevant notebook or `src/` modules.

## Review Workflow

1. **Identify the claim**
   - Predictive, explanatory, causal, simulation, detection, or descriptive.
   - State what evidence would be required for that claim.

2. **Audit data split**
   - Check train/test separation.
   - Check time ordering for temporal data.
   - Check group leakage for repeated entities.
   - Check target leakage from engineered features.

3. **Audit baseline**
   - Confirm an appropriate baseline exists.
   - If absent, propose the simplest credible baseline.

4. **Audit metrics**
   - Match metrics to the problem type.
   - Flag misleading metrics under imbalance, skew, seasonality, or censoring.

5. **Audit uncertainty and diagnostics**
   - Residuals for regression.
   - Calibration for probabilistic classification.
   - Detection delay and false alarm rate for anomaly detection.
   - Convergence or conservation checks for simulations.

6. **Audit reproducibility**
   - Random seeds.
   - Dependency path.
   - Data availability.
   - Re-runnable pipeline function.

## Output Format

```markdown
## Verdict
<Trust level: strong / moderate / weak / invalid, with one sentence why.>

## Findings
1. [Severity] <Finding>
   Evidence:
   Impact:
   Fix:

## Experiment Matrix
| Component | Current state | Required improvement |
|---|---|---|
| Baseline | | |
| Split | | |
| Metrics | | |
| Diagnostics | | |

## Recommended Next Experiments
1.
2.
3.

## Claims That Are Supported
- 

## Claims That Are Not Yet Supported
- 
```

## Exit Criteria

The review is complete only when it addresses leakage, baselines, metrics,
validation, reproducibility, and claim strength.
