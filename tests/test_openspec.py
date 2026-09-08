"""Real OpenSpec CLI integration in temporary projects; no model or private input."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class OpenSpecIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        node = shutil.which("node")
        shim = shutil.which("openspec.cmd") or shutil.which("openspec")
        if not node or not shim:
            raise unittest.SkipTest("OpenSpec CLI and Node are required for integration tests")
        if os.name == "nt":
            entry = Path(shim).parent / "node_modules/@fission-ai/openspec/bin/openspec.js"
        else:
            entry = Path(shim).resolve()
        if not entry.is_file():
            raise unittest.SkipTest("Cannot locate installed OpenSpec entrypoint")
        cls.cli = [node, str(entry)]

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="research_openspec_")
        self.addCleanup(self.temporary.cleanup)
        self.project = Path(self.temporary.name).resolve()
        shutil.copytree(ROOT / "openspec/schemas", self.project / "openspec/schemas")
        (self.project / "openspec/config.yaml").write_text(
            "schema: research-task\ncontext: |\n  Authority: accepted_science.md\n",
            encoding="utf-8",
        )
        self.env = dict(os.environ, OPENSPEC_TELEMETRY="0", DO_NOT_TRACK="1", CI="1")
        # Prevent a user's default store from redirecting the temporary project.
        self.env["APPDATA"] = str(self.project / "user_config")
        self.env["XDG_CONFIG_HOME"] = str(self.project / "user_config")
        self.run_cli("new", "change", "test-research-task")
        self.change = self.project / "openspec/changes/test-research-task"

    def run_cli(self, *args, expect_success=True):
        result = subprocess.run(
            self.cli + list(args), cwd=self.project, env=self.env,
            capture_output=True, text=True, encoding="utf-8", timeout=30,
        )
        if expect_success:
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        else:
            self.assertNotEqual(result.returncode, 0, result.stderr + result.stdout)
        return result

    def instructions(self):
        return json.loads(self.run_cli(
            "instructions", "apply", "--change", "test-research-task", "--json"
        ).stdout)

    def write_tasks(self, completed=False):
        mark = "x" if completed else " "
        (self.change / "tasks.md").write_text(
            "# Work package\n\nSource: accepted_science.md\n\n"
            f"- [{mark}] 1.1 Check the source remains unchanged; compare its bytes.\n",
            encoding="utf-8",
        )

    def test_schema_and_context_resolve_from_project(self):
        self.run_cli("schema", "validate", "research-task")
        result = json.loads(self.run_cli(
            "instructions", "tasks", "--change", "test-research-task", "--json"
        ).stdout)
        self.assertEqual(result["schemaName"], "research-task")
        self.assertEqual(Path(result["resolvedOutputPath"]), self.change / "tasks.md")
        self.assertEqual(result["context"].strip(), "Authority: accepted_science.md")
        self.assertEqual(result["dependencies"], [])

    def test_missing_pending_and_completed_tasks_are_distinct(self):
        self.assertEqual(self.instructions()["state"], "blocked")
        self.write_tasks()
        pending = self.instructions()
        self.assertEqual(pending["state"], "ready")
        self.assertEqual(pending["progress"], {"total": 1, "complete": 0, "remaining": 1})
        self.assertEqual(set(pending["contextFiles"]), {"tasks"})
        status = json.loads(self.run_cli(
            "status", "--change", "test-research-task", "--json"
        ).stdout)
        # Artifact completeness must not be reported as accepted implementation.
        self.assertTrue(status["isComplete"])
        self.assertEqual(pending["progress"]["complete"], 0)
        self.write_tasks(completed=True)
        self.assertEqual(self.instructions()["state"], "all_done")

    def test_archive_preserves_linked_scientific_source(self):
        source = self.project / "accepted_science.md"
        original = b"Unknown observations remain distinct from negative observations.\n"
        source.write_bytes(original)
        self.write_tasks(completed=True)
        self.run_cli("validate", "test-research-task", "--strict", "--no-interactive")
        self.run_cli("archive", "test-research-task", "--json")
        self.assertEqual(source.read_bytes(), original)
        self.assertFalse(self.change.exists())
        archives = list((self.project / "openspec/changes/archive").glob("*-test-research-task/tasks.md"))
        self.assertEqual(len(archives), 1)
        self.assertEqual(list((self.project / "openspec/specs").rglob("*.md")), [])

    def test_missing_template_fails_visibly(self):
        template = self.project / "openspec/schemas/research-task/templates/tasks.md"
        template.unlink()
        self.run_cli("schema", "validate", "research-task", expect_success=False)


if __name__ == "__main__":
    unittest.main()
