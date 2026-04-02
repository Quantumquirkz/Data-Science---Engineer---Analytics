from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
import pickle

import matplotlib.pyplot as plt
import pandas as pd

from .data import DatasetConfig, assign_temporal_split, load_or_build_merged_table, summarize_raw_dataset
from .features import FeatureConfig, build_feature_table
from .modeling import ModelArtifacts, train_forecast_models
from .preprocessing import PreprocessingConfig, preprocess_hourly_frame
from .visualization import plot_stl_decomposition


@dataclass(slots=True)
class PipelineArtifacts:
    dataset_summary: dict[str, object]
    features_df: pd.DataFrame
    model_artifacts: ModelArtifacts
    merged_cache_path: Path
    features_path: Path
    metrics_path: Path
    predictions_path: Path
    summary_path: Path
    model_bundle_path: Path
    stl_figure_path: Path | None


def _project_paths(project_root: Path) -> dict[str, Path]:
    processed = project_root / "data" / "processed"
    return {
        "project_root": project_root,
        "processed_dir": processed,
        "models_dir": processed / "models",
        "reports_dir": processed / "reports",
    }


def run_power_grid_load_pipeline(
    project_root: Path,
    dataset_config: DatasetConfig | None = None,
    preprocessing_config: PreprocessingConfig | None = None,
    feature_config: FeatureConfig | None = None,
    save_stl_plot: bool = True,
) -> PipelineArtifacts:
    dataset_config = dataset_config or DatasetConfig()
    preprocessing_config = preprocessing_config or PreprocessingConfig()
    feature_config = feature_config or FeatureConfig()

    paths = _project_paths(project_root)
    for key in ("processed_dir", "models_dir", "reports_dir"):
        paths[key].mkdir(parents=True, exist_ok=True)

    merged_frame, merged_path = load_or_build_merged_table(paths["processed_dir"], dataset_config)
    clean_frame = preprocess_hourly_frame(merged_frame, preprocessing_config)
    split = assign_temporal_split(clean_frame, dataset_config.validation_months)
    dataset_summary = summarize_raw_dataset(clean_frame, split)

    features_df = build_feature_table(
        clean_frame,
        split=split,
        country_code=dataset_config.country_code,
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

    stl_path: Path | None = None
    if save_stl_plot:
        train_load = clean_frame.loc[split == "train", "load_mw"]
        min_hours = 24 * 14
        if len(train_load) > min_hours:
            fig = plot_stl_decomposition(train_load, seasonal_period=24)
            stl_path = paths["reports_dir"] / "stl_load_decomposition.png"
            fig.savefig(stl_path, dpi=120, bbox_inches="tight")
            plt.close(fig)

    ensemble_payload = {
        str(h): model_artifacts.ensemble_weights[h].tolist()
        for h in model_artifacts.horizons
    }
    ensemble_names_payload = {
        str(h): list(model_artifacts.ensemble_component_names[h]) for h in model_artifacts.horizons
    }

    summary_payload = {
        "dataset": dataset_summary,
        "preprocessing": asdict(preprocessing_config),
        "features": asdict(feature_config),
        "best_point_model": model_artifacts.best_point_model_name,
        "forecast_horizons": list(feature_config.forecast_horizons_hours),
        "sarimax_fitted": model_artifacts.sarimax_fitted,
        "ensemble_weights": ensemble_payload,
        "ensemble_component_names": ensemble_names_payload,
    }
    summary_path = paths["reports_dir"] / "run_summary.json"
    summary_path.write_text(json.dumps(summary_payload, indent=2), encoding="utf-8")

    bundle = {
        "feature_columns": model_artifacts.feature_columns,
        "lgb_models": model_artifacts.lgb_models,
        "ridge_models": model_artifacts.ridge_models,
        "hgb_models": model_artifacts.hgb_models,
        "hourly_dow_median": model_artifacts.hourly_dow_median,
        "ensemble_weights": model_artifacts.ensemble_weights,
        "ensemble_component_names": model_artifacts.ensemble_component_names,
        "dataset_config": asdict(dataset_config),
        "feature_config": asdict(feature_config),
        "preprocessing_config": asdict(preprocessing_config),
        "sarimax_fitted": model_artifacts.sarimax_fitted,
    }
    model_bundle_path = paths["models_dir"] / "forecast_bundle.pkl"
    with model_bundle_path.open("wb") as file:
        pickle.dump(bundle, file)

    return PipelineArtifacts(
        dataset_summary=dataset_summary,
        features_df=features_df,
        model_artifacts=model_artifacts,
        merged_cache_path=merged_path,
        features_path=features_path,
        metrics_path=metrics_path,
        predictions_path=predictions_path,
        summary_path=summary_path,
        model_bundle_path=model_bundle_path,
        stl_figure_path=stl_path,
    )
