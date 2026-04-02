from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


sns.set_theme(style="whitegrid")


def plot_sensor_series(df: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(df["timestamp"], df["value"], label="Observed signal", linewidth=1.5)
    ax.plot(df["timestamp"], df["baseline_value"], label="Baseline expectation", linewidth=1.2)
    drift_df = df[df["is_drift"]]
    if not drift_df.empty:
        ax.scatter(
            drift_df["timestamp"],
            drift_df["value"],
            s=10,
            alpha=0.45,
            label="Injected drift region",
        )
    ax.set_title("Sensor signal with baseline and injected drift")
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Signal value")
    ax.legend()
    fig.autofmt_xdate()
    return fig


def plot_drift_scores(df: pd.DataFrame) -> plt.Figure:
    fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True)

    axes[0].plot(df["end_timestamp"], df["distribution_score"], label="Distribution score")
    axes[0].axhline(
        df["distribution_threshold"].iloc[0],
        color="tab:red",
        linestyle="--",
        label="Threshold",
    )
    axes[0].scatter(
        df.loc[df["distribution_alarm"], "end_timestamp"],
        df.loc[df["distribution_alarm"], "distribution_score"],
        color="tab:red",
        s=20,
        label="Persistent alarm",
    )
    axes[0].set_title("Distribution-shift detector")
    axes[0].legend()

    axes[1].plot(df["end_timestamp"], df["ewma_score"], label="EWMA score", color="tab:green")
    axes[1].axhline(
        df["ewma_threshold"].iloc[0],
        color="tab:red",
        linestyle="--",
        label="Threshold",
    )
    axes[1].scatter(
        df.loc[df["ewma_alarm"], "end_timestamp"],
        df.loc[df["ewma_alarm"], "ewma_score"],
        color="tab:red",
        s=20,
        label="Persistent alarm",
    )
    axes[1].set_title("EWMA detector")
    axes[1].legend()
    axes[1].set_xlabel("Window end timestamp")

    fig.autofmt_xdate()
    fig.tight_layout()
    return fig


def plot_method_comparison(metrics_df: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(8, 4))
    melted = metrics_df.melt(
        id_vars="method",
        value_vars=["precision", "recall", "f1"],
        var_name="metric",
        value_name="score",
    )
    sns.barplot(data=melted, x="metric", y="score", hue="method", ax=ax)
    ax.set_ylim(0, 1.05)
    ax.set_title("Method comparison on labeled drift windows")
    return fig


def plot_distribution_diagnostics(df: pd.DataFrame) -> plt.Figure:
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    sns.histplot(
        df.loc[df["is_baseline_window"], "ks_stat"],
        bins=12,
        ax=axes[0],
        color="tab:blue",
    )
    axes[0].set_title("KS statistic in baseline windows")

    sns.histplot(
        df.loc[~df["is_baseline_window"], "wasserstein"],
        bins=12,
        ax=axes[1],
        color="tab:orange",
    )
    axes[1].set_title("Wasserstein distance in monitoring windows")
    fig.tight_layout()
    return fig
