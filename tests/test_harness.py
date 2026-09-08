"""Exercise staging/data-boundary failures without touching live installations."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location(
    "harness", Path(__file__).resolve().parents[1] / "scripts/harness.py")
harness = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(harness)


class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.sandbox = tempfile.TemporaryDirectory()
        self.addCleanup(self.sandbox.cleanup)
        self.base = Path(self.sandbox.name)
        self.repo = self.base / "repo"
        skill = self.repo / "skills/research-agent"
        (skill / "references").mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            "---\nname: research-agent\ndescription: Research entry.\n---\nBody.\n", encoding="utf-8")
        (skill / "references/copilot-regression.json").write_text(
            json.dumps({"cases": [{"case_id": "sample", "expected_owner": "research-agent"}]}),
            encoding="utf-8")

    def test_valid_source_does_not_claim_behavioral_execution(self):
        result = harness.validate(self.repo)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["behavioral_evaluations_executed"], 0)

    def test_missing_owner_is_rejected(self):
        path = self.repo / "skills/research-agent/references/copilot-regression.json"
        path.write_text(json.dumps({"cases": [{"case_id": "bad", "expected_owner": "missing"}]}))
        self.assertIn("Missing route owner", " ".join(harness.validate(self.repo)["errors"]))

    def test_secret_scan_reports_locator_without_secret(self):
        fake = "ghp_" + "X" * 36
        (self.repo / "example.txt").write_text(fake)
        result = harness.validate(self.repo)
        self.assertEqual(result["status"], "FAIL")
        self.assertNotIn(fake, json.dumps(result))
        self.assertIn("example.txt:1", json.dumps(result))

    def test_invalid_python_is_rejected(self):
        (self.repo / "bad.py").write_text("def broken(:\n")
        self.assertEqual(harness.validate(self.repo)["status"], "FAIL")

    def test_malformed_regression_pack_returns_visible_failure(self):
        path = self.repo / "skills/research-agent/references/copilot-regression.json"
        path.write_text("{broken")
        result = harness.validate(self.repo)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("JSON syntax", " ".join(result["errors"]))

    def test_stage_preserves_source_and_copies_exact_content(self):
        source = self.repo / "skills/research-agent/SKILL.md"
        before = source.read_bytes()
        target = self.base / "trial"
        result = harness.stage(target, ["research-agent"], self.repo)
        self.assertFalse(result["live_installation_changed"])
        self.assertEqual(before, source.read_bytes())
        self.assertEqual(before, (target / "research-agent/SKILL.md").read_bytes())

    def test_existing_target_is_never_overwritten(self):
        target = self.base / "existing"
        target.mkdir()
        sentinel = target / "work.txt"
        sentinel.write_text("user work")
        with self.assertRaises(ValueError):
            harness.stage(target, ["research-agent"], self.repo)
        self.assertEqual(sentinel.read_text(), "user work")
        self.assertEqual(list(target.iterdir()), [sentinel])

    def test_unknown_skill_fails_before_target_creation(self):
        target = self.base / "trial"
        with self.assertRaises(ValueError):
            harness.stage(target, ["research-agent", "missing"], self.repo)
        self.assertFalse(target.exists())

    def test_live_discovery_path_is_refused(self):
        target = self.base / ".agents/skills"
        with self.assertRaises(ValueError):
            harness.stage(target, ["research-agent"], self.repo)
        self.assertFalse(target.exists())

    def test_private_fixture_is_marked_unexecuted(self):
        path = self.repo / "skills/research-agent/references/copilot-regression.json"
        path.write_text(json.dumps({"cases": [{"case_id": "private", "fixture": {"path": "private.txt"}}]}))
        self.assertEqual(harness.validate(self.repo)["private_fixture_cases_not_executed"], ["private"])


if __name__ == "__main__":
    unittest.main()
