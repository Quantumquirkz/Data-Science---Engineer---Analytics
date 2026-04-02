from __future__ import annotations

from pathlib import Path
import sys

import gradio as gr

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src import analytics, evaluation, simulation, visualization


def run_demo(sigma, T, n_steps, n_paths, include_2d):
    cfg = simulation.SimulationConfig(
        sigma=float(sigma),
        T=float(T),
        n_steps=int(n_steps),
        n_paths=int(n_paths),
        include_2d=bool(include_2d),
    )
    times, paths_1d = simulation.simulate_bm_1d(cfg)
    endpoints = paths_1d[:, -1]
    ks_d, ks_p = evaluation.ks_test_endpoint_1d(endpoints, cfg.sigma, cfg.T)
    hist_l2 = evaluation.histogram_density_l2_error(endpoints, cfg.sigma, cfg.T)
    msd_emp = evaluation.empirical_msd_1d(paths_1d, times)
    msd_th = analytics.msd_theory_1d(times, cfg.sigma)
    rmse_1d = evaluation.msd_rmse(msd_emp, msd_th)

    lines = [
        "1D endpoint KS: D=%.4f, p=%.4f" % (ks_d, ks_p),
        "1D histogram L2 vs Gaussian: %.4f" % hist_l2,
        "1D MSD RMSE vs sigma^2 t: %.4f" % rmse_1d,
    ]
    if include_2d:
        _, paths_2d = simulation.simulate_bm_2d(cfg)
        radii = simulation.endpoint_radius_2d(paths_2d)
        ks_r, ks_pr = evaluation.ks_test_rayleigh_2d(radii, cfg.sigma, cfg.T)
        h2 = evaluation.histogram_rayleigh_l2(radii, cfg.sigma, cfg.T)
        m2e = evaluation.empirical_msd_2d(paths_2d, times)
        m2t = analytics.msd_theory_2d_squared_norm(times, cfg.sigma)
        rmse_2d = evaluation.msd_rmse(m2e, m2t)
        lines.append("2D Rayleigh KS: D=%.4f, p=%.4f" % (ks_r, ks_pr))
        lines.append("2D radial histogram L2: %.4f" % h2)
        lines.append("2D MSD RMSE vs 2 sigma^2 t: %.4f" % rmse_2d)
        fig_2d = visualization.plot_2d_endpoints_and_rayleigh(paths_2d, cfg.sigma, cfg.T)
        fig_msd2 = visualization.plot_msd_2d(times, m2e, cfg.sigma)
    else:
        fig_2d = None
        fig_msd2 = None

    fig_paths = visualization.plot_sample_paths_1d(times, paths_1d)
    fig_hist = visualization.plot_histogram_vs_pdf_1d(endpoints, cfg.sigma, cfg.T)
    fig_msd1 = visualization.plot_msd_1d(times, msd_emp, cfg.sigma)
    return "\n".join(lines), fig_paths, fig_hist, fig_msd1, fig_msd2, fig_2d


with gr.Blocks(title="Particle Diffusion MC") as demo:
    gr.Markdown("# Brownian motion vs diffusion kernel")
    sigma = gr.Slider(0.2, 2.0, value=1.0, step=0.05, label="sigma (dX = sigma dW)")
    T = gr.Slider(0.2, 3.0, value=1.0, step=0.1, label="Horizon T")
    n_steps = gr.Slider(50, 2000, value=300, step=50, label="Time steps")
    n_paths = gr.Slider(500, 15000, value=3000, step=500, label="Paths")
    include_2d = gr.Checkbox(value=True, label="Include 2D Rayleigh diagnostics")
    btn = gr.Button("Run", variant="primary")
    out_text = gr.Textbox(label="Metrics", lines=6)
    p1 = gr.Plot(label="Sample paths 1D")
    p2 = gr.Plot(label="Endpoint vs Gaussian")
    p3 = gr.Plot(label="MSD 1D")
    p4 = gr.Plot(label="MSD 2D")
    p5 = gr.Plot(label="2D endpoints and Rayleigh")
    btn.click(
        fn=run_demo,
        inputs=[sigma, T, n_steps, n_paths, include_2d],
        outputs=[out_text, p1, p2, p3, p4, p5],
    )

if __name__ == "__main__":
    demo.launch()
