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
    assert "slug: large_scale_log_compression_and_analytics" in metadata
    assert "projects/large_scale_log_compression_and_analytics" in metadata
