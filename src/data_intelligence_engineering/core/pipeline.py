from __future__ import annotations

import json
import pickle
from dataclasses import asdict, dataclass
from pathlib import Path

import pandas as pd

from ..catalog.schemas import ProjectSpec
from ..data.loaders import load_or_build_dataset, summarize_dataset
from ..data.preprocessing import preprocess_observations
from ..features.tabular import build_feature_table
from ..modeling.training import ModelResult, train_project_models
from ..visualization.plots import save_project_figures


@dataclass(slots=True)
class PipelineArtifacts:
    dataset_summary: dict[str, object]
    features_df: pd.DataFrame
    model_result: ModelResult
    raw_path: Path
    features_path: Path
    metrics_path: Path
    predictions_path: Path
    summary_path: Path
    model_bundle_path: Path
    figure_paths: dict[str, Path]


def run_portfolio_pipeline(
    project_root: Path,
    spec: ProjectSpec,
    n_samples: int = 720,
    random_seed: int | None = None,
) -> PipelineArtifacts:
    processed = project_root / "data" / "processed"
    reports = processed / "reports"
    models = processed / "models"
    for directory in (processed, reports, models):
        directory.mkdir(parents=True, exist_ok=True)

    raw_frame, raw_path = load_or_build_dataset(project_root, spec, n_samples=n_samples, random_seed=random_seed)
    clean = preprocess_observations(raw_frame)
    features_df, feature_columns = build_feature_table(clean, spec)
    features_path = processed / "features_dataset.parquet"
    features_df.to_parquet(features_path)

    model_result = train_project_models(features_df, feature_columns, spec)
    metrics_path = reports / "model_metrics.csv"
    predictions_path = reports / "validation_predictions.csv"
    model_result.metrics.to_csv(metrics_path, index=False)
    model_result.predictions.to_csv(predictions_path, index=False)

    figure_paths = save_project_figures(
        features=features_df,
        predictions=model_result.predictions,
        projection=model_result.pca_projection,
        spec=spec,
        reports_dir=reports,
    )

    dataset_summary = summarize_dataset(features_df, spec)
    summary_payload = {
        "spec": asdict(spec),
        "dataset": dataset_summary,
        "feature_columns": feature_columns,
        "model": model_result.model_name,
        "figures": {name: str(path) for name, path in figure_paths.items()},
    }
    summary_path = reports / "run_summary.json"
    summary_path.write_text(json.dumps(summary_payload, indent=2), encoding="utf-8")

    model_bundle_path = models / "portfolio_bundle.pkl"
    with model_bundle_path.open("wb") as file:
        pickle.dump(
            {
                "spec": asdict(spec),
                "feature_columns": feature_columns,
                "model_name": model_result.model_name,
                "metrics": model_result.metrics,
            },
            file,
        )

    return PipelineArtifacts(
        dataset_summary=dataset_summary,
        features_df=features_df,
        model_result=model_result,
        raw_path=raw_path,
        features_path=features_path,
        metrics_path=metrics_path,
        predictions_path=predictions_path,
        summary_path=summary_path,
        model_bundle_path=model_bundle_path,
        figure_paths=figure_paths,
    )
