from __future__ import annotations

from importlib import import_module
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from data_intelligence_engineering import FEATURED_PROJECTS
from data_intelligence_engineering.curriculum import discover_levels
from data_intelligence_engineering.curriculum import load_mission_registry


def _import_or_fail(module_name: str) -> None:
    import_module(module_name)


def main() -> None:
    _import_or_fail("data_intelligence_engineering")
    _import_or_fail("data_intelligence_engineering.curriculum")
    _import_or_fail("projects._portfolio_common")
    _import_or_fail("projects.sensor_drift_detection.src.pipeline")
    _import_or_fail("projects.gravitational_orbit_simulator.src.pipeline")
    _import_or_fail("projects.renewable_energy_mix_optimizer.src.pipeline")

    levels = discover_levels()
    missions = load_mission_registry()
    assert len(levels) == 50
    assert len(missions) == 50

    from projects.sensor_drift_detection.src.pipeline import run_sensor_drift_pipeline
    from projects.gravitational_orbit_simulator.src.pipeline import run_gravitational_orbit_simulator_pipeline
    from projects.renewable_energy_mix_optimizer.src.pipeline import run_renewable_energy_mix_optimizer_pipeline

    raw_df, windows_df, metrics_df, _ = run_sensor_drift_pipeline(window_size=40, step_size=20)
    assert not raw_df.empty and not windows_df.empty and not metrics_df.empty

    orbit = run_gravitational_orbit_simulator_pipeline(ROOT / "projects" / "gravitational_orbit_simulator", n_samples=240)
    renewable = run_renewable_energy_mix_optimizer_pipeline(ROOT / "projects" / "renewable_energy_mix_optimizer", n_samples=240)
    assert not orbit.model_result.metrics.empty
    assert not renewable.model_result.metrics.empty

    print(f"Smoke checks passed for: {', '.join(FEATURED_PROJECTS[:3])}; curriculum levels={len(levels)} missions={len(missions)}")


if __name__ == "__main__":
    main()
