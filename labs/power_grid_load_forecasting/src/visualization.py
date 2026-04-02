from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose


def plot_forecast_intervals(
    predictions_df: pd.DataFrame,
    horizon_h: int,
    max_points: int = 800,
) -> plt.Figure:
    """Observed load vs median forecast and 80% interval for one horizon."""
    sub = predictions_df.loc[predictions_df["horizon_h"] == horizon_h].copy()
    sub["timestamp"] = pd.to_datetime(sub["timestamp"], utc=True)
    sub = sub.sort_values("timestamp")
    if len(sub) > max_points:
        sub = sub.iloc[-max_points:]

    fig, ax = plt.subplots(figsize=(11, 4))
    ax.fill_between(
        sub["timestamp"],
        sub["lgb_q10"],
        sub["lgb_q90"],
        alpha=0.25,
        label="LightGBM 10-90%",
    )
    ax.plot(sub["timestamp"], sub["y_true"], color="black", linewidth=1.0, label="Observed load")
    ax.plot(sub["timestamp"], sub["lgb_q50"], color="tab:orange", linewidth=1.0, label="LightGBM median")
    ax.plot(sub["timestamp"], sub["ensemble_opt"], color="tab:red", linewidth=0.9, alpha=0.85, label="Ensemble")
    ax.plot(
        sub["timestamp"],
        sub["naive_calendar"],
        color="tab:green",
        alpha=0.55,
        linewidth=0.8,
        label="Naive baseline",
    )
    ax.set_ylabel("Load (MW)")
    ax.set_title(f"Validation forecasts — {horizon_h} h horizon")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    return fig


def plot_residuals_by_hour(
    predictions_df: pd.DataFrame,
    horizon_h: int,
) -> plt.Figure:
    """Median model residuals by hour of day (Europe/Berlin)."""
    sub = predictions_df.loc[predictions_df["horizon_h"] == horizon_h].copy()
    sub["timestamp"] = pd.to_datetime(sub["timestamp"], utc=True)
    sub["hour"] = sub["timestamp"].dt.tz_convert("Europe/Berlin").dt.hour
    sub["residual"] = sub["lgb_q50"] - sub["y_true"]

    hourly = sub.groupby("hour")["residual"].median()
    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.bar(hourly.index.astype(int), hourly.values, color="steelblue", alpha=0.85)
    ax.axhline(0.0, color="black", linewidth=0.8)
    ax.set_xlabel("Hour (Europe/Berlin)")
    ax.set_ylabel("Median residual (pred - true)")
    ax.set_title(f"Residuals by hour — {horizon_h} h horizon (LightGBM median)")
    ax.set_xticks(range(0, 24, 2))
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    return fig


def plot_metrics_heatmap(metrics_df: pd.DataFrame) -> plt.Figure:
    """RMSE by model and horizon (excludes horizon 0 rows)."""
    sub = metrics_df.loc[metrics_df["horizon_h"] > 0].copy()
    pivot = sub.pivot_table(index="model", columns="horizon_h", values="rmse", aggfunc="first")
    fig, ax = plt.subplots(figsize=(7, 4.5))
    im = ax.imshow(pivot.to_numpy(dtype=float), aspect="auto", cmap="viridis")
    ax.set_xticks(range(pivot.shape[1]))
    ax.set_xticklabels([str(c) for c in pivot.columns])
    ax.set_yticks(range(pivot.shape[0]))
    ax.set_yticklabels(list(pivot.index))
    ax.set_xlabel("Horizon (h)")
    ax.set_ylabel("Model")
    ax.set_title("RMSE (MW) on validation — direct horizons")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    return fig


def plot_stl_decomposition(
    load_series: pd.Series,
    seasonal_period: int = 24,
) -> plt.Figure:
    """Additive seasonal decomposition for EDA (train-only series recommended)."""
    y = load_series.astype(float).asfreq("h")
    res = seasonal_decompose(y, model="additive", period=seasonal_period, extrapolate_trend="freq")
    fig, axes = plt.subplots(4, 1, figsize=(11, 8), sharex=True)
    res.observed.plot(ax=axes[0], title="Observed", legend=False, color="black")
    res.trend.plot(ax=axes[1], title="Trend", legend=False, color="tab:blue")
    res.seasonal.plot(ax=axes[2], title="Seasonal", legend=False, color="tab:green")
    res.resid.plot(ax=axes[3], title="Residual", legend=False, color="tab:red")
    for ax in axes:
        ax.grid(True, alpha=0.3)
    axes[0].set_ylabel("MW")
    fig.suptitle("Seasonal decomposition (hourly load)")
    fig.tight_layout()
    return fig
