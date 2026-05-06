from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import sys

import gradio as gr

PROJECT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PROJECT_ROOT.parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

from projects.fraud_detection_in_scientific_grant_data.src.config import SPEC
from projects.fraud_detection_in_scientific_grant_data.src.pipeline import run_fraud_detection_in_scientific_grant_data_pipeline


@lru_cache(maxsize=1)
def _load_pipeline(n_samples: int):
    return run_fraud_detection_in_scientific_grant_data_pipeline(PROJECT_ROOT, n_samples=int(n_samples))


def run_demo(n_samples: int):
    artifacts = _load_pipeline(int(n_samples))
    metrics = artifacts.model_result.metrics.copy()
    summary = (
        f"### {SPEC.title}\n\n"
        f"- Domain: `{SPEC.domain}`\n"
        f"- Task: `{SPEC.task_kind}`\n"
        f"- Rows: `{artifacts.dataset_summary['rows']}`\n"
        f"- Target: `{SPEC.target_name}`\n"
        f"- Data policy: {SPEC.public_data_note}\n"
    )
    figures = artifacts.figure_paths
    return (
        summary,
        metrics.round(4),
        str(figures["domain_signals"]),
        str(figures["feature_projection"]),
        str(figures["validation_predictions"]),
    )


with gr.Blocks(title=SPEC.title) as demo:
    gr.Markdown(f"# {SPEC.title}\n\n{SPEC.description}")
    n_samples = gr.Slider(240, 1800, value=720, step=120, label="Synthetic/domain sample size")
    run_button = gr.Button("Run portfolio demo", variant="primary")
    summary_output = gr.Markdown()
    metrics_output = gr.Dataframe(label="Validation metrics")
    signal_plot = gr.Image(label="Domain signals", type="filepath")
    projection_plot = gr.Image(label="Feature projection", type="filepath")
    prediction_plot = gr.Image(label="Validation predictions", type="filepath")
    run_button.click(
        fn=run_demo,
        inputs=[n_samples],
        outputs=[summary_output, metrics_output, signal_plot, projection_plot, prediction_plot],
    )


if __name__ == "__main__":
    demo.launch()
