from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
import pickle

import numpy as np
import pandas as pd

from .data import DatasetConfig, load_or_build_dataset, summarize_dataset
from .features import FeatureConfig, build_feature_table, select_feature_columns
from .modeling import ModelArtifacts, train_and_compare_models
from .preprocessing import PreprocessingConfig, preprocess_dataset, preprocess_waveform


@dataclass(slots=True)
class PipelineArtifacts:
    dataset_summary: dict[str, object]
    features_df: pd.DataFrame
    model_artifacts: ModelArtifacts
    processed_waveforms_path: Path
    dataset_paths: dict[str, Path]
    model_bundle_path: Path
    metrics_path: Path
    predictions_path: Path
    summary_path: Path


def _project_paths(project_root: Path) -> dict[str, Path]:
    return {
        "project_root": project_root,
        "processed_dir": project_root / "data" / "processed",
        "models_dir": project_root / "data" / "processed" / "models",
        "reports_dir": project_root / "data" / "processed" / "reports",
    }


def run_seismic_classification_pipeline(
    project_root: Path,
    dataset_config: DatasetConfig | None = None,
    preprocessing_config: PreprocessingConfig | None = None,
    feature_config: FeatureConfig | None = None,
) -> PipelineArtifacts:
    dataset_config = dataset_config or DatasetConfig()
    preprocessing_config = preprocessing_config or PreprocessingConfig()
    feature_config = feature_config or FeatureConfig()

    paths = _project_paths(project_root)
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)

    waveforms, metadata, dataset_config, dataset_paths = load_or_build_dataset(
        dataset_dir=paths["processed_dir"],
        config=dataset_config,
    )
    processed_waveforms = preprocess_dataset(waveforms, dataset_config.sample_rate_hz, preprocessing_config)
    processed_waveforms_path = paths["processed_dir"] / "processed_waveforms.npy"
    pd.DataFrame(metadata).to_csv(dataset_paths["metadata"], index=False)
    np.save(processed_waveforms_path, processed_waveforms.astype("float32"))

    features_df = build_feature_table(
        processed_waveforms,
        metadata=metadata,
        sample_rate_hz=dataset_config.sample_rate_hz,
        config=feature_config,
    )
    model_artifacts = train_and_compare_models(features_df, random_seed=dataset_config.random_seed)

    metrics_frames = [bundle.summary for bundle in model_artifacts.evaluations.values()]
    metrics_df = pd.concat(metrics_frames, ignore_index=True)
    metrics_path = paths["reports_dir"] / "model_metrics.csv"
    metrics_df.to_csv(metrics_path, index=False)

    predictions_df = pd.concat(
        [bundle.predictions for bundle in model_artifacts.evaluations.values()],
        ignore_index=True,
    )
    predictions_path = paths["reports_dir"] / "predictions.csv"
    predictions_df.to_csv(predictions_path, index=False)

    dataset_summary = summarize_dataset(metadata, dataset_config)
    summary_payload = {
        "dataset": dataset_summary,
        "preprocessing": asdict(preprocessing_config),
        "features": asdict(feature_config),
        "best_model": model_artifacts.best_model_name,
    }
    summary_path = paths["reports_dir"] / "run_summary.json"
    summary_path.write_text(json.dumps(summary_payload, indent=2), encoding="utf-8")

    bundle = {
        "model": model_artifacts.best_model,
        "feature_columns": model_artifacts.feature_columns,
        "labels": model_artifacts.labels,
        "dataset_config": asdict(dataset_config),
        "preprocessing_config": asdict(preprocessing_config),
    }
    model_bundle_path = paths["models_dir"] / "best_model.pkl"
    with model_bundle_path.open("wb") as file:
        pickle.dump(bundle, file)

    return PipelineArtifacts(
        dataset_summary=dataset_summary,
        features_df=features_df,
        model_artifacts=model_artifacts,
        processed_waveforms_path=processed_waveforms_path,
        dataset_paths=dataset_paths,
        model_bundle_path=model_bundle_path,
        metrics_path=metrics_path,
        predictions_path=predictions_path,
        summary_path=summary_path,
    )


def classify_single_waveform(
    waveform,
    model_bundle_path: Path,
) -> pd.DataFrame:
    with model_bundle_path.open("rb") as file:
        bundle = pickle.load(file)

    sample_rate_hz = float(bundle["dataset_config"]["sample_rate_hz"])
    processed = preprocess_waveform(waveform, sample_rate_hz=sample_rate_hz)
    features_df = build_feature_table(
        processed.reshape(1, -1),
        metadata=pd.DataFrame(
            [
                {
                    "signal_id": "uploaded_signal",
                    "label": "unknown",
                    "split": "inference",
                    "station_id": "user_supplied",
                }
            ]
        ),
        sample_rate_hz=sample_rate_hz,
    )
    x = features_df[select_feature_columns(features_df)].to_numpy()
    model = bundle["model"]
    probabilities = model.predict_proba(x)[0]
    return pd.DataFrame(
        {
            "label": bundle["labels"],
            "probability": probabilities,
        }
    ).sort_values("probability", ascending=False)
