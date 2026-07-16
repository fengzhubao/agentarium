import codecs
import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from importlib import util
from importlib.machinery import SourceFileLoader
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ZH_SCRIPT = (
    ROOT
    / "skills"
    / "shared"
    / "agent-context-sync"
    / "zh_CN"
    / "scripts"
    / "sync_agent_context.py"
)
EN_SCRIPT = (
    ROOT
    / "skills"
    / "shared"
    / "agent-context-sync"
    / "en_US"
    / "scripts"
    / "sync_agent_context.py"
)
LOADER = SourceFileLoader("sync_agent_context", str(ZH_SCRIPT))
SPEC = util.spec_from_loader(LOADER.name, LOADER)
SYNC = util.module_from_spec(SPEC)
sys.modules[SPEC.name] = SYNC
LOADER.exec_module(SYNC)


class AgentContextSyncTests(unittest.TestCase):
    def make_repo(
        self,
        root: Path,
        *,
        source: str = "# Shared rules\n\n- Run tests.\n",
        targets: tuple[str, ...] = ("AGENTS.md", "CLAUDE.md"),
    ) -> None:
        (root / ".agent-context").mkdir(parents=True)
        (root / ".agent-context" / "shared.md").write_text(
            source, encoding="utf-8", newline=""
        )
        (root / ".agent-context-sync.json").write_text(
            json.dumps(
                {"source": ".agent-context/shared.md", "targets": list(targets)},
                indent=2,
            )
            + "\n",
            encoding="utf-8",
            newline="",
        )

    def run_main(self, root: Path, command: str, *extra: str):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = SYNC.main([command, "--repo-root", str(root), *extra])
        return code, stdout.getvalue(), stderr.getvalue()

    def test_locale_scripts_are_byte_identical(self):
        self.assertEqual(ZH_SCRIPT.read_bytes(), EN_SCRIPT.read_bytes())

    def test_check_reports_missing_targets_as_drift(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(root)

            code, stdout, stderr = self.run_main(root, "check")

        self.assertEqual(1, code)
        self.assertIn("DRIFT AGENTS.md: target missing", stdout)
        self.assertIn("2 drifted", stdout)
        self.assertEqual("", stderr)

    def test_sync_creates_missing_targets_and_check_becomes_clean(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(root)

            sync_code, sync_stdout, _ = self.run_main(root, "sync")
            check_code, check_stdout, _ = self.run_main(root, "check")

            agents = (root / "AGENTS.md").read_text(encoding="utf-8")

        self.assertEqual(0, sync_code)
        self.assertIn("UPDATED AGENTS.md", sync_stdout)
        self.assertEqual(0, check_code)
        self.assertIn("2 synced, 0 drifted", check_stdout)
        self.assertIn(SYNC.START_MARKER, agents)
        self.assertIn("- Run tests.", agents)

    def test_sync_appends_block_without_overwriting_tool_specific_content(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(root, targets=("AGENTS.md",))
            target = root / "AGENTS.md"
            target.write_text("# Codex-only rules\n\nKeep this section.\n", encoding="utf-8")

            code, _, _ = self.run_main(root, "sync")
            result = target.read_text(encoding="utf-8")

        self.assertEqual(0, code)
        self.assertTrue(result.startswith("# Codex-only rules\n\nKeep this section.\n"))
        self.assertEqual(1, result.count(SYNC.START_MARKER))

    def test_sync_replaces_only_existing_managed_block(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(root, source="New shared rule.\n", targets=("AGENTS.md",))
            target = root / "AGENTS.md"
            target.write_text(
                "Before\n"
                f"{SYNC.START_MARKER}\nOld shared rule.\n{SYNC.END_MARKER}\n"
                "After\n",
                encoding="utf-8",
            )

            code, _, _ = self.run_main(root, "sync")
            result = target.read_text(encoding="utf-8")

        self.assertEqual(0, code)
        self.assertEqual(
            "Before\n"
            f"{SYNC.START_MARKER}\nNew shared rule.\n{SYNC.END_MARKER}\n"
            "After\n",
            result,
        )

    def test_diff_is_read_only_and_uses_repository_relative_labels(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(root, targets=("AGENTS.md",))
            target = root / "AGENTS.md"
            target.write_text("Tool-only content.\n", encoding="utf-8")
            before = target.read_bytes()

            code, stdout, _ = self.run_main(root, "diff")
            after = target.read_bytes()

        self.assertEqual(1, code)
        self.assertIn("--- a/AGENTS.md", stdout)
        self.assertIn("+++ b/AGENTS.md", stdout)
        self.assertEqual(before, after)

    def test_cli_diff_emits_utf8_under_legacy_redirected_encoding(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(
                root,
                source="# Shared rules\n\n- ✅ Shipped.\n",
                targets=("AGENTS.md",),
            )
            environment = os.environ.copy()
            environment["PYTHONIOENCODING"] = "cp1252"

            completed = subprocess.run(
                [
                    sys.executable,
                    "-S",
                    str(ZH_SCRIPT),
                    "diff",
                    "--repo-root",
                    str(root),
                ],
                cwd=ROOT,
                env=environment,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )

        self.assertEqual(1, completed.returncode)
        self.assertIn("✅ Shipped.", completed.stdout.decode("utf-8"))
        self.assertEqual(b"", completed.stderr)

    def test_crlf_target_preserves_crlf_and_unmanaged_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(root, source="Shared A.\nShared B.\n", targets=("AGENTS.md",))
            target = root / "AGENTS.md"
            target.write_bytes(
                b"Windows-only\r\n\r\n"
                + SYNC.START_MARKER.encode()
                + b"\r\nOld\r\n"
                + SYNC.END_MARKER.encode()
                + b"\r\nTail\r\n"
            )

            code, _, _ = self.run_main(root, "sync")
            result = target.read_bytes()

        self.assertEqual(0, code)
        self.assertTrue(result.startswith(b"Windows-only\r\n\r\n"))
        self.assertTrue(result.endswith(b"\r\nTail\r\n"))
        self.assertNotIn(b"Shared A.\n", result.replace(b"\r\n", b""))
        self.assertIn(b"Shared A.\r\nShared B.", result)

    def test_utf8_bom_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(root, targets=("AGENTS.md",))
            target = root / "AGENTS.md"
            target.write_bytes(codecs.BOM_UTF8 + b"Existing\n")

            code, _, _ = self.run_main(root, "sync")
            result = target.read_bytes()

        self.assertEqual(0, code)
        self.assertTrue(result.startswith(codecs.BOM_UTF8))
        self.assertEqual(1, result.count(codecs.BOM_UTF8))

    def test_unmatched_marker_blocks_all_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(root)
            first = root / "AGENTS.md"
            second = root / "CLAUDE.md"
            first.write_text("First tool content.\n", encoding="utf-8")
            second.write_text(f"{SYNC.START_MARKER}\nBroken\n", encoding="utf-8")
            before = first.read_bytes()

            code, _, stderr = self.run_main(root, "sync")
            after = first.read_bytes()

        self.assertEqual(2, code)
        self.assertIn("unmatched managed-block marker", stderr)
        self.assertEqual(before, after)

    def test_duplicate_markers_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(root, targets=("AGENTS.md",))
            (root / "AGENTS.md").write_text(
                f"{SYNC.START_MARKER}\nA\n{SYNC.END_MARKER}\n"
                f"{SYNC.START_MARKER}\nB\n{SYNC.END_MARKER}\n",
                encoding="utf-8",
            )

            code, _, stderr = self.run_main(root, "check")

        self.assertEqual(2, code)
        self.assertIn("contains 2 copies", stderr)

    def test_source_cannot_contain_managed_markers(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(root, source=f"Unsafe\n{SYNC.START_MARKER}\n")

            code, _, stderr = self.run_main(root, "check")

        self.assertEqual(2, code)
        self.assertIn("source file must not contain", stderr)

    def test_parent_and_windows_absolute_paths_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(root)
            config = root / ".agent-context-sync.json"

            config.write_text(
                json.dumps({"source": "../shared.md", "targets": ["AGENTS.md"]}),
                encoding="utf-8",
            )
            parent_code, _, parent_error = self.run_main(root, "check")

            config.write_text(
                json.dumps(
                    {
                        "source": ".agent-context/shared.md",
                        "targets": ["C:" + "/Users/" + "demo/AGENTS.md"],
                    }
                ),
                encoding="utf-8",
            )
            windows_code, _, windows_error = self.run_main(root, "check")

        self.assertEqual(2, parent_code)
        self.assertIn("parent segments", parent_error)
        self.assertEqual(2, windows_code)
        self.assertIn("repository-relative", windows_error)

    def test_backslash_paths_are_portably_normalized(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(root, targets=("docs/AGENTS.md",))
            (root / ".agent-context-sync.json").write_text(
                json.dumps(
                    {
                        "source": ".agent-context\\shared.md",
                        "targets": ["docs\\AGENTS.md"],
                    }
                ),
                encoding="utf-8",
            )

            code, stdout, _ = self.run_main(root, "sync")
            target_exists = (root / "docs" / "AGENTS.md").is_file()

        self.assertEqual(0, code)
        self.assertIn("UPDATED docs/AGENTS.md", stdout)
        self.assertTrue(target_exists)

    def test_invalid_config_shape_and_unknown_fields_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.mkdir(exist_ok=True)
            config = root / ".agent-context-sync.json"
            config.write_text("[]\n", encoding="utf-8")
            shape_code, _, shape_error = self.run_main(root, "check")

            config.write_text(
                json.dumps(
                    {
                        "source": ".agent-context/shared.md",
                        "targets": ["AGENTS.md"],
                        "overwrite": True,
                    }
                ),
                encoding="utf-8",
            )
            unknown_code, _, unknown_error = self.run_main(root, "check")

        self.assertEqual(2, shape_code)
        self.assertIn("JSON object", shape_error)
        self.assertEqual(2, unknown_code)
        self.assertIn("unsupported fields", unknown_error)

    def test_duplicate_targets_are_rejected_case_insensitively(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(root)
            (root / ".agent-context-sync.json").write_text(
                json.dumps(
                    {
                        "source": ".agent-context/shared.md",
                        "targets": ["AGENTS.md", "agents.md"],
                    }
                ),
                encoding="utf-8",
            )

            code, _, stderr = self.run_main(root, "check")

        self.assertEqual(2, code)
        self.assertIn("targets must be unique", stderr)

    def test_config_file_cannot_be_a_target(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(root)
            (root / ".agent-context-sync.json").write_text(
                json.dumps(
                    {
                        "source": ".agent-context/shared.md",
                        "targets": [".agent-context-sync.json"],
                    }
                ),
                encoding="utf-8",
            )

            code, _, stderr = self.run_main(root, "sync")

        self.assertEqual(2, code)
        self.assertIn("config file must not also be listed", stderr)

    def test_sensitive_and_git_internal_paths_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(root)
            config = root / ".agent-context-sync.json"

            config.write_text(
                json.dumps(
                    {"source": ".agent-context/shared.md", "targets": [".env.local"]}
                ),
                encoding="utf-8",
            )
            sensitive_code, _, sensitive_error = self.run_main(root, "check")

            config.write_text(
                json.dumps(
                    {"source": ".agent-context/shared.md", "targets": [".git/info/agents"]}
                ),
                encoding="utf-8",
            )
            git_code, _, git_error = self.run_main(root, "check")

        self.assertEqual(2, sensitive_code)
        self.assertIn("forbidden sensitive filename", sensitive_error)
        self.assertEqual(2, git_code)
        self.assertIn("must not point inside .git", git_error)

    def test_custom_config_path_is_supported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".agent-context").mkdir()
            (root / ".agent-context" / "shared.md").write_text(
                "Shared.\n", encoding="utf-8"
            )
            (root / "config").mkdir()
            (root / "config" / "sync.json").write_text(
                json.dumps(
                    {"source": ".agent-context/shared.md", "targets": ["AGENTS.md"]}
                ),
                encoding="utf-8",
            )

            code, _, _ = self.run_main(root, "sync", "--config", "config/sync.json")
            target_exists = (root / "AGENTS.md").is_file()

        self.assertEqual(0, code)
        self.assertTrue(target_exists)


if __name__ == "__main__":
    unittest.main()
