from __future__ import annotations

import json
import re
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_PATH = ROOT / "docs" / "PROJECTS.md"
README_PATH = ROOT / "README.md"
PROJECTS_DIR = ROOT / "projects"


COMMON_FILES: dict[str, str] = {
    "__init__.py": '''"""Shared machinery for generated portfolio projects."""

from .spec import ProjectSpec
from .pipeline import PipelineArtifacts, run_portfolio_pipeline

__all__ = ["PipelineArtifacts", "ProjectSpec", "run_portfolio_pipeline"]
''',
    "spec.py": '''from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProjectSpec:
    """Configuration that makes one portfolio project domain-specific."""

    number: int
    slug: str
    title: str
    description: str
    theoretical_stack: str
    domain: str
    task_kind: str
    target_name: str
    public_data_note: str
    random_seed: int
''',
    "data.py": r'''from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .spec import ProjectSpec


def _domain_coordinates(domain: str, n_samples: int, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    if domain in {"spatial", "environment", "geoscience", "astronomy"}:
        x = rng.uniform(-1.0, 1.0, n_samples)
        y = rng.uniform(-1.0, 1.0, n_samples)
    elif domain in {"network", "logistics", "traffic", "recommendation"}:
        x = rng.integers(0, 25, n_samples).astype(float)
        y = rng.integers(0, 25, n_samples).astype(float)
    else:
        x = np.linspace(-1.0, 1.0, n_samples)
        y = rng.normal(0.0, 0.45, n_samples)
    return x, y


def generate_domain_dataset(spec: ProjectSpec, n_samples: int = 720, random_seed: int | None = None) -> pd.DataFrame:
    """Generate a reproducible research-grade proxy dataset for the project domain.

    The generated table is intentionally compact enough for portfolio demos while
    preserving the dominant structure of the target problem: temporal dynamics,
    spatial fields, nonlinear physical response, rare events, and noisy sensors.
    """

    seed = spec.random_seed if random_seed is None else random_seed
    rng = np.random.default_rng(seed)
    n_samples = int(max(180, n_samples))
    t = np.arange(n_samples, dtype=float)
    phase = 2.0 * np.pi * t / max(n_samples, 1)
    x, y = _domain_coordinates(spec.domain, n_samples, rng)

    seasonal = np.sin(phase * 4.0)
    slow_trend = (t - t.mean()) / max(t.std(), 1.0)
    wave = np.sin(3.0 * x + 2.0 * y + phase) + 0.35 * np.cos(5.0 * y - phase / 2.0)
    forcing = 0.7 * seasonal + 0.25 * slow_trend + rng.normal(0.0, 0.08, n_samples)
    sensor_a = wave + forcing + rng.normal(0.0, 0.12, n_samples)
    sensor_b = 0.55 * np.cos(2.0 * x - y) + 0.35 * seasonal + rng.normal(0.0, 0.15, n_samples)
    sensor_c = np.sin(sensor_a) + 0.2 * sensor_b + rng.normal(0.0, 0.10, n_samples)
    stressor = np.abs(sensor_a) + 0.6 * np.abs(sensor_b) + 0.2 * np.maximum(slow_trend, 0)
    physics_response = 1.6 * sensor_a - 0.9 * sensor_b + 0.45 * sensor_c**2 + 0.25 * x * y

    anomaly_score = stressor + 0.25 * rng.normal(size=n_samples)
    anomaly_threshold = np.quantile(anomaly_score, 0.90)
    anomaly = anomaly_score > anomaly_threshold
    class_label = pd.qcut(
        physics_response + 0.45 * anomaly.astype(float) + rng.normal(0.0, 0.25, n_samples),
        q=3,
        labels=False,
        duplicates="drop",
    )
    class_label = np.asarray(class_label, dtype=int)
    target = physics_response + 0.35 * forcing + rng.normal(0.0, 0.18, n_samples)

    if spec.task_kind in {"forecasting", "state_space", "control"}:
        target = pd.Series(target).rolling(8, min_periods=1).mean().shift(-1).bfill().to_numpy()
    elif spec.task_kind in {"classification", "segmentation", "rare_event"}:
        target = class_label
    elif spec.task_kind in {"anomaly", "event_detection"}:
        target = anomaly.astype(int)
    elif spec.task_kind in {"optimization", "simulation"}:
        target = target - 0.35 * np.square(sensor_b) + 0.15 * np.maximum(sensor_a, 0)
    elif spec.task_kind == "recommendation":
        target = 0.5 * class_label + 0.5 * (sensor_a > np.median(sensor_a)).astype(int)

    frame = pd.DataFrame(
        {
            "timestamp": pd.date_range("2024-01-01", periods=n_samples, freq="h"),
            "x_coord": x,
            "y_coord": y,
            "sensor_a": sensor_a,
            "sensor_b": sensor_b,
            "sensor_c": sensor_c,
            "external_forcing": forcing,
            "physics_signal": physics_response,
            "stressor_index": stressor,
            "anomaly": anomaly.astype(int),
            "class_label": class_label,
            spec.target_name: target,
        }
    )
    return frame


def load_or_build_dataset(
    project_root: Path,
    spec: ProjectSpec,
    n_samples: int = 720,
    random_seed: int | None = None,
) -> tuple[pd.DataFrame, Path]:
    processed = project_root / "data" / "processed"
    processed.mkdir(parents=True, exist_ok=True)
    raw_path = processed / "synthetic_domain_observations.csv"
    frame = generate_domain_dataset(spec, n_samples=n_samples, random_seed=random_seed)
    frame.to_csv(raw_path, index=False)
    return frame, raw_path


def summarize_dataset(frame: pd.DataFrame, spec: ProjectSpec) -> dict[str, object]:
    target = frame[spec.target_name]
    return {
        "project": spec.title,
        "rows": int(len(frame)),
        "columns": int(frame.shape[1]),
        "domain": spec.domain,
        "task_kind": spec.task_kind,
        "target": spec.target_name,
        "target_mean": float(pd.to_numeric(target, errors="coerce").mean()),
        "target_std": float(pd.to_numeric(target, errors="coerce").std()),
        "anomaly_rate": float(frame["anomaly"].mean()) if "anomaly" in frame else None,
        "data_policy": spec.public_data_note,
    }
''',
    "preprocessing.py": '''from __future__ import annotations

import pandas as pd


def preprocess_observations(frame: pd.DataFrame) -> pd.DataFrame:
    clean = frame.copy()
    clean["timestamp"] = pd.to_datetime(clean["timestamp"], errors="coerce")
    clean = clean.sort_values("timestamp").reset_index(drop=True)
    numeric_columns = clean.select_dtypes(include="number").columns
    clean[numeric_columns] = clean[numeric_columns].interpolate(limit_direction="both")
    clean[numeric_columns] = clean[numeric_columns].fillna(clean[numeric_columns].median(numeric_only=True))
    clean["hour"] = clean["timestamp"].dt.hour
    clean["dayofweek"] = clean["timestamp"].dt.dayofweek
    clean["time_index"] = range(len(clean))
    return clean
''',
    "features.py": r'''from __future__ import annotations

import numpy as np
import pandas as pd

from .spec import ProjectSpec


def build_feature_table(frame: pd.DataFrame, spec: ProjectSpec) -> tuple[pd.DataFrame, list[str]]:
    features = frame.copy()
    features["hour_sin"] = np.sin(2.0 * np.pi * features["hour"] / 24.0)
    features["hour_cos"] = np.cos(2.0 * np.pi * features["hour"] / 24.0)
    features["interaction_ab"] = features["sensor_a"] * features["sensor_b"]
    features["energy_proxy"] = features["sensor_a"] ** 2 + features["sensor_b"] ** 2 + features["sensor_c"] ** 2
    features["rolling_signal_mean"] = features["physics_signal"].rolling(12, min_periods=1).mean()
    features["rolling_signal_std"] = features["physics_signal"].rolling(12, min_periods=2).std().fillna(0.0)
    features["forcing_lag_1"] = features["external_forcing"].shift(1).bfill()
    features["target_lag_1"] = pd.to_numeric(features[spec.target_name], errors="coerce").shift(1).bfill()

    feature_columns = [
        "x_coord",
        "y_coord",
        "sensor_a",
        "sensor_b",
        "sensor_c",
        "external_forcing",
        "physics_signal",
        "stressor_index",
        "hour_sin",
        "hour_cos",
        "interaction_ab",
        "energy_proxy",
        "rolling_signal_mean",
        "rolling_signal_std",
        "forcing_lag_1",
        "target_lag_1",
    ]
    return features, feature_columns
''',
    "modeling.py": r'''from __future__ import annotations

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
''',
    "evaluation.py": '''from __future__ import annotations

import pandas as pd


def summarize_metrics(metrics: pd.DataFrame) -> str:
    best = metrics.sort_values("value", ascending=False).head(1).iloc[0]
    return f"{best['model']} / {best['metric']}: {best['value']:.3f}"
''',
    "visualization.py": r'''from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from .spec import ProjectSpec


def save_project_figures(
    features: pd.DataFrame,
    predictions: pd.DataFrame,
    projection: pd.DataFrame,
    spec: ProjectSpec,
    reports_dir: Path,
) -> dict[str, Path]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    paths: dict[str, Path] = {}

    fig, ax = plt.subplots(figsize=(8, 3.8))
    sample = features.head(240)
    ax.plot(sample["timestamp"], sample["physics_signal"], label="physics signal", linewidth=1.5)
    ax.plot(sample["timestamp"], sample["external_forcing"], label="external forcing", linewidth=1.1, alpha=0.8)
    ax.set_title(f"{spec.title}: domain signals")
    ax.set_xlabel("time")
    ax.set_ylabel("standardized units")
    ax.legend(loc="best")
    fig.autofmt_xdate()
    path = reports_dir / "domain_signals.png"
    fig.savefig(path, dpi=130, bbox_inches="tight")
    plt.close(fig)
    paths["domain_signals"] = path

    fig, ax = plt.subplots(figsize=(5.4, 4.6))
    color = features["anomaly"] if "anomaly" in features else features[spec.target_name]
    sc = ax.scatter(projection["pc1"], projection["pc2"], c=color, s=14, cmap="viridis", alpha=0.8)
    ax.set_title("Feature-space projection")
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    fig.colorbar(sc, ax=ax, label="anomaly / target")
    path = reports_dir / "feature_projection.png"
    fig.savefig(path, dpi=130, bbox_inches="tight")
    plt.close(fig)
    paths["feature_projection"] = path

    fig, ax = plt.subplots(figsize=(5.8, 4.6))
    y_true = pd.to_numeric(predictions[spec.target_name], errors="coerce")
    y_pred = pd.to_numeric(predictions["prediction"], errors="coerce")
    ax.scatter(y_true, y_pred, s=18, alpha=0.75)
    if y_true.nunique() > 5:
        low = min(y_true.min(), y_pred.min())
        high = max(y_true.max(), y_pred.max())
        ax.plot([low, high], [low, high], "--", color="black", linewidth=1)
    ax.set_title("Validation predictions")
    ax.set_xlabel("observed")
    ax.set_ylabel("predicted")
    path = reports_dir / "validation_predictions.png"
    fig.savefig(path, dpi=130, bbox_inches="tight")
    plt.close(fig)
    paths["validation_predictions"] = path

    return paths
''',
    "pipeline.py": r'''from __future__ import annotations

import json
import pickle
from dataclasses import asdict, dataclass
from pathlib import Path

import pandas as pd

from .data import load_or_build_dataset, summarize_dataset
from .features import build_feature_table
from .modeling import ModelResult, train_project_models
from .preprocessing import preprocess_observations
from .spec import ProjectSpec
from .visualization import save_project_figures


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
''',
    "inference.py": '''from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_validation_predictions(predictions_path: Path) -> pd.DataFrame:
    return pd.read_csv(predictions_path)


def load_metrics(metrics_path: Path) -> pd.DataFrame:
    return pd.read_csv(metrics_path)
''',
}


