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

from data_intelligence_engineering.catalog.schemas import ProjectSpec
from projects._portfolio_common import PipelineArtifacts, run_portfolio_pipeline
from projects._portfolio_common.spec import ProjectSpec as CompatProjectSpec


class PortfolioCommonCompatTest(unittest.TestCase):
    def test_project_spec_reexport(self) -> None:
        self.assertIs(ProjectSpec, CompatProjectSpec)

    def test_pipeline_exports_exist(self) -> None:
        self.assertTrue(callable(run_portfolio_pipeline))
        self.assertEqual(PipelineArtifacts.__name__, "PipelineArtifacts")


if __name__ == "__main__":
    unittest.main()
