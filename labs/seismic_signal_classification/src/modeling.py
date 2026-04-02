from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from .evaluation import EvaluationBundle, compare_model_summaries, evaluate_classifier
from .features import select_feature_columns


@dataclass(slots=True)
class ModelArtifacts:
    feature_columns: list[str]
    labels: list[str]
    models: dict[str, object]
    evaluations: dict[str, EvaluationBundle]
    summary_table: pd.DataFrame
    best_model_name: str
    best_model: object
    feature_importances: pd.DataFrame


def _build_estimators(random_seed: int) -> dict[str, object]:
    baseline = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1_500,
                    random_state=random_seed,
                ),
            ),
        ]
    )
    forest = CalibratedClassifierCV(
        estimator=RandomForestClassifier(
            n_estimators=300,
            max_depth=12,
            min_samples_leaf=2,
            random_state=random_seed,
            n_jobs=-1,
        ),
        method="sigmoid",
        cv=3,
    )
    return {
        "logistic_regression": baseline,
        "calibrated_random_forest": forest,
    }


def train_and_compare_models(features_df: pd.DataFrame, random_seed: int = 42) -> ModelArtifacts:
    feature_columns = select_feature_columns(features_df)
    labels = sorted(features_df["label"].unique().tolist())

    train_mask = features_df["split"] == "train"
    validation_mask = features_df["split"] == "validation"
    test_mask = features_df["split"] == "test"

    train_df = features_df.loc[train_mask].reset_index(drop=True)
    validation_df = features_df.loc[validation_mask].reset_index(drop=True)
    test_df = features_df.loc[test_mask].reset_index(drop=True)

    x_train = train_df[feature_columns].to_numpy()
    y_train = train_df["label"].to_numpy()

    x_validation = validation_df[feature_columns].to_numpy()
    y_validation = validation_df["label"].to_numpy()

    x_test = test_df[feature_columns].to_numpy()
    y_test = test_df["label"].to_numpy()

    evaluations: dict[str, EvaluationBundle] = {}
    models = _build_estimators(random_seed)
    summary_frames: list[pd.DataFrame] = []
    feature_importances: list[pd.DataFrame] = []

    for model_name, estimator in models.items():
        estimator.fit(x_train, y_train)
        validation_predictions = estimator.predict(x_validation)
        validation_probabilities = estimator.predict_proba(x_validation)
        validation_eval = evaluate_classifier(
            model_name=model_name,
            split_name="validation",
            y_true=y_validation,
            y_pred=validation_predictions,
            probabilities=validation_probabilities,
            labels=labels,
            signal_ids=validation_df["signal_id"].to_numpy(),
        )
        evaluations[f"{model_name}__validation"] = validation_eval
        summary_frames.append(validation_eval.summary)

        test_predictions = estimator.predict(x_test)
        test_probabilities = estimator.predict_proba(x_test)
        test_eval = evaluate_classifier(
            model_name=model_name,
            split_name="test",
            y_true=y_test,
            y_pred=test_predictions,
            probabilities=test_probabilities,
            labels=labels,
            signal_ids=test_df["signal_id"].to_numpy(),
        )
        evaluations[f"{model_name}__test"] = test_eval
        summary_frames.append(test_eval.summary)

        inner_estimator = getattr(estimator, "estimator", estimator)
        if hasattr(inner_estimator, "feature_importances_"):
            feature_importances.append(
                pd.DataFrame(
                    {
                        "model": model_name,
                        "feature": feature_columns,
                        "importance": inner_estimator.feature_importances_,
                    }
                )
            )
        elif hasattr(inner_estimator, "named_steps"):
            classifier = inner_estimator.named_steps["classifier"]
            importances = np.mean(np.abs(classifier.coef_), axis=0)
            feature_importances.append(
                pd.DataFrame(
                    {
                        "model": model_name,
                        "feature": feature_columns,
                        "importance": importances,
                    }
                )
            )

    summary_table = pd.concat(summary_frames, ignore_index=True)
    validation_summary = summary_table.loc[summary_table["split"] == "validation"].copy()
    best_model_name = (
        validation_summary.sort_values(["macro_f1", "accuracy"], ascending=False).iloc[0]["model"]
    )
    importance_table = pd.concat(feature_importances, ignore_index=True)
    return ModelArtifacts(
        feature_columns=feature_columns,
        labels=labels,
        models=models,
        evaluations=evaluations,
        summary_table=compare_model_summaries(list(evaluations.values())),
        best_model_name=str(best_model_name),
        best_model=models[str(best_model_name)],
        feature_importances=importance_table,
    )
