from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from data_intelligence_engineering.curriculum import projects_by_template, projects_by_track


class CurriculumIndexTest(unittest.TestCase):
    def test_projects_group_by_track(self) -> None:
        grouped = projects_by_track()
        self.assertIn("data_science", grouped)
        self.assertGreater(len(grouped["data_science"]), 0)

    def test_projects_group_by_template(self) -> None:
        grouped = projects_by_template()
        self.assertIn("data_science_project", grouped)
        self.assertGreater(len(grouped["data_science_project"]), 0)


if __name__ == "__main__":
    unittest.main()