DOMAIN_KEYWORDS = [
    ("finance", ["trading", "financial", "portfolio", "market", "pricing"]),
    ("energy", ["energy", "grid", "battery", "renewable", "storage", "power"]),
    ("environment", ["climate", "weather", "air quality", "pollution", "wildfire", "flood", "urban heat", "farming", "environmental"]),
    ("geoscience", ["atmospheric", "ocean", "seafloor", "hydrological", "reservoir", "magnetic", "earth"]),
    ("biomedical", ["protein", "blood", "neuron", "disease", "gait", "biomechanics", "healthcare"]),
    ("astronomy", ["astronomy", "cosmic", "neutrino", "gravitational wave", "satellite orbit"]),
    ("manufacturing", ["manufacturing", "semiconductor", "defect", "yield", "process", "thermal camera"]),
    ("network", ["network", "graph", "knowledge graph", "traffic", "supply chain"]),
    ("robotics", ["robot", "drone", "autonomous", "sensor fusion", "multi-agent"]),
    ("signal", ["spectroscopy", "sound", "resonance", "shockwave", "interference", "optical"]),
    ("simulation", ["simulator", "simulation", "trajectory", "orbit", "evacuation"]),
    ("recommendation", ["recommender", "recommendation", "learning paths"]),
    ("platform", ["platform", "metadata", "multi-modal", "log compression"]),
]


