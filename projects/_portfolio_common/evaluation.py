from __future__ import annotations

import pandas as pd


def summarize_metrics(metrics: pd.DataFrame) -> str:
    best = metrics.sort_values("value", ascending=False).head(1).iloc[0]
    return f"{best['model']} / {best['metric']}: {best['value']:.3f}"
