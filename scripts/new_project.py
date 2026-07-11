from __future__ import annotations

import argparse
import re
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from data_intelligence_engineering.catalog.project_registry import discover_project_records


VALID_TEMPLATES = (
    "analytics_project",
    "data_science_project",
    "data_engineering_project",
    "ml_engineering_project",
    "scientific_computing_project",
    "capstone_project",
)


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def next_project_id() -> str:
    used = {int(record.id[1:]) for record in discover_project_records() if record.id.startswith("p") and record.id[1:].isdigit()}
    candidate = 1
    while candidate in used:
        candidate += 1
    return f"p{candidate:03d}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scaffold a new metadata-backed portfolio project.")
    parser.add_argument("title", help="Human-readable project title")
    parser.add_argument("--slug", help="Project slug. Defaults to a slugified title.")
    parser.add_argument("--template", choices=VALID_TEMPLATES, default="data_science_project")
    parser.add_argument("--summary", default="Applied learning project for reproducible data workflows.")
    parser.add_argument("--root", default="projects", help="Project root directory")
    return parser.parse_args()


def render_tokens(text: str, *, project_id: str, slug: str, title: str, summary: str) -> str:
    return (
        text.replace("{{ project_id }}", project_id)
        .replace("{{ slug }}", slug)
        .replace("{{ title }}", title)
        .replace("{{ summary }}", summary)
    )


def copy_template(template_root: Path, project_root: Path, *, project_id: str, slug: str, title: str, summary: str) -> None:
    for source in template_root.rglob("*"):
        relative = source.relative_to(template_root)
        target = project_root / relative
        if source.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        content = source.read_text(encoding="utf-8")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_tokens(content, project_id=project_id, slug=slug, title=title, summary=summary), encoding="utf-8")


def main() -> None:
    args = parse_args()
    slug = args.slug or slugify(args.title)
    project_root = ROOT / args.root / slug
    template_root = ROOT / "templates" / args.template
    if not template_root.exists():
        raise SystemExit(f"Unknown template directory: {template_root}")
    if project_root.exists():
        raise SystemExit(f"Refusing to overwrite existing project: {project_root}")
    project_id = next_project_id()
    copy_template(template_root, project_root, project_id=project_id, slug=slug, title=args.title, summary=args.summary)
    print(f"Created {project_id} at {project_root.relative_to(ROOT)} from {args.template}.")
    print("Run `PYTHONPATH=src:. python scripts/generate_project_catalog.py` after adding it to the registry.")


if __name__ == "__main__":
    main()
