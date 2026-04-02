from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import sys

import gradio as gr
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.data import DatasetConfig
from src.inference import predict_csv_waveform
from src.pipeline import run_seismic_classification_pipeline
from src.visualization import (
    plot_average_spectra,
    plot_confusion_matrix,
    plot_example_waveforms,
    plot_feature_importance,
    plot_prediction_confidence,
    plot_scalogram_example,
)


@lru_cache(maxsize=1)
def _load_pipeline():
    return run_seismic_classification_pipeline(
        project_root=PROJECT_ROOT,
        dataset_config=DatasetConfig(n_samples_per_class=180),
    )


def run_demo(uploaded_file):
    artifacts = _load_pipeline()
    dataset_config = DatasetConfig()
    best_model_name = artifacts.model_artifacts.best_model_name
    best_test_eval = artifacts.model_artifacts.evaluations[f"{best_model_name}__test"]
    best_row = artifacts.model_artifacts.summary_table[
        (artifacts.model_artifacts.summary_table["model"] == best_model_name)
        & (artifacts.model_artifacts.summary_table["split"] == "test")
    ].iloc[0]

    archive = np.load(artifacts.dataset_paths["npz"])
    metadata = pd.read_csv(artifacts.dataset_paths["metadata"])
    waveforms = archive["signals"]

    summary = f"""
### Earthquake signal classification

- Curated samples per class: `{artifacts.dataset_summary["class_counts"]}`
- Best model: `{best_model_name}`
- Test accuracy: `{best_row["accuracy"]:.3f}`
- Test macro F1: `{best_row["macro_f1"]:.3f}`
- Log loss: `{best_row["log_loss"]:.3f}`
- Brier score: `{best_row["multiclass_brier"]:.3f}`
"""

    inference_table = None
    if uploaded_file is not None:
        inference_table = predict_csv_waveform(uploaded_file.name, artifacts.model_bundle_path).round(4)

    importance_plot = plot_feature_importance(artifacts.model_artifacts.feature_importances, best_model_name)
    confidence_plot = plot_prediction_confidence(best_test_eval.predictions, best_model_name)
    microseism_index = int(metadata.loc[metadata["label"] == "microseisms", "sample_index"].iloc[0])

    return (
        summary,
        artifacts.model_artifacts.summary_table.round(4),
        inference_table,
        plot_example_waveforms(waveforms, metadata, sample_rate_hz=dataset_config.sample_rate_hz),
        plot_average_spectra(waveforms, metadata, sample_rate_hz=dataset_config.sample_rate_hz),
        plot_scalogram_example(waveforms[microseism_index], sample_rate_hz=dataset_config.sample_rate_hz),
        plot_confusion_matrix(best_test_eval.confusion, f"Confusion matrix - {best_model_name}"),
        importance_plot,
        confidence_plot,
    )


with gr.Blocks(title="Earthquake Signal Classification") as demo:
    gr.Markdown(
        """
# Earthquake Signal Classification

Train a reproducible tri-class seismic classifier and optionally score a CSV waveform.
The expected upload format is a single numeric column with waveform amplitudes.
"""
    )
    uploaded_file = gr.File(label="Optional waveform CSV", file_types=[".csv"])
    run_button = gr.Button("Run portfolio demo", variant="primary")

    summary_output = gr.Markdown()
    metrics_output = gr.Dataframe(label="Model metrics")
    inference_output = gr.Dataframe(label="Uploaded waveform probabilities")
    waveform_plot = gr.Plot(label="Waveform examples")
    spectra_plot = gr.Plot(label="Frequency spectra")
    scalogram_plot = gr.Plot(label="Wavelet scalogram")
    confusion_plot = gr.Plot(label="Confusion matrix")
    importance_plot = gr.Plot(label="Feature importances")
    confidence_plot = gr.Plot(label="Prediction confidence")

    run_button.click(
        fn=run_demo,
        inputs=[uploaded_file],
        outputs=[
            summary_output,
            metrics_output,
            inference_output,
            waveform_plot,
            spectra_plot,
            scalogram_plot,
            confusion_plot,
            importance_plot,
            confidence_plot,
        ],
    )


if __name__ == "__main__":
    demo.launch()