TASK_KEYWORDS = [
    ("forecasting", ["forecast", "predict", "nowcasting", "trend"]),
    ("classification", ["classify", "classifier", "recognize"]),
    ("anomaly", ["anomaly", "outlier", "fault", "failure", "suspicious", "defect"]),
    ("clustering", ["cluster", "segmentation", "archetypes"]),
    ("optimization", ["optimize", "optimizer", "routing", "allocation", "placement", "control"]),
    ("simulation", ["simulate", "simulator", "trajectory"]),
    ("reconstruction", ["reconstruct", "impute", "compression", "assimil"]),
    ("event_detection", ["detect", "search", "localize"]),
    ("recommendation", ["recommend"]),
    ("knowledge_graph", ["knowledge graph", "metadata"]),
    ("platform", ["platform", "ingest", "query"]),
]


PUBLIC_DATA_NOTES = {
    "finance": "Public-first when stable market samples are available; synthetic fallback for offline demos.",
    "energy": "Mix public energy benchmarks with reproducible synthetic telemetry for offline runs.",
    "environment": "Public meteorological or geospatial data can be swapped in; default demo uses synthetic spatial fields.",
    "geoscience": "Designed for public scientific repositories, with generated proxy fields for reproducibility.",
    "biomedical": "Uses privacy-safe synthetic proxies by default; public biomedical datasets can replace the source table.",
    "astronomy": "Compatible with open astronomy archives; default table emulates noisy detector/catalog measurements.",
    "manufacturing": "Uses synthetic process telemetry by default because production datasets are often proprietary.",
    "network": "Uses generated graph/flow proxies by default; public logs or network datasets can be mapped into the same schema.",
    "robotics": "Uses simulated telemetry by default; benchmark logs can be adapted later.",
    "signal": "Uses synthetic spectral/time-series measurements with documented public-data extension points.",
    "simulation": "Simulation-first project with reproducible stochastic scenarios.",
    "recommendation": "Uses generated interaction/content features by default; public corpora can be mapped in.",
    "platform": "Uses synthetic multi-table experiment/log metadata by default to keep the platform demo portable.",
    "general": "Uses a reproducible synthetic dataset by default, with public-data replacement points documented.",
}


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")
    return slug


