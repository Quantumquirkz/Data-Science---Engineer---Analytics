from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


class SmokeTargetsTest(unittest.TestCase):
    def test_featured_pipeline_entrypoints(self) -> None:
        from projects.sensor_drift_detection.src.pipeline import run_sensor_drift_pipeline
        from projects.gravitational_orbit_simulator.src.pipeline import run_gravitational_orbit_simulator_pipeline
        from projects.renewable_energy_mix_optimizer.src.pipeline import run_renewable_energy_mix_optimizer_pipeline

        raw_df, windows_df, metrics_df, _ = run_sensor_drift_pipeline(window_size=40, step_size=20)
        self.assertFalse(raw_df.empty)
        self.assertFalse(windows_df.empty)
        self.assertFalse(metrics_df.empty)

        orbit = run_gravitational_orbit_simulator_pipeline(ROOT / "projects" / "gravitational_orbit_simulator", n_samples=240)
        renewable = run_renewable_energy_mix_optimizer_pipeline(ROOT / "projects" / "renewable_energy_mix_optimizer", n_samples=240)
        self.assertFalse(orbit.model_result.metrics.empty)
        self.assertFalse(renewable.model_result.metrics.empty)


if __name__ == "__main__":
    unittest.main()
