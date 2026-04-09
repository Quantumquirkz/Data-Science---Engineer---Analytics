from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
import pickle

import pandas as pd

from .data import DatasetConfig, assign_temporal_split, load_or_build_raw_table, summarize_raw_dataset
from .features import FeatureConfig, build_feature_table
from .modeling import ModelArtifacts, train_forecast_models
from .preprocessing import PreprocessingConfig, preprocess_hourly_frame


@dataclass(slots=True)
class PipelineArtifacts:
    dataset_summary: dict[str, object]
    features_df: pd.DataFrame
    model_artifacts: ModelArtifacts
    raw_cache_path: Path
    features_path: Path
    metrics_path: Path
    predictions_path: Path
    summary_path: Path
    model_bundle_path: Path


def _project_paths(project_root: Path) -> dict[str, Path]:
    processed = project_root / "data" / "processed"
    return {
        "project_root": project_root,
        "processed_dir": processed,
        "models_dir": processed / "models",
        "reports_dir": processed / "reports",
    }


def run_solar_irradiance_pipeline(
    project_root: Path,
    dataset_config: DatasetConfig | None = None,
    preprocessing_config: PreprocessingConfig | None = None,
    feature_config: FeatureConfig | None = None,
) -> PipelineArtifacts:
    dataset_config = dataset_config or DatasetConfig()
    preprocessing_config = preprocessing_config or PreprocessingConfig()
    feature_config = feature_config or FeatureConfig()

    paths = _project_paths(project_root)
    for key in ("processed_dir", "models_dir", "reports_dir"):
        paths[key].mkdir(parents=True, exist_ok=True)

    raw_frame, cache_path = load_or_build_raw_table(paths["processed_dir"], dataset_config)
    clean_frame = preprocess_hourly_frame(raw_frame, preprocessing_config)
    split = assign_temporal_split(clean_frame, dataset_config.validation_months)
    dataset_summary = summarize_raw_dataset(clean_frame, split)

    features_df = build_feature_table(
        clean_frame,
        latitude=dataset_config.latitude,
        longitude=dataset_config.longitude,
        split=split,
        config=feature_config,
    )
    features_path = paths["processed_dir"] / "features_dataset.parquet"
    features_df.to_parquet(features_path)

    model_artifacts = train_forecast_models(
        features_df,
        random_seed=dataset_config.random_seed,
        feature_config=feature_config,
    )

    metrics_path = paths["reports_dir"] / "model_metrics.csv"
    model_artifacts.metrics.to_csv(metrics_path, index=False)

    predictions_path = paths["reports_dir"] / "validation_predictions.csv"
    model_artifacts.predictions_validation.to_csv(predictions_path, index=False)

    summary_payload = {
        "dataset": dataset_summary,
        "preprocessing": asdict(preprocessing_config),
        "features": asdict(feature_config),
        "best_point_model": model_artifacts.best_point_model_name,
        "forecast_horizons": list(feature_config.forecast_horizons_hours),
    }
    summary_path = paths["reports_dir"] / "run_summary.json"
    summary_path.write_text(json.dumps(summary_payload, indent=2), encoding="utf-8")

    bundle = {
        "feature_columns": model_artifacts.feature_columns,
        "lgb_models": model_artifacts.lgb_models,
        "ridge_models": model_artifacts.ridge_models,
        "hgb_models": model_artifacts.hgb_models,
        "hourly_median_ghi": model_artifacts.hourly_median_ghi,
        "dataset_config": asdict(dataset_config),
        "feature_config": asdict(feature_config),
        "preprocessing_config": asdict(preprocessing_config),
    }
    model_bundle_path = paths["models_dir"] / "forecast_bundle.pkl"
    with model_bundle_path.open("wb") as file:
        pickle.dump(bundle, file)

    return PipelineArtifacts(
        dataset_summary=dataset_summary,
        features_df=features_df,
        model_artifacts=model_artifacts,
        raw_cache_path=cache_path,
        features_path=features_path,
        metrics_path=metrics_path,
        predictions_path=predictions_path,
        summary_path=summary_path,
        model_bundle_path=model_bundle_path,
    )