def parse_projects() -> list[dict[str, object]]:
    text = DOCS_PATH.read_text(encoding="utf-8")
    pattern = re.compile(
        r"^## (?P<number>\d+)\. (?P<title>.+?)\n\n"
        r"\*\*Description:\*\* (?P<description>.+?)  \n"
        r"\*\*Theoretical stack:\*\* (?P<stack>.+?)\n",
        re.MULTILINE,
    )
    projects = []
    for match in pattern.finditer(text):
        number = int(match.group("number"))
        if number < 6:
            continue
        title = match.group("title").strip()
        description = match.group("description").strip()
        stack = match.group("stack").strip().rstrip(".")
        haystack = f"{title} {description} {stack}".lower()
        domain = next((name for name, words in DOMAIN_KEYWORDS if any(word in haystack for word in words)), "general")
        task_kind = next((name for name, words in TASK_KEYWORDS if any(word in haystack for word in words)), "regression")
        if "segmentation" in haystack:
            task_kind = "segmentation"
        if "rare" in haystack:
            task_kind = "rare_event"
        if "compression" in haystack:
            task_kind = "compression"
        projects.append(
            {
                "number": number,
                "title": title,
                "slug": slugify(title),
                "description": description,
                "stack": stack,
                "domain": domain,
                "task_kind": task_kind,
                "target_name": "target_value" if task_kind not in {"classification", "anomaly", "event_detection", "segmentation", "rare_event", "recommendation"} else "target_label",
                "public_data_note": PUBLIC_DATA_NOTES.get(domain, PUBLIC_DATA_NOTES["general"]),
                "random_seed": 1729 + number,
            }
        )
    return projects


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def spec_literal(project: dict[str, object]) -> str:
    return (
        "ProjectSpec(\n"
        f"    number={project['number']},\n"
        f"    slug={project['slug']!r},\n"
        f"    title={project['title']!r},\n"
        f"    description={project['description']!r},\n"
        f"    theoretical_stack={project['stack']!r},\n"
        f"    domain={project['domain']!r},\n"
        f"    task_kind={project['task_kind']!r},\n"
        f"    target_name={project['target_name']!r},\n"
        f"    public_data_note={project['public_data_note']!r},\n"
        f"    random_seed={project['random_seed']},\n"
        ")"
    )


