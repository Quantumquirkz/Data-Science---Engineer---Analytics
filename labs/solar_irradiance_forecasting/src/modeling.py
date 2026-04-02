from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from lightgbm import LGBMRegressor
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from .evaluation import metrics_row
from .features import FeatureConfig, select_feature_columns


@dataclass(slots=True)
class ModelArtifacts:
    feature_columns: list[str]
    horizons: tuple[int, ...]
    quantiles: tuple[float, ...]
    metrics: pd.DataFrame
    predictions_validation: pd.DataFrame
    lgb_models: dict[str, LGBMRegressor]
    ridge_models: dict[int, Pipeline]
    hgb_models: dict[int, HistGradientBoostingRegressor]
    hourly_median_ghi: pd.Series
    best_point_model_name: str


def _lgb_quantile_model(alpha: float, random_seed: int) -> LGBMRegressor:
    return LGBMRegressor(
        objective="quantile",
        alpha=alpha,
        n_estimators=250,
        learning_rate=0.05,
        max_depth=-1,
        num_leaves=48,
        subsample=0.85,
        colsample_bytree=0.85,
        reg_lambda=1.0,
        min_child_samples=20,
        random_state=random_seed,
        n_jobs=1,
        verbose=-1,
    )


def train_forecast_models(
    features_df: pd.DataFrame,
    random_seed: int = 42,
    feature_config: FeatureConfig | None = None,
) -> ModelArtifacts:
    feature_config = feature_config or FeatureConfig()
    horizons = feature_config.forecast_horizons_hours
    quantiles = (0.1, 0.5, 0.9)
    feature_columns = select_feature_columns(features_df)

    train_df = features_df.loc[features_df["split"] == "train"].copy()
    val_df = features_df.loc[features_df["split"] == "validation"].copy()

    hourly_median_ghi = train_df.groupby(train_df.index.hour)["ghi_wm2"].median()

    lgb_models: dict[str, LGBMRegressor] = {}
    ridge_models: dict[int, Pipeline] = {}
    hgb_models: dict[int, HistGradientBoostingRegressor] = {}

    metric_rows: list[dict[str, object]] = []
    pred_rows: list[dict[str, object]] = []

    x_train_df = train_df[feature_columns]
    x_val_df = val_df[feature_columns]
    x_train = x_train_df.to_numpy(dtype=np.float64)
    x_val = x_val_df.to_numpy(dtype=np.float64)

    for h in horizons:
        target_col = f"target_ghi_{h}h"
        y_train = train_df[target_col].to_numpy(dtype=np.float64)
        y_val = val_df[target_col].to_numpy(dtype=np.float64)

        pers_val = val_df["ghi_wm2"].to_numpy(dtype=np.float64)
        hod_val = val_df.index.hour.map(hourly_median_ghi).to_numpy(dtype=np.float64)

        metric_rows.append(
            metrics_row(h, "persistence", y_val, pers_val),
        )
        metric_rows.append(
            metrics_row(h, "hourly_median_train", y_val, hod_val),
        )

        ridge = Pipeline(
            steps=[
                ("scaler", StandardScaler()),
                ("ridge", Ridge(alpha=2.0, random_state=random_seed)),
            ]
        )
        ridge.fit(x_train, y_train)
        ridge_pred_val = ridge.predict(x_val)
        ridge_models[h] = ridge
        metric_rows.append(metrics_row(h, "ridge", y_val, ridge_pred_val))

        hgb = HistGradientBoostingRegressor(
            max_depth=8,
            learning_rate=0.06,
            max_iter=200,
            min_samples_leaf=15,
            l2_regularization=1e-3,
            random_state=random_seed,
        )
        hgb.fit(x_train, y_train)
        hgb_pred_val = hgb.predict(x_val)
        hgb_models[h] = hgb
        metric_rows.append(metrics_row(h, "hist_gradient_boosting", y_val, hgb_pred_val))

        preds_by_q: dict[float, np.ndarray] = {}
        for alpha in quantiles:
            lgb = _lgb_quantile_model(alpha, random_seed)
            lgb.fit(x_train_df, y_train)
            key = f"{h}h_alpha_{alpha}"
            lgb_models[key] = lgb
            preds_by_q[alpha] = lgb.predict(x_val_df)

        q10, q50, q90 = preds_by_q[0.1], preds_by_q[0.5], preds_by_q[0.9]
        metric_rows.append(
            metrics_row(
                h,
                "lightgbm_quantile",
                y_val,
                q50,
                q10=q10,
                q50=q50,
                q90=q90,
            ),
        )

        for i, ts in enumerate(val_df.index):
            pred_rows.append(
                {
                    "timestamp": ts.isoformat(),
                    "horizon_h": h,
                    "y_true": float(y_val[i]),
                    "persistence": float(pers_val[i]),
                    "hourly_median": float(hod_val[i]),
                    "ridge": float(ridge_pred_val[i]),
                    "hgb": float(hgb_pred_val[i]),
                    "lgb_q10": float(q10[i]),
                    "lgb_q50": float(q50[i]),
                    "lgb_q90": float(q90[i]),
                },
            )

    metrics = pd.DataFrame(metric_rows)
    predictions_validation = pd.DataFrame(pred_rows)

    point_candidates = metrics.loc[
        metrics["model"].isin(["ridge", "hist_gradient_boosting", "lightgbm_quantile"])
    ]
    best_point_model_name = str(point_candidates.groupby("model", sort=False)["rmse"].mean().idxmin())

    return ModelArtifacts(
        feature_columns=feature_columns,
        horizons=horizons,
        quantiles=quantiles,
        metrics=metrics,
        predictions_validation=predictions_validation,
        lgb_models=lgb_models,
        ridge_models=ridge_models,
        hgb_models=hgb_models,
        hourly_median_ghi=hourly_median_ghi,
        best_point_model_name=best_point_model_name,
    )
