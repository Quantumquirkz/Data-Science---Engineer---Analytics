from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import pandas as pd

from . import analytics, evaluation, simulation, visualization


@dataclass(slots=True)
class PipelineArtifacts:
    config: simulation.SimulationConfig
    metrics_df: pd.DataFrame
    reports_dir: Path
    summary_path: Path
    metrics_csv_path: Path
    figure_paths: dict[str, Path]


def _project_paths(project_root: Path) -> dict[str, Path]:
    processed = project_root / "data" / "processed"
    reports = processed / "reports"
    return {"processed_dir": processed, "reports_dir": reports}


def run_particle_diffusion_demo(
    project_root: Path,
    config: simulation.SimulationConfig | None = None,
) -> PipelineArtifacts:
    config = config or simulation.SimulationConfig()
    paths = _project_paths(project_root)
    paths["reports_dir"].mkdir(parents=True, exist_ok=True)

    times, paths_1d = simulation.simulate_bm_1d(config)
    endpoints_1d = paths_1d[:, -1]

    ks_d, ks_p = evaluation.ks_test_endpoint_1d(endpoints_1d, config.sigma, config.T)
    hist_l2 = evaluation.histogram_density_l2_error(endpoints_1d, config.sigma, config.T)
    msd_emp = evaluation.empirical_msd_1d(paths_1d, times)
    msd_th = analytics.msd_theory_1d(times, config.sigma)
    msd_rmse_1d = evaluation.msd_rmse(msd_emp, msd_th)

    rows: list[dict[str, object]] = [
        {"metric": "ks_statistic_1d_endpoint", "value": ks_d},
        {"metric": "ks_pvalue_1d_endpoint", "value": ks_p},
        {"metric": "histogram_l2_1d_endpoint", "value": hist_l2},
        {"metric": "msd_rmse_1d", "value": msd_rmse_1d},
    ]

    fig_paths: dict[str, Path] = {
        "paths_1d": paths["reports_dir"] / "fig_sample_paths_1d.png",
        "hist_1d": paths["reports_dir"] / "fig_histogram_endpoint_1d.png",
        "msd_1d": paths["reports_dir"] / "fig_msd_1d.png",
    }

    visualization.save_figure(
        visualization.plot_sample_paths_1d(times, paths_1d),
        fig_paths["paths_1d"],
    )
    visualization.save_figure(
        visualization.plot_histogram_vs_pdf_1d(endpoints_1d, config.sigma, config.T),
        fig_paths["hist_1d"],
    )
    visualization.save_figure(
        visualization.plot_msd_1d(times, msd_emp, config.sigma),
        fig_paths["msd_1d"],
    )

    if config.include_2d:
        _, paths_2d = simulation.simulate_bm_2d(config)
        radii = simulation.endpoint_radius_2d(paths_2d)
        ks_r, ks_pr = evaluation.ks_test_rayleigh_2d(radii, config.sigma, config.T)
        h_l2_r = evaluation.histogram_rayleigh_l2(radii, config.sigma, config.T)
        msd_emp_2 = evaluation.empirical_msd_2d(paths_2d, times)
        msd_th_2 = analytics.msd_theory_2d_squared_norm(times, config.sigma)
        msd_rmse_2d = evaluation.msd_rmse(msd_emp_2, msd_th_2)
        rows.extend(
            [
                {"metric": "ks_statistic_2d_rayleigh", "value": ks_r},
                {"metric": "ks_pvalue_2d_rayleigh", "value": ks_pr},
                {"metric": "histogram_l2_2d_rayleigh", "value": h_l2_r},
                {"metric": "msd_rmse_2d", "value": msd_rmse_2d},
            ]
        )
        fig_paths["msd_2d"] = paths["reports_dir"] / "fig_msd_2d.png"
        fig_paths["scatter_2d"] = paths["reports_dir"] / "fig_2d_endpoints_rayleigh.png"
        visualization.save_figure(
            visualization.plot_msd_2d(times, msd_emp_2, config.sigma),
            fig_paths["msd_2d"],
        )
        visualization.save_figure(
            visualization.plot_2d_endpoints_and_rayleigh(paths_2d, config.sigma, config.T),
            fig_paths["scatter_2d"],
        )

    metrics_df = pd.DataFrame(rows)
    metrics_csv_path = paths["reports_dir"] / "metrics_summary.csv"
    metrics_df.to_csv(metrics_csv_path, index=False)

    summary_payload = {
        "simulation": {k: (v if not isinstance(v, bool) else v) for k, v in asdict(config).items()},
        "figures": {k: str(v) for k, v in fig_paths.items()},
    }
    summary_path = paths["reports_dir"] / "run_summary.json"
    summary_path.write_text(json.dumps(summary_payload, indent=2), encoding="utf-8")

    return PipelineArtifacts(
        config=config,
        metrics_df=metrics_df,
        reports_dir=paths["reports_dir"],
        summary_path=summary_path,
        metrics_csv_path=metrics_csv_path,
        figure_paths=fig_paths,
    )