def readme(project: dict[str, object]) -> str:
    title = project["title"]
    slug = project["slug"]
    function_name = f"run_{slug}_pipeline"
    return f"""# {title}

Portfolio research lab for **{title}**.

## Problem framing

{project["description"]}

The implementation is intentionally reproducible: it uses a compact domain proxy dataset by default, while the pipeline is structured so a public benchmark can replace the generated source table without changing the modeling, evaluation, or demo surface.

## Theoretical stack

{project["stack"]}.

## Data policy

{project["public_data_note"]}

## Project structure

- `src/config.py` - project metadata and domain/task configuration
- `src/data.py` - reproducible data generation/loading wrappers
- `src/preprocessing.py` - timestamp ordering, imputation, and numeric cleanup
- `src/features.py` - temporal, physical, interaction, and rolling features
- `src/modeling.py` - supervised or unsupervised models selected from the project task
- `src/evaluation.py` - metric summaries for reports and demos
- `src/visualization.py` - signal, projection, and validation plots
- `src/pipeline.py` - `{function_name}`
- `src/inference.py` - helpers to reload metrics and validation predictions
- `app.py` - Gradio portfolio demo
- `notebooks/{slug}.ipynb` - walkthrough notebook

## How to run

From the repository root:

```bash
PYTHONPATH=. uv run python -c "from pathlib import Path; from projects.{slug}.src.pipeline import {function_name}; a = {function_name}(Path('projects/{slug}')); print(a.model_result.metrics.round(3).to_string(index=False))"
```

Gradio:

```bash
PYTHONPATH=. uv run python projects/{slug}/app.py
```

Notebook:

```bash
uv run jupyter lab
```

Open `projects/{slug}/notebooks/{slug}.ipynb`.

## Suggested extensions

- Replace the generated source table with a domain-specific public benchmark.
- Add uncertainty intervals, calibration curves, or sensitivity analysis.
- Expand the Gradio demo with scenario controls tied to the governing physics or optimization constraints.
"""


def data_readme(project: dict[str, object]) -> str:
    return f"""# Data

This project defaults to a reproducible generated dataset saved under `data/processed/`.

Policy: {project["public_data_note"]}

Expected replacement schema for public data:

- `timestamp`
- `x_coord`, `y_coord`
- `sensor_a`, `sensor_b`, `sensor_c`
- `external_forcing`
- `physics_signal`
- `{project["target_name"]}`

Keep raw public downloads outside git unless they are small and redistributable.
"""


def notebook(project: dict[str, object]) -> str:
    slug = project["slug"]
    function_name = f"run_{slug}_pipeline"
    cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [f"# {project['title']}\n", "\n", f"{project['description']}\n"],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from pathlib import Path\n",
                f"from projects.{slug}.src.pipeline import {function_name}\n",
                f"artifacts = {function_name}(Path('projects/{slug}'))\n",
                "artifacts.model_result.metrics\n",
            ],
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["Generated artifacts are saved to `data/processed/reports/` for review and dashboarding.\n"],
        },
    ]
    return json.dumps(
        {
            "cells": cells,
            "metadata": {
                "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                "language_info": {"name": "python", "pygments_lexer": "ipython3"},
            },
            "nbformat": 4,
            "nbformat_minor": 5,
        },
        indent=2,
    )


def write_common() -> None:
    common_root = PROJECTS_DIR / "_portfolio_common"
    for relative, content in COMMON_FILES.items():
        write(common_root / relative, content)
    write(PROJECTS_DIR / "__init__.py", '"""Portfolio project packages."""\n')


