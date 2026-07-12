from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from data_intelligence_engineering.catalog.project_registry import (
    FEATURED_PROJECTS,
    discover_project_records,
    registry_aliases,
    registry_by_id,
    registry_by_slug,
    resolve_project,
    validate_registry,
)


class ProjectRegistryTest(unittest.TestCase):
    def test_registry_discovers_existing_projects(self) -> None:
        records = discover_project_records()
        self.assertEqual(len(records), 100)

    def test_featured_projects_exist_in_registry(self) -> None:
        registry = registry_by_slug()
        for slug in FEATURED_PROJECTS:
            self.assertIn(slug, registry)

    def test_registry_resolves_ids_and_slugs(self) -> None:
        first = discover_project_records()[0]
        self.assertEqual(resolve_project(first.id), registry_by_id()[first.id])
        self.assertEqual(resolve_project(first.slug), registry_by_slug()[first.slug])
        aliases = registry_aliases()
        self.assertIs(aliases[first.id], aliases[first.slug])

    def test_project_metadata_is_complete_and_unique(self) -> None:
        result = validate_registry()
        self.assertTrue(result.ok)
        ids = {record.id for record in result.records}
        slugs = {record.slug for record in result.records}
        self.assertEqual(len(ids), 100)
        self.assertEqual(len(slugs), 100)
        self.assertTrue(all(record.tracks for record in result.records))
        self.assertTrue(any(record.learning_mission_ids for record in result.records))


if __name__ == "__main__":
    unittest.main()
