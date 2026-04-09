from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from lightgbm import LGBMRegressor
from scipy.optimize import minimize
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.statespace.sarimax import SARIMAX

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
    hourly_dow_median: pd.Series
    best_point_model_name: str
    ensemble_weights: dict[int, np.ndarray]
    ensemble_component_names: dict[int, tuple[str, ...]]
    sarimax_forecast_validation: pd.Series | None
    sarimax_fitted: bool


SARIMAX_EXOG_COLS = ("temperature_c", "is_holiday", "hour_sin", "hour_cos")


def _lgb_quantile_model(alpha: float, random_seed: int) -> LGBMRegressor:
    return LGBMRegressor(
        objective="quantile",
        alpha=alpha,
        n_estimators=300,
        learning_rate=0.05,
        max_depth=-1,
        num_leaves=64,
        subsample=0.85,
        colsample_bytree=0.85,
        reg_lambda=1.0,
        min_child_samples=25,
        random_state=random_seed,
        n_jobs=1,
        verbose=-1,
    )


def _fit_sarimax_validation_forecast(
    train_df: pd.DataFrame,
    val_df: pd.DataFrame,
    max_train_hours: int = 8_760,
) -> pd.Series | None:
    """Fixed-origin multi-step forecast of actual load during validation (exog known)."""
    exog_cols = [c for c in SARIMAX_EXOG_COLS if c in train_df.columns]
    if len(exog_cols) < len(SARIMAX_EXOG_COLS):
        return None
    train_slice = train_df
    if len(train_df) > max_train_hours:
        train_slice = train_df.iloc[-max_train_hours:]
    y_train = np.log1p(train_slice["load_mw"].astype(float).to_numpy())
    ex_train = train_slice[list(SARIMAX_EXOG_COLS)].astype(float).to_numpy()
    ex_val = val_df[list(SARIMAX_EXOG_COLS)].astype(float).to_numpy()
    try:
        mod = SARIMAX(
            y_train,
            exog=ex_train,
            order=(1, 1, 1),
            seasonal_order=(0, 0, 0, 0),
            enforce_stationarity=False,
            enforce_invertibility=False,
        )
        res = mod.fit(disp=False, maxiter=80)
        fc = res.get_forecast(steps=len(val_df), exog=ex_val)
        pred = np.expm1(np.asarray(fc.predicted_mean, dtype=float))
        return pd.Series(pred, index=val_df.index, name="sarimax_load_hat")
    except Exception:
        return None


