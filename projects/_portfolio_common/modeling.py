from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor, IsolationForest, RandomForestClassifier
from sklearn.linear_model import Ridge
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error, mean_squared_error, r2_score, roc_auc_score, silhouette_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from .spec import ProjectSpec


@dataclass(slots=True)
class ModelResult:
    metrics: pd.DataFrame
    predictions: pd.DataFrame
    model_name: str
    pca_projection: pd.DataFrame


CLASSIFICATION_TASKS = {"classification", "segmentation", "rare_event", "anomaly", "event_detection", "recommendation"}
UNSUPERVISED_TASKS = {"clustering", "compression", "knowledge_graph", "platform"}


def _split(features: pd.DataFrame, feature_columns: list[str], target_name: str):
    x = features[feature_columns].astype(float)
    y = pd.to_numeric(features[target_name], errors="coerce")
    return train_test_split(x, y, test_size=0.25, random_state=42, shuffle=True)


def _projection(features: pd.DataFrame, feature_columns: list[str]) -> pd.DataFrame:
    scaled = StandardScaler().fit_transform(features[feature_columns].astype(float))
    coords = PCA(n_components=2, random_state=42).fit_transform(scaled)
    return pd.DataFrame({"pc1": coords[:, 0], "pc2": coords[:, 1]})


def train_project_models(features: pd.DataFrame, feature_columns: list[str], spec: ProjectSpec) -> ModelResult:
    projection = _projection(features, feature_columns)

    if spec.task_kind in UNSUPERVISED_TASKS:
        scaled = StandardScaler().fit_transform(features[feature_columns].astype(float))
        kmeans = KMeans(n_clusters=3, n_init=10, random_state=spec.random_seed)
        clusters = kmeans.fit_predict(scaled)
        iso = IsolationForest(contamination=0.1, random_state=spec.random_seed)
        anomaly_pred = (iso.fit_predict(scaled) == -1).astype(int)
        sil = silhouette_score(scaled, clusters)
        metrics = pd.DataFrame(
            [
                {"model": "kmeans_pca", "metric": "silhouette", "value": float(sil)},
                {"model": "isolation_forest", "metric": "flagged_rate", "value": float(anomaly_pred.mean())},
            ]
        )
        predictions = features[["timestamp", spec.target_name]].copy()
        predictions["prediction"] = clusters
        predictions["anomaly_score"] = anomaly_pred
        return ModelResult(metrics=metrics, predictions=predictions, model_name="kmeans_pca", pca_projection=projection)

    x_train, x_test, y_train, y_test = _split(features, feature_columns, spec.target_name)
    predictions = features.loc[x_test.index, ["timestamp", spec.target_name]].copy()

    if spec.task_kind in CLASSIFICATION_TASKS:
        y_train_i = y_train.round().astype(int)
        y_test_i = y_test.round().astype(int)
        model = make_pipeline(
            StandardScaler(),
            RandomForestClassifier(n_estimators=120, min_samples_leaf=3, random_state=spec.random_seed),
        )
        model.fit(x_train, y_train_i)
        pred = model.predict(x_test)
        predictions["prediction"] = pred
        metric_rows = [
            {"model": "random_forest", "metric": "accuracy", "value": float(accuracy_score(y_test_i, pred))},
            {"model": "random_forest", "metric": "macro_f1", "value": float(f1_score(y_test_i, pred, average="macro"))},
        ]
        if len(np.unique(y_test_i)) == 2:
            proba = model.predict_proba(x_test)[:, 1]
            predictions["score"] = proba
            metric_rows.append({"model": "random_forest", "metric": "roc_auc", "value": float(roc_auc_score(y_test_i, proba))})
        baseline = HistGradientBoostingClassifier(random_state=spec.random_seed)
        baseline.fit(x_train, y_train_i)
        baseline_pred = baseline.predict(x_test)
        metric_rows.append(
            {"model": "hist_gradient_boosting", "metric": "macro_f1", "value": float(f1_score(y_test_i, baseline_pred, average="macro"))}
        )
        return ModelResult(metrics=pd.DataFrame(metric_rows), predictions=predictions, model_name="random_forest", pca_projection=projection)

    ridge = make_pipeline(StandardScaler(), Ridge(alpha=1.0))
    hgb = HistGradientBoostingRegressor(random_state=spec.random_seed, max_iter=180, learning_rate=0.06)
    ridge.fit(x_train, y_train)
    hgb.fit(x_train, y_train)
    pred_ridge = ridge.predict(x_test)
    pred_hgb = hgb.predict(x_test)
    pred = 0.35 * pred_ridge + 0.65 * pred_hgb
    predictions["prediction"] = pred
    predictions["ridge_prediction"] = pred_ridge
    predictions["hgb_prediction"] = pred_hgb
    rmse = mean_squared_error(y_test, pred) ** 0.5
    metrics = pd.DataFrame(
        [
            {"model": "ridge_hgb_ensemble", "metric": "rmse", "value": float(rmse)},
            {"model": "ridge_hgb_ensemble", "metric": "mae", "value": float(mean_absolute_error(y_test, pred))},
            {"model": "ridge_hgb_ensemble", "metric": "r2", "value": float(r2_score(y_test, pred))},
            {"model": "ridge", "metric": "rmse", "value": float(mean_squared_error(y_test, pred_ridge) ** 0.5)},
            {"model": "hist_gradient_boosting", "metric": "rmse", "value": float(mean_squared_error(y_test, pred_hgb) ** 0.5)},
        ]
    )
    return ModelResult(metrics=metrics, predictions=predictions, model_name="ridge_hgb_ensemble", pca_projection=projection)
