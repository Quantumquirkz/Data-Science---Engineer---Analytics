from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from data_intelligence_engineering.catalog.project_registry import discover_project_records
from data_intelligence_engineering.catalog.project_registry import validate_registry
from data_intelligence_engineering.core.validation import validate_project_root

ALLOWED_TRACKS = {"data_analytics", "data_science", "data_engineering", "ml_engineering", "scientific_computing"}
ALLOWED_DIFFICULTIES = {"beginner", "intermediate", "advanced"}
ALLOWED_DOMAINS = {
    "physical_systems",
    "environmental_systems",
    "energy_systems",
    "finance_risk",
    "biology_health",
    "industrial_analytics",
    "large_scale_data",
}
ALLOWED_TEMPLATES = {
    "analytics_project",
    "data_science_project",
    "data_engineering_project",
    "ml_engineering_project",
    "scientific_computing_project",
    "capstone_project",
}
ALLOWED_MATURITY = {"featured", "active", "candidate", "archived"}
STRICT_PILOT_PROJECTS = {
    "sensor_drift_detection",
    "real_time_manufacturing_yield_dashboard",
    "scientific_data_platform_for_multi_modal_experiments",
    "large_scale_log_compression_and_analytics",
    "renewable_energy_mix_optimizer",
    "network_traffic_anomaly_detection",
    "gravitational_orbit_simulator",
    "particle_diffusion_mc",
    "portfolio_risk_stress_testing_engine",
    "satellite_image_change_detection",
}
STRICT_PILOT_REQUIRED = ("project.yaml", "tests", "reports/README.md")


def main() -> None:
    failures: list[str] = []
    registry_result = validate_registry()
    if registry_result.duplicate_ids:
        failures.append(f"duplicate project ids: {', '.join(registry_result.duplicate_ids)}")
    if registry_result.duplicate_slugs:
        failures.append(f"duplicate project slugs: {', '.join(registry_result.duplicate_slugs)}")
    if registry_result.missing_metadata:
        failures.append(f"missing project.yaml: {', '.join(registry_result.missing_metadata)}")

    for record in discover_project_records():
        missing = validate_project_root(record.canonical_path)
        if missing:
            failures.append(f"{record.slug}: missing {', '.join(missing)}")
        if not record.id.startswith("p") or len(record.id) != 4 or not record.id[1:].isdigit():
            failures.append(f"{record.slug}: invalid id {record.id}")
        if record.slug != record.canonical_path.name:
            failures.append(f"{record.slug}: slug does not match canonical path {record.canonical_path.name}")
        if not set(record.tracks).issubset(ALLOWED_TRACKS):
            failures.append(f"{record.slug}: invalid tracks {', '.join(record.tracks)}")
        if record.difficulty not in ALLOWED_DIFFICULTIES:
            failures.append(f"{record.slug}: invalid difficulty {record.difficulty}")
        if not set(record.domain).issubset(ALLOWED_DOMAINS):
            failures.append(f"{record.slug}: invalid domain {', '.join(record.domain)}")
        if record.template not in ALLOWED_TEMPLATES:
            failures.append(f"{record.slug}: invalid template {record.template}")
        if record.maturity not in ALLOWED_MATURITY:
            failures.append(f"{record.slug}: invalid maturity {record.maturity}")
        if not record.commands.get("run") or not record.commands.get("test"):
            failures.append(f"{record.slug}: missing run/test commands")
        if record.slug in STRICT_PILOT_PROJECTS:
            missing_pilot = [relative for relative in STRICT_PILOT_REQUIRED if not (record.canonical_path / relative).exists()]
            if missing_pilot:
                failures.append(f"{record.slug}: pilot missing {', '.join(missing_pilot)}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        raise SystemExit(1)
    print(f"Validated {len(discover_project_records())} project structures.")


if __name__ == "__main__":
    main()
