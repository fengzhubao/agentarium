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
    / "skill-quality-auditor"
    / "zh_CN"
    / "scripts"
    / "validate_agentarium.py"
)
EN_SCRIPT = (
    ROOT
    / "skills"
    / "shared"
    / "skill-quality-auditor"
    / "en_US"
    / "scripts"
    / "validate_agentarium.py"
)
LOADER = SourceFileLoader("validate_agentarium", str(ZH_SCRIPT))
SPEC = util.spec_from_loader(LOADER.name, LOADER)
VALIDATOR = util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
LOADER.exec_module(VALIDATOR)


class AgentariumValidatorTests(unittest.TestCase):
    def test_catalog_parser_supports_inline_unquoted_lists(self):
        catalog = VALIDATOR.parse_catalog_yaml(
            "schema_version: 2\nrequired_locales: [zh_CN, en_US]\n"
        )

        self.assertEqual(["zh_CN", "en_US"], catalog["required_locales"])

    def test_catalog_parser_handles_quoted_colons_and_inline_comments(self):
        catalog = VALIDATOR.parse_catalog_yaml(
            "scope: shared # portable workflow\n"
            "summary: 'It''s portable'\n"
            'items:\n  - "Agents: with file access"\n'
        )

        self.assertEqual("shared", catalog["scope"])
        self.assertEqual("It's portable", catalog["summary"])
        self.assertEqual(["Agents: with file access"], catalog["items"])

    def test_catalog_parser_handles_nested_first_list_field(self):
        catalog = VALIDATOR.parse_catalog_yaml(
            "items:\n"
            "  - nested:\n"
            "      key: value\n"
            "    other: x\n"
        )

        self.assertEqual(
            [{"nested": {"key": "value"}, "other": "x"}],
            catalog["items"],
        )

    def test_malformed_catalog_types_return_findings_instead_of_crashing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            governance = [
                "AGENTS.md",
                "README.md",
                "catalog/status-policy.md",
                "docs/importing.md",
                "docs/publishing.md",
                "docs/localization.md",
                "docs/safety.md",
                "docs/skill-completeness.md",
            ]
            for relative in governance:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("fixture\n", encoding="utf-8")
            catalog_path = root / "catalog" / "skills.yaml"
            catalog_path.write_text(
                "schema_version: 2\n"
                "required_locales: [zh_CN, en_US]\n"
                "tool_families: [shared, trae, claude, codex]\n"
                "skills:\n"
                "  - id: []\n"
                "    slug: []\n"
                "    title: []\n"
                "    category: quality\n"
                "    scope: []\n"
                "    status: []\n"
                "    summary_zh: fixture\n"
                "    summary_en: fixture\n"
                "    model_fit: {}\n"
                "    supported_tools: []\n"
                "    target_tools: [shared]\n"
                "    required_locales: [zh_CN, en_US]\n"
                "    variants: []\n"
                "    tags: []\n",
                encoding="utf-8",
            )

            report = VALIDATOR.validate_repository(root)

        codes = {finding.code for finding in report.errors}
        self.assertIn("invalid-id", codes)
        self.assertIn("scope", codes)
        self.assertIn("invalid-status", codes)

    def test_extra_draft_locale_does_not_lower_required_locale_aggregation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            governance = [
                "AGENTS.md",
                "README.md",
                "catalog/status-policy.md",
                "docs/importing.md",
                "docs/publishing.md",
                "docs/localization.md",
                "docs/safety.md",
                "docs/skill-completeness.md",
            ]
            for relative in governance:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("fixture\n", encoding="utf-8")
            package = root / "skills" / "shared" / "demo-skill"
            package.mkdir(parents=True)
            (package / "README.md").write_text("# Demo\n", encoding="utf-8")
            (package / "STATUS.md").write_text("# Status\n", encoding="utf-8")
            for locale in ("zh_CN", "en_US", "ja_JP"):
                locale_root = package / locale
                locale_root.mkdir()
                (locale_root / "SKILL.md").write_text(
                    "---\n"
                    "name: demo-skill\n"
                    "description: Fixture Skill.\n"
                    "---\n\n"
                    "# Demo\n",
                    encoding="utf-8",
                )
            for locale in ("zh_CN", "en_US"):
                examples = root / "examples" / "shared" / "demo-skill" / locale
                examples.mkdir(parents=True)
                (examples / "sample-input.md").write_text("input\n", encoding="utf-8")
                (examples / "sample-output.md").write_text("output\n", encoding="utf-8")
            catalog_path = root / "catalog" / "skills.yaml"
            catalog_path.write_text(
                "schema_version: 2\n"
                "required_locales: [zh_CN, en_US]\n"
                "tool_families: [shared, trae, claude, codex]\n"
                "skills:\n"
                "  - id: SKL-0001\n"
                "    slug: demo-skill\n"
                "    title: Demo Skill\n"
                "    category: quality\n"
                "    scope: shared\n"
                "    status: sampled\n"
                "    summary_zh: fixture\n"
                "    summary_en: fixture\n"
                "    model_fit:\n"
                "      suitable_for: [repository agents]\n"
                "      not_suitable_for: [chat only]\n"
                "    supported_tools: [shared]\n"
                "    target_tools: [shared]\n"
                "    required_locales: [zh_CN, en_US]\n"
                "    variants:\n"
                "      - tool: shared\n"
                "        status: sampled\n"
                "        package_root: skills/shared/demo-skill\n"
                "        readme_file: skills/shared/demo-skill/README.md\n"
                "        status_file: skills/shared/demo-skill/STATUS.md\n"
                "        examples_root: examples/shared/demo-skill\n"
                "        locale_roots:\n"
                "          zh_CN:\n"
                "            status: sampled\n"
                "            import_root: skills/shared/demo-skill/zh_CN\n"
                "            skill_file: skills/shared/demo-skill/zh_CN/SKILL.md\n"
                "            examples_root: examples/shared/demo-skill/zh_CN\n"
                "            evidence:\n"
                "              sample_input: examples/shared/demo-skill/zh_CN/sample-input.md\n"
                "              sample_output: examples/shared/demo-skill/zh_CN/sample-output.md\n"
                "          en_US:\n"
                "            status: sampled\n"
                "            import_root: skills/shared/demo-skill/en_US\n"
                "            skill_file: skills/shared/demo-skill/en_US/SKILL.md\n"
                "            examples_root: examples/shared/demo-skill/en_US\n"
                "            evidence:\n"
                "              sample_input: examples/shared/demo-skill/en_US/sample-input.md\n"
                "              sample_output: examples/shared/demo-skill/en_US/sample-output.md\n"
                "          ja_JP:\n"
                "            status: draft\n"
                "            import_root: skills/shared/demo-skill/ja_JP\n"
                "            skill_file: skills/shared/demo-skill/ja_JP/SKILL.md\n"
                "            examples_root: examples/shared/demo-skill/ja_JP\n"
                "            evidence: {}\n"
                "    tags: [quality]\n",
                encoding="utf-8",
            )

            report = VALIDATOR.validate_repository(root)

            orphan = root / "skills" / "unknown-family" / "orphan-skill" / "en_US"
            orphan.mkdir(parents=True)
            (orphan / "SKILL.md").write_text(
                "---\n"
                "name: orphan-skill\n"
                "description: Unregistered fixture.\n"
                "---\n",
                encoding="utf-8",
            )
            orphan_report = VALIDATOR.validate_repository(root)

        self.assertEqual([], report.errors)
        self.assertIn(
            "unregistered-package",
            {finding.code for finding in orphan_report.errors},
        )

    def test_locale_scripts_are_identical(self):
        self.assertEqual(
            ZH_SCRIPT.read_text(encoding="utf-8"),
            EN_SCRIPT.read_text(encoding="utf-8"),
        )

    def test_current_repository_passes_strict_validation(self):
        report = VALIDATOR.validate_repository(ROOT)

        self.assertEqual([], report.errors)
        self.assertEqual([], report.warnings)
        self.assertEqual(6, report.checks["catalog_skills"])

    def test_skill_filter_selects_one_catalog_entry(self):
        report = VALIDATOR.validate_repository(ROOT, "SKL-0003")

        self.assertEqual(["SKL-0003:skill-quality-auditor"], report.selected_skills)
        self.assertEqual([], report.errors)

    def test_unknown_skill_is_an_error(self):
        report = VALIDATOR.validate_repository(ROOT, "SKL-9999")

        self.assertIn("unknown-skill", [finding.code for finding in report.errors])

    def test_json_report_redacts_repository_root(self):
        report = VALIDATOR.validate_repository(ROOT, "SKL-0003")

        self.assertEqual("<repo-root>", VALIDATOR._report_dict(report)["repo_root"])

    def test_frontmatter_rejects_extra_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill_file = root / "SKILL.md"
            skill_file.write_text(
                "---\n"
                "name: demo-skill\n"
                "description: Demo description.\n"
                "metadata: unexpected\n"
                "---\n\n"
                "# Demo\n",
                encoding="utf-8",
            )

            findings = VALIDATOR.check_skill_frontmatter(
                skill_file, root, "demo-skill"
            )

        self.assertIn("frontmatter-fields", [finding.code for finding in findings])

    def test_frontmatter_rejects_duplicate_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill_file = root / "SKILL.md"
            skill_file.write_text(
                "---\n"
                "name: demo-skill\n"
                "name: duplicate\n"
                "description: Demo description.\n"
                "---\n\n"
                "# Demo\n",
                encoding="utf-8",
            )

            findings = VALIDATOR.check_skill_frontmatter(
                skill_file, root, "demo-skill"
            )

        self.assertIn("frontmatter-duplicate", [finding.code for finding in findings])

    def test_frontmatter_accepts_quoted_name_and_folded_description(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill_file = root / "SKILL.md"
            skill_file.write_text(
                "---\n"
                "name: 'demo-skill'\n"
                "description: >-\n"
                "  Use when a folded description\n"
                "  is easier to maintain.\n"
                "---\n\n"
                "# Demo\n",
                encoding="utf-8",
            )

            findings = VALIDATOR.check_skill_frontmatter(
                skill_file, root, "demo-skill"
            )

        self.assertEqual([], findings)

    def test_frontmatter_accepts_inline_comments(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill_file = root / "SKILL.md"
            skill_file.write_text(
                "---\n"
                "name: demo-skill # canonical slug\n"
                "description: Demo description. # trigger summary\n"
                "---\n\n"
                "# Demo\n",
                encoding="utf-8",
            )

            findings = VALIDATOR.check_skill_frontmatter(
                skill_file, root, "demo-skill"
            )

        self.assertEqual([], findings)

    def test_repository_path_rejects_absolute_and_parent_segments(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            findings = []

            VALIDATOR._resolve_repo_path(
                root,
                "C:" + "/Users/" + "demo/file.md",
                findings,
                "fixture",
                "path",
            )
            VALIDATOR._resolve_repo_path(
                root, "inside/../file.md", findings, "fixture", "path"
            )

        codes = [finding.code for finding in findings]
        self.assertIn("absolute-path", codes)
        self.assertIn("parent-path-segment", codes)

    def test_repository_path_reports_case_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / "Actual.md").write_text("fixture\n", encoding="utf-8")
            findings = []

            VALIDATOR._resolve_repo_path(
                root, "actual.md", findings, "fixture", "path"
            )

        self.assertIn("path-case", [finding.code for finding in findings])

    def test_repository_path_checks_file_type(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / "not-a-file.md").mkdir()
            findings = []

            VALIDATOR._resolve_repo_path(
                root,
                "not-a-file.md",
                findings,
                "fixture",
                "path",
                "file",
            )

        self.assertIn("path-type", [finding.code for finding in findings])

    def test_markdown_checker_reports_broken_relative_link(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            markdown = root / "README.md"
            markdown.write_text("[missing](missing.md)\n", encoding="utf-8")
            findings = []

            VALIDATOR._check_markdown_links(root, [markdown], findings)

        self.assertIn("broken-link", [finding.code for finding in findings])

    def test_markdown_checker_handles_spaces_references_and_code_text(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            target = root / "file with spaces.md"
            target.write_text("target\n", encoding="utf-8")
            markdown = root / "README.md"
            markdown.write_text(
                "[inline](<file with spaces.md>)\n"
                "[reference][target]\n"
                "[target]: <file with spaces.md>\n"
                "```text\nmatrix[i][j]\n[fake]: missing.md\n```\n"
                "`[fake](missing.md)`\n"
                "`` `[fake](missing.md)` ``\n"
                "matrix[i][j] remains text.\n",
                encoding="utf-8",
            )
            findings = []

            VALIDATOR._check_markdown_links(root, [markdown], findings)

        self.assertEqual([], findings)

    def test_markdown_checker_reports_broken_reference_definition(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            markdown = root / "README.md"
            markdown.write_text(
                "[reference][target]\n[target]: missing.md\n",
                encoding="utf-8",
            )
            findings = []

            VALIDATOR._check_markdown_links(root, [markdown], findings)

        self.assertIn("broken-link", [finding.code for finding in findings])

    def test_markdown_checker_reports_likely_undefined_reference_link(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            markdown = root / "README.md"
            markdown.write_text("See [guide][missing-guide].\n", encoding="utf-8")
            findings = []

            VALIDATOR._check_markdown_links(root, [markdown], findings)

        self.assertIn(
            "missing-link-definition",
            [finding.code for finding in findings],
        )

    def test_public_safety_accepts_reserved_placeholders(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            note = root / "safe.md"
            note.write_text(
                "user@example.net\n/Users/<user>/project\n",
                encoding="utf-8",
            )
            findings = []

            VALIDATOR._check_public_safety(root, [note], findings)

        self.assertEqual([], findings)

    def test_public_safety_reports_macos_home_and_fine_grained_token(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            note = root / "unsafe.md"
            note.write_text(
                "/Users/" + "alice/private\n"
                "github_pat_" + "1234567890abcdefghijklmnop\n",
                encoding="utf-8",
            )
            findings = []

            VALIDATOR._check_public_safety(root, [note], findings)

        codes = {finding.code for finding in findings}
        self.assertIn("concrete-user-path", codes)
        self.assertIn("secret-pattern", codes)

    def test_public_file_collection_reports_forbidden_and_non_markdown_secret(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            env_file = root / ".env"
            env_file.write_text("placeholder=true\n", encoding="utf-8")
            script = root / "runtime.py"
            script.write_text(
                "TOKEN = 'github_pat_" + "1234567890abcdefghijklmnop'\n",
                encoding="utf-8",
            )
            private_key = root / "private-key.pem"
            private_key.write_text(
                "-----BEGIN " + "PRIVATE KEY-----\nplaceholder\n",
                encoding="utf-8",
            )
            env_template = root / ".env.example"
            env_template.write_text(
                "TOKEN=github_pat_" + "1234567890abcdefghijklmnop\n",
                encoding="utf-8",
            )
            extensionless_key = root / "deploy_key"
            extensionless_key.write_text(
                "-----BEGIN " + "PRIVATE KEY-----\nplaceholder\n",
                encoding="utf-8",
            )
            findings = []

            files = VALIDATOR._collect_public_text_files(root, [root], findings)
            VALIDATOR._check_public_safety(root, files, findings)

        codes = {finding.code for finding in findings}
        self.assertIn(private_key, files)
        self.assertIn(env_template, files)
        self.assertIn(extensionless_key, files)
        self.assertIn("forbidden-public-file", codes)
        self.assertIn("secret-pattern", codes)


if __name__ == "__main__":
    unittest.main()
