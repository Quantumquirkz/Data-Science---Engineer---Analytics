from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import sys

import gradio as gr

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.data import DatasetConfig
from src.inference import load_validation_predictions
from src.pipeline import run_power_grid_load_pipeline
from src.visualization import plot_forecast_intervals, plot_metrics_heatmap, plot_residuals_by_hour


@lru_cache(maxsize=1)
def _load_pipeline():
    return run_power_grid_load_pipeline(
        project_root=PROJECT_ROOT,
        dataset_config=DatasetConfig(),
    )


def run_demo(horizon: int, max_points: int):
    artifacts = _load_pipeline()
    preds = load_validation_predictions(artifacts.predictions_path)
    metrics = artifacts.model_artifacts.metrics.copy()
    cfg = DatasetConfig()
    summary = (
        "### Power grid load forecasting (OPSD + Open-Meteo)\n\n"
        f"- Weather point: `{cfg.latitude}, {cfg.longitude}` (UTC hourly)\n"
        f"- Load column: `{cfg.load_column}`\n"
        f"- Window: `{cfg.start_date}` to `{cfg.end_date}`\n"
        f"- Validation: last `{cfg.validation_months}` month(s)\n"
        f"- Feature rows: `{len(artifacts.features_df)}`\n"
        f"- SARIMAX benchmark fitted: `{artifacts.model_artifacts.sarimax_fitted}`\n"
        f"- Best mean RMSE (direct horizons): `{artifacts.model_artifacts.best_point_model_name}`\n"
    )
    h = int(horizon)
    n = int(max_points)
    fig_fc = plot_forecast_intervals(preds, horizon_h=h, max_points=n)
    fig_res = plot_residuals_by_hour(preds, horizon_h=h)
    fig_rmse = plot_metrics_heatmap(metrics)
    return summary, metrics.round(4), fig_fc, fig_res, fig_rmse


with gr.Blocks(title="Power Grid Load Forecasting") as demo:
    gr.Markdown(
        "# Power grid load forecasting\n\n"
        "Regional load from OPSD, weather from Open-Meteo: baselines, Ridge, HGBR, "
        "LightGBM quantiles, optimized ensemble, SARIMAX fixed-origin benchmark."
    )
    horizon = gr.Dropdown(choices=[24, 168], value=24, label="Forecast horizon (hours)")
    max_points = gr.Slider(100, 2500, value=800, step=50, label="Points in forecast plot")
    run_button = gr.Button("Run portfolio demo", variant="primary")
    summary_output = gr.Markdown()
    metrics_output = gr.Dataframe(label="Validation metrics")
    forecast_plot = gr.Plot(label="Forecasts vs observed")
    residual_plot = gr.Plot(label="Residuals by hour (Berlin local)")
    rmse_plot = gr.Plot(label="RMSE heatmap (direct horizons)")
    run_button.click(
        fn=run_demo,
        inputs=[horizon, max_points],
        outputs=[summary_output, metrics_output, forecast_plot, residual_plot, rmse_plot],
    )

if __name__ == "__main__":
    demo.launch()
