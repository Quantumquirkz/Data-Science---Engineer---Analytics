# Particle Diffusion Monte Carlo Simulator

Monte Carlo simulation of **Brownian motion** and comparison of empirical distributions with the **analytical solution** of the diffusion (heat) equation.

**1D:** \(dX_t = \sigma\, dW_t\), \(X_0 = 0\). At time \(T\), \(X_T \sim \mathcal{N}(0, \sigma^2 T)\), matching the fundamental solution of \(u_t = \frac{\sigma^2}{2} u_{xx}\) with initial data \(\delta_0\).

**2D (optional):** isotropic \(\mathrm{d}\mathbf{X}_t = \sigma\, \mathrm{d}\mathbf{W}_t\). The endpoint radius \(R_T = \|\mathbf{X}_T\|\) follows a **Rayleigh** law with scale \(\sigma\sqrt{T}\).

## Layout

- `src/simulation.py` — exact-increment Brownian paths (1D / 2D)
- `src/analytics.py` — theoretical PDFs, MSD
- `src/evaluation.py` — Kolmogorov–Smirnov, histogram \(L^2\) vs PDF, MSD curve error
- `src/visualization.py` — matplotlib figures
- `src/pipeline.py` — `run_particle_diffusion_demo`
- `app.py` — Gradio UI
- `notebooks/particle_diffusion_mc.ipynb` — SDE / PDE narrative

## Run (repository root)

```bash
uv run python -c "from pathlib import Path; from labs.particle_diffusion_mc.src.pipeline import run_particle_diffusion_demo; a = run_particle_diffusion_demo(Path('labs/particle_diffusion_mc')); print(a.metrics_df.to_string(index=False))"
```

Gradio:

```bash
uv run python labs/particle_diffusion_mc/app.py
```

## Suggested extensions

- Drift (Brownian with drift, Ornstein–Uhlenbeck)
- Boundaries (reflection / absorption, method of images)
- Convergence study vs `n_paths`
