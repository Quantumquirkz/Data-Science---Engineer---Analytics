"""Domain heuristics for organizing portfolio projects."""

from __future__ import annotations

DOMAIN_KEYWORDS: dict[str, tuple[str, ...]] = {
    "physical_systems": (
        "orbit",
        "gravitational",
        "plasma",
        "particle",
        "spectroscopy",
        "optical",
        "physics",
        "shockwave",
        "wave",
        "resonance",
    ),
    "environmental_systems": (
        "climate",
        "air_quality",
        "weather",
        "hydrological",
        "wildfire",
        "heat_island",
        "atmospheric",
        "flood",
        "satellite",
        "ocean",
        "seafloor",
        "environmental",
    ),
    "energy_systems": (
        "energy",
        "battery",
        "power_grid",
        "solar",
        "wind_turbine",
        "renewable",
        "smart_grid",
        "thermal",
    ),
    "finance_risk": (
        "financial",
        "portfolio",
        "trading",
        "pricing",
        "risk",
        "contagion",
        "regime",
        "volatility",
    ),
    "biology_health": (
        "protein",
        "blood",
        "epidemiological",
        "disease",
        "human",
        "gait",
        "biomechanics",
        "hospital",
        "neuron",
    ),
    "industrial_analytics": (
        "sensor",
        "manufacturing",
        "semiconductor",
        "defect",
        "industrial",
        "yield",
        "structural_health",
        "process_variation",
        "drift",
        "robotics",
    ),
    "large_scale_data": (
        "large_scale",
        "knowledge_graph",
        "platform",
        "metadata",
        "recommendation",
        "log_",
        "scientific_literature",
        "network_traffic",
        "experiment_metadata",
    ),
}


def infer_domain_group(slug: str) -> str:
    for domain_group, keywords in DOMAIN_KEYWORDS.items():
        if any(keyword in slug for keyword in keywords):
            return domain_group
    return "industrial_analytics"