def _solve_ensemble_weights(y: np.ndarray, preds: np.ndarray) -> np.ndarray:
    """Nonnegative weights summing to 1 minimizing mean squared error."""
    n, k = preds.shape
    if k == 0 or n == 0:
        return np.array([])

    def mse(w: np.ndarray) -> float:
        wn = np.maximum(w, 0.0)
        s = float(wn.sum())
        if s < 1e-15:
            return 1e18
        wn = wn / s
        err = y - preds @ wn
        return float(np.mean(err**2))

    w0 = np.full(k, 1.0 / k)
    res = minimize(mse, w0, method="Powell", options={"maxiter": 2000})
    wn = np.maximum(res.x, 0.0)
    s = float(wn.sum())
    if s < 1e-15:
        return w0
    return wn / s


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

    local_train = train_df.index.tz_convert("Europe/Berlin")
    hourly_dow_median = train_df.groupby([local_train.hour, local_train.dayofweek])[
        "load_mw"
    ].median()

    def dow_hour_median_vector(df: pd.DataFrame) -> np.ndarray:
        loc = df.index.tz_convert("Europe/Berlin")
        multi_idx = pd.MultiIndex.from_arrays([loc.hour, loc.dayofweek])
        return hourly_dow_median.reindex(multi_idx).to_numpy(dtype=float)

    sarimax_series = _fit_sarimax_validation_forecast(train_df, val_df)
    val_actual_load = val_df["load_mw"].astype(float).to_numpy()
    if sarimax_series is not None:
        sarimax_aligned = sarimax_series.reindex(val_df.index).astype(float).to_numpy()
    else:
        sarimax_aligned = np.full(len(val_df), np.nan)

    lgb_models: dict[str, LGBMRegressor] = {}
    ridge_models: dict[int, Pipeline] = {}
    hgb_models: dict[int, HistGradientBoostingRegressor] = {}

    metric_rows: list[dict[str, object]] = []
    pred_rows: list[dict[str, object]] = []

    x_train_df = train_df[feature_columns]
    x_val_df = val_df[feature_columns]
    x_train = x_train_df.to_numpy(dtype=np.float64)
    x_val = x_val_df.to_numpy(dtype=np.float64)

    if sarimax_series is not None and np.all(np.isfinite(sarimax_aligned)):
        metric_rows.append(
            metrics_row(0, "sarimax_multi_fixed_origin", val_actual_load, sarimax_aligned),
        )

    ensemble_weights: dict[int, np.ndarray] = {}
    ensemble_names: dict[int, tuple[str, ...]] = {}

    for h in horizons:
        target_col = f"target_load_{h}h"
        y_train = train_df[target_col].to_numpy(dtype=np.float64)
        y_val = val_df[target_col].to_numpy(dtype=np.float64)

        if h == 24:
            naive_val = val_df["load_mw"].to_numpy(dtype=np.float64)
        else:
            col = f"load_lag_{h}h"
            if col not in val_df.columns:
                naive_val = val_df["load_mw"].shift(h).to_numpy(dtype=np.float64)
            else:
                naive_val = val_df[col].to_numpy(dtype=np.float64)

        hod_val = dow_hour_median_vector(val_df)
        hod_val = np.nan_to_num(hod_val, nan=np.nanmedian(hod_val))

        metric_rows.append(metrics_row(h, "naive_calendar", y_val, naive_val))
        metric_rows.append(metrics_row(h, "hour_dow_median_train", y_val, hod_val))

        ridge = Pipeline(
            steps=[
                ("scaler", StandardScaler()),
                ("ridge", Ridge(alpha=5.0, random_state=random_seed)),
            ]
        )
        ridge.fit(x_train, y_train)
        ridge_pred_val = ridge.predict(x_val)
        ridge_models[h] = ridge
        metric_rows.append(metrics_row(h, "ridge", y_val, ridge_pred_val))

        hgb = HistGradientBoostingRegressor(
            max_depth=10,
            learning_rate=0.06,
            max_iter=220,
            min_samples_leaf=20,
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

        comp_arrays = [naive_val, hod_val, ridge_pred_val, hgb_pred_val, q50]
        comp_names = ("naive_calendar", "hour_dow_median", "ridge", "hgb", "lgb_q50")
        P = np.column_stack(comp_arrays)
        w = _solve_ensemble_weights(y_val, P)
        ensemble_pred = P @ w
        ensemble_weights[h] = w
        ensemble_names[h] = comp_names
        metric_rows.append(metrics_row(h, "ensemble_nonneg_weights", y_val, ensemble_pred))

        for i, ts in enumerate(val_df.index):
            row: dict[str, object] = {
                "timestamp": ts.isoformat(),
                "horizon_h": h,
                "y_true": float(y_val[i]),
                "naive_calendar": float(naive_val[i]),
                "hour_dow_median": float(hod_val[i]),
                "ridge": float(ridge_pred_val[i]),
                "hgb": float(hgb_pred_val[i]),
                "lgb_q10": float(q10[i]),
                "lgb_q50": float(q50[i]),
                "lgb_q90": float(q90[i]),
                "ensemble_opt": float(ensemble_pred[i]),
            }
            if np.isfinite(sarimax_aligned[i]):
                row["sarimax_fixed_origin_load"] = float(sarimax_aligned[i])
            else:
                row["sarimax_fixed_origin_load"] = None
            pred_rows.append(row)

    metrics = pd.DataFrame(metric_rows)
    predictions_validation = pd.DataFrame(pred_rows)

    point_candidates = metrics.loc[
        metrics["model"].isin(["ridge", "hist_gradient_boosting", "lightgbm_quantile", "ensemble_nonneg_weights"])
        & (metrics["horizon_h"] > 0)
    ]
    if point_candidates.empty:
        best_point_model_name = "ridge"
    else:
        best_point_model_name = str(
            point_candidates.groupby("model", sort=False)["rmse"].mean().idxmin()
        )

    return ModelArtifacts(
        feature_columns=feature_columns,
        horizons=horizons,
        quantiles=quantiles,
        metrics=metrics,
        predictions_validation=predictions_validation,
        lgb_models=lgb_models,
        ridge_models=ridge_models,
        hgb_models=hgb_models,
        hourly_dow_median=hourly_dow_median,
        best_point_model_name=best_point_model_name,
        ensemble_weights=ensemble_weights,
        ensemble_component_names=ensemble_names,
        sarimax_forecast_validation=sarimax_series,
        sarimax_fitted=sarimax_series is not None,
    )
