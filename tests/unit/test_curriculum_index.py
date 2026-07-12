from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from data_intelligence_engineering.curriculum import TRACKS
from data_intelligence_engineering.curriculum import discover_levels
from data_intelligence_engineering.curriculum import levels_by_track
from data_intelligence_engineering.curriculum import load_mission_registry
from data_intelligence_engineering.curriculum import projects_by_template
from data_intelligence_engineering.curriculum import projects_by_track
from data_intelligence_engineering.curriculum import validate_curriculum


class CurriculumIndexTest(unittest.TestCase):
    def test_projects_group_by_track(self) -> None:
        grouped = projects_by_track()
        self.assertIn("data_science", grouped)
        self.assertGreater(len(grouped["data_science"]), 0)

    def test_projects_group_by_template(self) -> None:
        grouped = projects_by_template()
        self.assertIn("data_science_project", grouped)
        self.assertGreater(len(grouped["data_science_project"]), 0)

    def test_curriculum_levels_cover_all_tracks(self) -> None:
        grouped = levels_by_track()
        self.assertEqual(set(grouped), set(TRACKS))
        self.assertTrue(all(len(grouped[track]) == 10 for track in TRACKS))

    def test_curriculum_missions_and_notebooks_exist(self) -> None:
        missions = load_mission_registry()
        self.assertEqual(len(missions), 50)
        levels = discover_levels()
        self.assertEqual(len(levels), 50)
        implemented = [record for record in levels if record.status == "implemented"]
        self.assertEqual(len(implemented), 50)
        for record in levels:
            self.assertEqual(len(record.notebook_paths), 1)
            for notebook in record.notebook_paths:
                self.assertTrue(notebook.exists(), notebook)
        for mission in missions:
            self.assertIsNotNone(mission.notebook_path)
            self.assertIsNotNone(mission.command)

    def test_curriculum_validation_passes(self) -> None:
        self.assertEqual(validate_curriculum(), ())


if __name__ == "__main__":
    unittest.main()