def write_project(project: dict[str, object]) -> None:
    slug = project["slug"]
    root = PROJECTS_DIR / slug
    function_name = f"run_{slug}_pipeline"
    title = project["title"]
    write(root / "__init__.py", f'"""Portfolio project: {title}."""\n')
    write(root / "README.md", readme(project))
    write(root / "data" / "README.md", data_readme(project))
    write(root / "notebooks" / f"{slug}.ipynb", notebook(project))
    write(root / "src" / "__init__.py", f'"""Source package for {title}."""\n')
    write(
        root / "src" / "config.py",
        "from __future__ import annotations\n\n"
        "from projects._portfolio_common import ProjectSpec\n\n\n"
        f"SPEC = {spec_literal(project)}\n",
    )
    for module, common_module in [
        ("data", "data"),
        ("preprocessing", "preprocessing"),
        ("features", "features"),
        ("modeling", "modeling"),
        ("evaluation", "evaluation"),
        ("visualization", "visualization"),
        ("inference", "inference"),
    ]:
        write(
            root / "src" / f"{module}.py",
            f'"""Project-local wrappers around shared {common_module} utilities."""\n\n'
            f"from projects._portfolio_common.{common_module} import *  # noqa: F401,F403\n",
        )
    write(
        root / "src" / "pipeline.py",
        "from __future__ import annotations\n\n"
        "from pathlib import Path\n\n"
        "from projects._portfolio_common import PipelineArtifacts, run_portfolio_pipeline\n"
        "from .config import SPEC\n\n\n"
        f"def {function_name}(\n"
        "    project_root: Path,\n"
        "    n_samples: int = 720,\n"
        "    random_seed: int | None = None,\n"
        ") -> PipelineArtifacts:\n"
        "    return run_portfolio_pipeline(\n"
        "        project_root=project_root,\n"
        "        spec=SPEC,\n"
        "        n_samples=n_samples,\n"
        "        random_seed=random_seed,\n"
        "    )\n\n\n"
        f"run_pipeline = {function_name}\n",
    )
    write(
        root / "app.py",
        f"""from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import sys

import gradio as gr

PROJECT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PROJECT_ROOT.parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

from projects.{slug}.src.config import SPEC
from projects.{slug}.src.pipeline import {function_name}


@lru_cache(maxsize=1)
def _load_pipeline(n_samples: int):
    return {function_name}(PROJECT_ROOT, n_samples=int(n_samples))


def run_demo(n_samples: int):
    artifacts = _load_pipeline(int(n_samples))
    metrics = artifacts.model_result.metrics.copy()
    summary = (
        f"### {{SPEC.title}}\\n\\n"
        f"- Domain: `{{SPEC.domain}}`\\n"
        f"- Task: `{{SPEC.task_kind}}`\\n"
        f"- Rows: `{{artifacts.dataset_summary['rows']}}`\\n"
        f"- Target: `{{SPEC.target_name}}`\\n"
        f"- Data policy: {{SPEC.public_data_note}}\\n"
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
    gr.Markdown(f"# {{SPEC.title}}\\n\\n{{SPEC.description}}")
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
""",
    )


def update_docs(projects: list[dict[str, object]]) -> None:
    text = DOCS_PATH.read_text(encoding="utf-8")
    for project in projects:
        slug = project["slug"]
        title = re.escape(str(project["title"]))
        pattern = re.compile(
            rf"(## {project['number']}\. {title}\n\n"
            rf"\*\*Description:\*\* [^\n]+  \n"
            rf"\*\*Theoretical stack:\*\* [^\n]+\n)"
            rf"(?:\n*Portfolio implementation available in `projects/[^`]+/`\.\n)*",
        )
        text = pattern.sub(rf"\1\nPortfolio implementation available in `projects/{slug}/`.\n", text)
    DOCS_PATH.write_text(text, encoding="utf-8")


def update_root_readme() -> None:
    text = README_PATH.read_text(encoding="utf-8")
    old = "- **`projects/`** — Self-contained portfolio projects (pipelines, `src/`, notebooks, optional `app.py`)."
    new = (
        "- **`projects/`** — Self-contained portfolio projects (pipelines, `src/`, notebooks, Gradio demos). "
        "The catalog now continues from the first five hand-built examples into generated, reproducible implementations for projects 6-100."
    )
    if old in text:
        text = text.replace(old, new)
    anchor = "- **`docs/PROJECTS.md`** — Project idea catalog and supporting reference material."
    catalog_line = (
        "- **`projects/_portfolio_common/`** — Shared pipeline, feature, modeling, evaluation, and visualization utilities "
        "used by the generated projects 6-100."
    )
    if catalog_line not in text and anchor in text:
        text = text.replace(anchor, catalog_line + "\n" + anchor)
    README_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    projects = parse_projects()
    if len(projects) != 95:
        raise SystemExit(f"Expected 95 projects from 6-100, found {len(projects)}")
    write_common()
    for project in projects:
        write_project(project)
    update_docs(projects)
    update_root_readme()
    print(f"Generated {len(projects)} portfolio projects.")


if __name__ == "__main__":
    main()
