from pathlib import Path


def test_project_contract_files_exist():
    root = Path(__file__).resolve().parents[1]
    for relative in [
        "project.yaml",
        "README.md",
        "data/README.md",
        "notebooks",
        "src",
        "reports/README.md",
    ]:
        assert (root / relative).exists(), relative


def test_project_metadata_uses_slug_path():
    root = Path(__file__).resolve().parents[1]
    metadata = (root / "project.yaml").read_text(encoding="utf-8")
    assert "slug: portfolio_risk_stress_testing_engine" in metadata
    assert "projects/portfolio_risk_stress_testing_engine" in metadata
