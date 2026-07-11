from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from data_intelligence_engineering.catalog.project_registry import discover_project_records


DOCS_CATALOG = ROOT / "docs" / "catalog"
PROJECT_CATALOG = ROOT / "docs" / "project_catalog.md"


def _project_line(record, prefix: str = "../") -> str:
    rel = record.canonical_path.relative_to(ROOT).as_posix()
    tracks = ", ".join(record.tracks)
    domains = ", ".join(record.domain)
    return (
        f"- `{record.id}` [{record.title}]({prefix}{rel}/README.md) "
        f"- `{record.slug}`, `{record.difficulty}`, `{record.template}`, "
        f"tracks: {tracks}, domains: {domains}"
    )


def _grouped_page(title: str, grouped: dict[str, list]) -> str:
    lines = [f"# {title}", "", "Generated from `projects/*/project.yaml`.", ""]
    for key in sorted(grouped):
        lines.extend([f"## {key}", ""])
        lines.extend(_project_line(record, prefix="../../") for record in sorted(grouped[key], key=lambda item: item.id))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_catalogs() -> dict[Path, str]:
    records = discover_project_records()
    by_track: dict[str, list] = defaultdict(list)
    by_domain: dict[str, list] = defaultdict(list)
    by_difficulty: dict[str, list] = defaultdict(list)
    by_artifact: dict[str, list] = defaultdict(list)
    by_template: dict[str, list] = defaultdict(list)
    by_tool: dict[str, list] = defaultdict(list)

    for record in records:
        for track in record.tracks:
            by_track[track].append(record)
        for domain in record.domain:
            by_domain[domain].append(record)
        for artifact in record.artifacts:
            by_artifact[artifact].append(record)
        for skill in record.skills:
            by_tool[skill].append(record)
        by_difficulty[record.difficulty].append(record)
        by_template[record.template].append(record)

    master = [
        "# Project Catalog",
        "",
        "This catalog is generated from the 100 project metadata files under `projects/*/project.yaml`.",
        "",
        "Projects keep their slug-based physical paths for compatibility. Stable IDs `p001`-`p100` are canonical metadata aliases.",
        "",
        "## Projects",
        "",
    ]
    master.extend(_project_line(record) for record in sorted(records, key=lambda item: item.id))
    master.append("")

    return {
        PROJECT_CATALOG: "\n".join(master),
        DOCS_CATALOG / "by_track.md": _grouped_page("Projects By Track", by_track),
        DOCS_CATALOG / "by_domain.md": _grouped_page("Projects By Domain", by_domain),
        DOCS_CATALOG / "by_difficulty.md": _grouped_page("Projects By Difficulty", by_difficulty),
        DOCS_CATALOG / "by_artifact.md": _grouped_page("Projects By Artifact", by_artifact),
        DOCS_CATALOG / "by_tool.md": _grouped_page("Projects By Tool Or Skill", by_tool),
        DOCS_CATALOG / "by_template.md": _grouped_page("Projects By Template", by_template),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate metadata-backed project catalogs.")
    parser.add_argument("--check", action="store_true", help="Fail if generated catalog files are stale.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rendered = render_catalogs()
    stale: list[Path] = []
    for path, content in rendered.items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(path)
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    if stale:
        for path in stale:
            print(f"STALE {path.relative_to(ROOT)}")
        raise SystemExit(1)
    if args.check:
        print(f"Catalog check passed for {len(rendered)} files.")
    else:
        print(f"Generated {len(rendered)} catalog files.")


if __name__ == "__main__":
    main()
