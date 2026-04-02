from __future__ import annotations

from pathlib import Path
import sys

import gradio as gr

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.data import SimulationConfig
from src.pipeline import run_sensor_drift_pipeline
from src.visualization import (
    plot_distribution_diagnostics,
    plot_drift_scores,
    plot_method_comparison,
    plot_sensor_series,
)
def run_demo(
    sensor_type: str,
    n_points: int,
    baseline_fraction: float,
    gradual_drift_magnitude: float,
    abrupt_drift_magnitude: float,
    noise_scale: float,
    random_seed: int,
):
    simulation_config = SimulationConfig(
        n_points=int(n_points),
        baseline_fraction=float(baseline_fraction),
        gradual_drift_magnitude=float(gradual_drift_magnitude),
        abrupt_drift_magnitude=float(abrupt_drift_magnitude),
        noise_scale=float(noise_scale),
        random_seed=int(random_seed),
    )
    raw_df, windows_df, metrics_df, metadata = run_sensor_drift_pipeline(
        sensor_type=sensor_type,
        simulation_config=simulation_config,
    )

    best_method = metrics_df.sort_values("f1", ascending=False).iloc[0]
    summary = f"""
### Sensor drift summary

- Sensor type: `{metadata["sensor_type"]}`
- Samples: `{metadata["n_points"]}`
- Baseline fraction: `{metadata["baseline_fraction"]:.2f}`
- Best method by F1: `{best_method["method"]}`
- Precision: `{best_method["precision"]:.3f}`
- Recall: `{best_method["recall"]:.3f}`
- F1: `{best_method["f1"]:.3f}`
- False alarm rate: `{best_method["false_alarm_rate"]:.3f}`
- Detection delay (windows): `{best_method["detection_delay_windows"]}`
"""
    metrics_table = metrics_df.round(3)
    return (
        summary,
        metrics_table,
        plot_sensor_series(raw_df),
        plot_drift_scores(windows_df),
        plot_method_comparison(metrics_df),
        plot_distribution_diagnostics(windows_df),
    )


with gr.Blocks(title="Sensor Drift Detection Demo") as demo:
    gr.Markdown(
        """
# Sensor Drift Detection in Industrial Systems

Generate a synthetic sensor stream, compare a distribution-shift detector
against an EWMA control-chart baseline, and inspect alerts over time.
"""
    )

    with gr.Row():
        sensor_type = gr.Dropdown(
            choices=["temperature", "pressure", "vibration"],
            value="temperature",
            label="Sensor type",
        )
        n_points = gr.Slider(1200, 4000, value=2400, step=200, label="Number of points")
        baseline_fraction = gr.Slider(
            0.2,
            0.5,
            value=0.35,
            step=0.05,
            label="Baseline fraction",
        )

    with gr.Row():
        gradual_drift_magnitude = gr.Slider(
            0.5,
            4.5,
            value=2.6,
            step=0.1,
            label="Gradual drift magnitude",
        )
        abrupt_drift_magnitude = gr.Slider(
            0.5,
            4.5,
            value=1.8,
            step=0.1,
            label="Abrupt drift magnitude",
        )
        noise_scale = gr.Slider(0.1, 1.2, value=0.35, step=0.05, label="Noise scale")
        random_seed = gr.Number(value=42, precision=0, label="Random seed")

    run_button = gr.Button("Run drift analysis", variant="primary")
    summary_output = gr.Markdown()
    metrics_output = gr.Dataframe(label="Method metrics")
    series_plot = gr.Plot(label="Raw signal and baseline")
    score_plot = gr.Plot(label="Drift scores")
    comparison_plot = gr.Plot(label="Method comparison")
    diagnostics_plot = gr.Plot(label="Distribution diagnostics")

    run_button.click(
        fn=run_demo,
        inputs=[
            sensor_type,
            n_points,
            baseline_fraction,
            gradual_drift_magnitude,
            abrupt_drift_magnitude,
            noise_scale,
            random_seed,
        ],
        outputs=[
            summary_output,
            metrics_output,
            series_plot,
            score_plot,
            comparison_plot,
            diagnostics_plot,
        ],
    )


if __name__ == "__main__":
    demo.launch()
