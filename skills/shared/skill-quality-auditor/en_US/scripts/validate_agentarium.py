#!/usr/bin/env python3
"""Deterministic, zero-third-party-dependency Agentarium checks."""

from __future__ import annotations

import argparse
import ast
import dataclasses
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable


ALLOWED_STATUSES = {
    "candidate",
    "draft",
    "sampled",
    "trial-validated",
    "ready",
    "deprecated",
}
STATUS_RANK = {
    "candidate": 0,
    "draft": 1,
    "sampled": 2,
    "trial-validated": 3,
    "ready": 4,
}
REQUIRED_SKILL_FIELDS = {
    "id",
    "slug",
    "title",
    "category",
    "scope",
    "status",
    "summary_zh",
    "summary_en",
    "model_fit",
    "supported_tools",
    "target_tools",
    "required_locales",
    "variants",
    "tags",
}
REQUIRED_VARIANT_FIELDS = {
    "tool",
    "status",
    "package_root",
    "readme_file",
    "status_file",
    "examples_root",
    "locale_roots",
}
REQUIRED_LOCALE_FIELDS = {
    "status",
    "import_root",
    "skill_file",
    "examples_root",
    "evidence",
}
TRIAL_EVIDENCE_KEYS = {"trial_output", "trial_note", "trial_evidence"}
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
REFERENCE_DEFINITION_RE = re.compile(
    r"(?m)^[ \t]{0,3}\[([^\]]+)\]:[ \t]*(.+)$"
)
REFERENCE_USE_RE = re.compile(r"(?<![!\w])\[([^\]\n]+)\]\[([^\]\n]*)\]")
IMAGE_REFERENCE_USE_RE = re.compile(r"!\[([^\]\n]*)\]\[([^\]\n]*)\]")
REFERENCE_RE = re.compile(r"references/[A-Za-z0-9._/-]+\.md")
WINDOWS_USER_RE = re.compile(
    r"[A-Za-z]:[\\/]+Users[\\/]+(?!<user>)[^\\/\s<>]+", re.IGNORECASE
)
POSIX_HOME_RE = re.compile(r"/home/(?!<user>)[A-Za-z0-9._-]+")
MACOS_HOME_RE = re.compile(r"/Users/(?!<user>)[A-Za-z0-9._-]+")
EMAIL_RE = re.compile(
    r"\b[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})\b"
)
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
]
SKIP_SCAN_DIRECTORIES = {".git", ".hug", ".venv", "node_modules", "venv", "__pycache__"}
FORBIDDEN_PUBLIC_FILENAMES = {
    "auth.json",
    "cookies.json",
    "credentials.json",
    "id_ed25519",
    "id_rsa",
}


class CatalogParseError(ValueError):
    """Raised when catalog YAML uses unsupported or malformed structure."""


def _strip_inline_comment(value: str) -> str:
    quote: str | None = None
    escaped = False
    for index, character in enumerate(value):
        if escaped:
            escaped = False
            continue
        if quote == '"' and character == "\\":
            escaped = True
            continue
        if quote:
            if character == quote:
                quote = None
            continue
        if character in {"'", '"'}:
            quote = character
            continue
        if character == "#" and (index == 0 or value[index - 1].isspace()):
            return value[:index].rstrip()
    return value.rstrip()


def _mapping_colon(value: str) -> int | None:
    quote: str | None = None
    escaped = False
    depth = 0
    for index, character in enumerate(value):
        if escaped:
            escaped = False
            continue
        if quote == '"' and character == "\\":
            escaped = True
            continue
        if quote:
            if character == quote:
                quote = None
            continue
        if character in {"'", '"'}:
            quote = character
        elif character in "[{":
            depth += 1
        elif character in "]}":
            depth = max(0, depth - 1)
        elif character == ":" and depth == 0:
            if index + 1 == len(value) or value[index + 1].isspace():
                return index
    return None


@dataclasses.dataclass(frozen=True)
class Finding:
    level: str
    code: str
    path: str
    message: str


@dataclasses.dataclass
class ValidationReport:
    repo_root: str
    selected_skills: list[str]
    findings: list[Finding]
    checks: dict[str, int]

    @property
    def errors(self) -> list[Finding]:
        return [finding for finding in self.findings if finding.level == "ERROR"]

    @property
    def warnings(self) -> list[Finding]:
        return [finding for finding in self.findings if finding.level == "WARNING"]


def _catalog_lines(text: str) -> list[tuple[int, str, int]]:
    lines: list[tuple[int, str, int]] = []
    for line_number, raw in enumerate(text.splitlines(), start=1):
        if "\t" in raw[: len(raw) - len(raw.lstrip())]:
            raise CatalogParseError(f"line {line_number}: tabs are not supported")
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        content = _strip_inline_comment(raw[indent:])
        if content:
            lines.append((indent, content, line_number))
    return lines


def _split_inline_list(body: str) -> list[str]:
    items: list[str] = []
    current: list[str] = []
    quote: str | None = None
    escaped = False
    index = 0
    while index < len(body):
        character = body[index]
        if escaped:
            current.append(character)
            escaped = False
        elif quote == '"' and character == "\\":
            current.append(character)
            escaped = True
        elif quote == "'" and character == "'" and index + 1 < len(body) and body[index + 1] == "'":
            current.extend(("'", "'"))
            index += 1
        elif quote:
            current.append(character)
            if character == quote:
                quote = None
        elif character in {"'", '"'}:
            quote = character
            current.append(character)
        elif character in "[]{}":
            raise CatalogParseError("nested flow collections are not supported")
        elif character == ",":
            item = "".join(current).strip()
            if not item:
                raise CatalogParseError("inline list contains an empty item")
            items.append(item)
            current = []
        else:
            current.append(character)
        index += 1
    if quote:
        raise CatalogParseError("unterminated quote in inline list")
    item = "".join(current).strip()
    if item:
        items.append(item)
    elif items:
        raise CatalogParseError("inline list contains a trailing empty item")
    return items


def _parse_scalar(raw: str) -> Any:
    value = raw.strip()
    if value in {"[]", "{}"}:
        return [] if value == "[]" else {}
    if value in {"true", "false"}:
        return value == "true"
    if value in {"null", "~"}:
        return None
    if value.startswith("["):
        if not value.endswith("]"):
            raise CatalogParseError(f"invalid inline list {value!r}")
        body = value[1:-1].strip()
        return [_parse_scalar(item) for item in _split_inline_list(body)] if body else []
    if value.startswith("'"):
        if not value.endswith("'") or len(value) < 2:
            raise CatalogParseError(f"invalid single-quoted scalar {value!r}")
        return value[1:-1].replace("''", "'")
    if value.startswith(("'", '"', "{")):
        try:
            return ast.literal_eval(value)
        except (ValueError, SyntaxError) as exc:
            raise CatalogParseError(f"invalid scalar {value!r}") from exc
    if re.fullmatch(r"-?[0-9]+", value):
        return int(value)
    return value


def _split_mapping(content: str, line_number: int) -> tuple[str, str]:
    separator = _mapping_colon(content)
    if separator is None:
        raise CatalogParseError(f"line {line_number}: expected key: value")
    key, value = content[:separator], content[separator + 1 :]
    key = key.strip()
    if not key:
        raise CatalogParseError(f"line {line_number}: empty mapping key")
    return key, value.strip()


def parse_catalog_yaml(text: str) -> dict[str, Any]:
    """Parse the mapping/list subset used by catalog/skills.yaml."""

    lines = _catalog_lines(text)

    def parse_block(index: int, indent: int) -> tuple[Any, int]:
        if lines[index][1].startswith("- "):
            return parse_list(index, indent)
        return parse_mapping(index, indent)

    def parse_mapping(index: int, indent: int) -> tuple[dict[str, Any], int]:
        result: dict[str, Any] = {}
        while index < len(lines):
            current_indent, content, line_number = lines[index]
            if current_indent < indent:
                break
            if current_indent > indent:
                raise CatalogParseError(
                    f"line {line_number}: unexpected indentation"
                )
            if content.startswith("- "):
                break
            key, raw_value = _split_mapping(content, line_number)
            if key in result:
                raise CatalogParseError(f"line {line_number}: duplicate key {key}")
            index += 1
            if raw_value:
                result[key] = _parse_scalar(raw_value)
            elif index < len(lines) and lines[index][0] > indent:
                result[key], index = parse_block(index, lines[index][0])
            else:
                result[key] = None
        return result, index

    def parse_list(index: int, indent: int) -> tuple[list[Any], int]:
        result: list[Any] = []
        while index < len(lines):
            current_indent, content, line_number = lines[index]
            if current_indent < indent:
                break
            if current_indent != indent or not content.startswith("- "):
                break
            item_text = content[2:].strip()
            index += 1
            if not item_text:
                if index >= len(lines) or lines[index][0] <= indent:
                    result.append(None)
                else:
                    child, index = parse_block(index, lines[index][0])
                    result.append(child)
                continue
            if _mapping_colon(item_text) is None:
                result.append(_parse_scalar(item_text))
                continue
            key, raw_value = _split_mapping(item_text, line_number)
            item: dict[str, Any] = {key: _parse_scalar(raw_value) if raw_value else None}
            item_mapping_indent = indent + 2
            if (
                not raw_value
                and index < len(lines)
                and lines[index][0] > item_mapping_indent
            ):
                item[key], index = parse_block(index, lines[index][0])
            if index < len(lines) and lines[index][0] > indent:
                tail_indent = lines[index][0]
                tail, index = parse_mapping(index, tail_indent)
                overlap = set(item) & set(tail)
                if overlap:
                    raise CatalogParseError(
                        f"line {line_number}: duplicate list item keys {sorted(overlap)}"
                    )
                item.update(tail)
            result.append(item)
        return result, index

    if not lines:
        return {}
    parsed, final_index = parse_block(0, lines[0][0])
    if final_index != len(lines) or not isinstance(parsed, dict):
        raise CatalogParseError("catalog root must be a mapping")
    return parsed


def _relative(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def _case_mismatch(repo_root: Path, raw: str) -> tuple[str, str] | None:
    current = repo_root
    for part in Path(raw).parts:
        if part in {"", "."}:
            continue
        try:
            names = {child.name for child in current.iterdir()}
        except OSError:
            return None
        if part in names:
            current /= part
            continue
        folded = next((name for name in names if name.casefold() == part.casefold()), None)
        if folded is not None:
            return part, folded
        return None
    return None


def _resolve_repo_path(
    repo_root: Path,
    raw: Any,
    findings: list[Finding],
    source: str,
    field: str,
    expected_kind: str | None = None,
) -> Path | None:
    if not isinstance(raw, str) or not raw:
        findings.append(Finding("ERROR", "invalid-path", source, f"{field} is empty"))
        return None
    if Path(raw).is_absolute() or re.match(r"^(?:[A-Za-z]:[\\/]|\\\\)", raw):
        findings.append(
            Finding(
                "ERROR",
                "absolute-path",
                source,
                f"{field} must be repository-relative",
            )
        )
        return None
    if "\\" in raw:
        findings.append(
            Finding(
                "ERROR",
                "path-separator",
                source,
                f"{field} must use forward slashes",
            )
        )
        return None
    if ".." in Path(raw).parts:
        findings.append(
            Finding(
                "ERROR",
                "parent-path-segment",
                source,
                f"{field} must not contain '..'",
            )
        )
        return None
    candidate = (repo_root / raw).resolve()
    try:
        candidate.relative_to(repo_root)
    except ValueError:
        findings.append(
            Finding("ERROR", "path-escape", source, f"{field} escapes repository: {raw}")
        )
        return None
    mismatch = _case_mismatch(repo_root, raw)
    if mismatch is not None:
        requested, actual = mismatch
        findings.append(
            Finding(
                "ERROR",
                "path-case",
                source,
                f"{field} uses {requested!r}; filesystem entry is {actual!r}",
            )
        )
    elif not candidate.exists():
        findings.append(
            Finding("ERROR", "missing-path", source, f"{field} does not exist: {raw}")
        )
    elif expected_kind == "file" and not candidate.is_file():
        findings.append(
            Finding("ERROR", "path-type", source, f"{field} must point to a file")
        )
    elif expected_kind == "directory" and not candidate.is_dir():
        findings.append(
            Finding("ERROR", "path-type", source, f"{field} must point to a directory")
        )
    return candidate


def _status_rank(status: Any) -> int | None:
    return STATUS_RANK.get(status) if isinstance(status, str) else None


def _is_nonempty_string_list(value: Any) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, str) and bool(item.strip()) for item in value)
        and len(value) == len(set(value))
    )


def check_skill_frontmatter(
    skill_file: Path, repo_root: Path, expected_name: str
) -> list[Finding]:
    findings: list[Finding] = []
    source = _relative(repo_root, skill_file)
    try:
        text = skill_file.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [Finding("ERROR", "skill-read", source, str(exc))]
    match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", text, re.DOTALL)
    if not match:
        return [
            Finding("ERROR", "frontmatter-missing", source, "missing YAML frontmatter")
        ]
    fields: dict[str, str] = {}
    frontmatter_lines = match.group(1).splitlines()
    index = 0
    while index < len(frontmatter_lines):
        line = frontmatter_lines[index]
        index += 1
        if not line.strip():
            continue
        if line[0].isspace():
            findings.append(
                Finding(
                    "ERROR",
                    "frontmatter-invalid",
                    source,
                    f"unexpected indented line: {line.strip()}",
                )
            )
            continue
        if ":" not in line:
            findings.append(
                Finding("ERROR", "frontmatter-invalid", source, f"invalid line: {line}")
            )
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key in fields:
            findings.append(
                Finding(
                    "ERROR",
                    "frontmatter-duplicate",
                    source,
                    f"duplicate frontmatter field: {key}",
                )
            )
            continue
        raw_value = _strip_inline_comment(value).strip()
        if raw_value in {"|", "|-", "|+", ">", ">-", ">+"}:
            continuation: list[str] = []
            while index < len(frontmatter_lines):
                next_line = frontmatter_lines[index]
                if next_line and not next_line[0].isspace():
                    break
                continuation.append(next_line.strip())
                index += 1
            separator = "\n" if raw_value.startswith("|") else " "
            parsed_value: Any = separator.join(continuation).strip()
        else:
            try:
                parsed_value = _parse_scalar(raw_value)
            except CatalogParseError as exc:
                findings.append(
                    Finding("ERROR", "frontmatter-invalid", source, str(exc))
                )
                continue
        if not isinstance(parsed_value, str):
            findings.append(
                Finding(
                    "ERROR",
                    "frontmatter-invalid",
                    source,
                    f"{key} must be a string",
                )
            )
            continue
        fields[key] = parsed_value
    if set(fields) != {"name", "description"}:
        findings.append(
            Finding(
                "ERROR",
                "frontmatter-fields",
                source,
                f"expected only name and description; found {sorted(fields)}",
            )
        )
    if fields.get("name") != expected_name:
        findings.append(
            Finding(
                "ERROR",
                "frontmatter-name",
                source,
                f"name must be {expected_name!r}",
            )
        )
    if not fields.get("description"):
        findings.append(
            Finding("ERROR", "frontmatter-description", source, "description is empty")
        )
    for reference in sorted(set(REFERENCE_RE.findall(text))):
        target = (skill_file.parent / reference).resolve()
        try:
            target.relative_to(skill_file.parent.resolve())
        except ValueError:
            findings.append(
                Finding(
                    "ERROR",
                    "runtime-reference-escape",
                    source,
                    f"runtime reference escapes import root: {reference}",
                )
            )
            continue
        if not target.is_file():
            findings.append(
                Finding(
                    "ERROR",
                    "missing-runtime-reference",
                    source,
                    f"missing runtime reference: {reference}",
                )
            )
    return findings


def _markdown_destination(raw: str) -> str:
    value = raw.strip()
    if value.startswith("<"):
        closing = value.find(">", 1)
        return value[1:closing] if closing >= 0 else value[1:]
    return value.split(maxsplit=1)[0] if value else ""


def _reference_label(raw: str) -> str:
    return " ".join(raw.strip().casefold().split())


def _strip_inline_code(line: str) -> str:
    output: list[str] = []
    index = 0
    while index < len(line):
        start = line.find("`", index)
        if start < 0:
            output.append(line[index:])
            break
        output.append(line[index:start])
        opener_end = start
        while opener_end < len(line) and line[opener_end] == "`":
            opener_end += 1
        length = opener_end - start
        search_from = opener_end
        closing = -1
        marker = "`" * length
        while True:
            candidate = line.find(marker, search_from)
            if candidate < 0:
                break
            before_is_tick = candidate > 0 and line[candidate - 1] == "`"
            after = candidate + length
            after_is_tick = after < len(line) and line[after] == "`"
            if not before_is_tick and not after_is_tick:
                closing = candidate
                break
            search_from = candidate + 1
        if closing < 0:
            output.append(line[start:opener_end])
            index = opener_end
        else:
            output.append(" ")
            index = closing + length
    return "".join(output)


def _markdown_without_code(text: str) -> str:
    output: list[str] = []
    fence_character: str | None = None
    fence_length = 0
    for line in text.splitlines():
        stripped = line.lstrip(" ")
        indent = len(line) - len(stripped)
        fence = re.match(r"(`{3,}|~{3,})", stripped) if indent <= 3 else None
        if fence:
            marker = fence.group(1)
            if fence_character is None:
                fence_character = marker[0]
                fence_length = len(marker)
                output.append("")
                continue
            if marker[0] == fence_character and len(marker) >= fence_length:
                fence_character = None
                fence_length = 0
            output.append("")
            continue
        if fence_character is not None:
            output.append("")
            continue
        output.append(_strip_inline_code(line))
    return "\n".join(output)


def _check_markdown_links(
    repo_root: Path, files: Iterable[Path], findings: list[Finding]
) -> None:
    for markdown in files:
        source = _relative(repo_root, markdown)
        try:
            text = markdown.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            findings.append(Finding("ERROR", "markdown-read", source, str(exc)))
            continue

        link_text = _markdown_without_code(text)
        definitions = {
            _reference_label(label): destination
            for label, destination in REFERENCE_DEFINITION_RE.findall(link_text)
        }
        reference_uses = [
            *REFERENCE_USE_RE.findall(link_text),
            *IMAGE_REFERENCE_USE_RE.findall(link_text),
        ]
        for label, reference in reference_uses:
            normalized = _reference_label(reference or label)
            if normalized not in definitions:
                findings.append(
                    Finding(
                        "ERROR",
                        "missing-link-definition",
                        source,
                        f"missing reference-style link definition: {reference or label}",
                    )
                )
        raw_targets = [*MARKDOWN_LINK_RE.findall(link_text), *definitions.values()]
        for raw_target in raw_targets:
            target = _markdown_destination(raw_target)
            if not target or target.startswith("#") or re.match(
                r"^[A-Za-z][A-Za-z0-9+.-]*:", target
            ):
                continue
            target = target.split("#", 1)[0]
            resolved = (markdown.parent / target).resolve()
            try:
                resolved.relative_to(repo_root)
            except ValueError:
                findings.append(
                    Finding(
                        "ERROR",
                        "link-escape",
                        source,
                        f"relative link escapes repository: {target}",
                    )
                )
                continue
            if target and not resolved.exists():
                findings.append(
                    Finding(
                        "ERROR",
                        "broken-link",
                        source,
                        f"relative link does not resolve: {target}",
                    )
                )


def _check_public_safety(
    repo_root: Path, files: Iterable[Path], findings: list[Finding]
) -> None:
    for path in sorted(set(files)):
        if not path.is_file():
            continue
        source = _relative(repo_root, path)
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                findings.append(
                    Finding(
                        "ERROR",
                        "secret-pattern",
                        source,
                        "high-confidence secret or private-key pattern found",
                    )
                )
        if (
            WINDOWS_USER_RE.search(text)
            or POSIX_HOME_RE.search(text)
            or MACOS_HOME_RE.search(text)
        ):
            findings.append(
                Finding(
                    "WARNING",
                    "concrete-user-path",
                    source,
                    "concrete user-home path found; review before publication",
                )
            )
        for match in EMAIL_RE.finditer(text):
            domain = match.group(1).lower()
            if domain not in {
                "example.com",
                "example.net",
                "example.org",
                "example.invalid",
            } and not domain.endswith((".example", ".invalid")):
                findings.append(
                    Finding(
                        "WARNING",
                        "email-address",
                        source,
                        "non-placeholder email address found; review before publication",
                    )
                )
                break


def _is_forbidden_public_file(path: Path) -> bool:
    name = path.name.lower()
    if name in FORBIDDEN_PUBLIC_FILENAMES:
        return True
    if name == ".env":
        return True
    if name.startswith(".env.") and not name.endswith(
        (".example", ".sample", ".template")
    ):
        return True
    return False


def _collect_public_text_files(
    repo_root: Path, roots: Iterable[Path], findings: list[Finding]
) -> set[Path]:
    files: set[Path] = set()
    seen: set[Path] = set()
    for root in roots:
        root = root.resolve()
        if not root.exists():
            continue
        candidates = [root] if root.is_file() else root.rglob("*")
        for path in candidates:
            if not path.is_file():
                continue
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            try:
                relative = resolved.relative_to(repo_root)
            except ValueError:
                continue
            if any(part in SKIP_SCAN_DIRECTORIES for part in relative.parts[:-1]):
                continue
            if _is_forbidden_public_file(resolved):
                findings.append(
                    Finding(
                        "ERROR",
                        "forbidden-public-file",
                        relative.as_posix(),
                        "sensitive credential or environment filename must not be published",
                    )
                )
            try:
                size = resolved.stat().st_size
            except OSError:
                continue
            if size > 1_000_000:
                continue
            try:
                resolved.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                continue
            files.add(resolved)
    return files


def validate_repository(
    repo_root: Path, skill_filter: str | None = None
) -> ValidationReport:
    repo_root = repo_root.expanduser().resolve()
    findings: list[Finding] = []
    checks: dict[str, int] = {
        "catalog_skills": 0,
        "selected_skills": 0,
        "variants": 0,
        "locales": 0,
        "markdown_files": 0,
        "safety_files": 0,
    }
    governance = [
        "AGENTS.md",
        "README.md",
        "catalog/skills.yaml",
        "catalog/status-policy.md",
        "docs/importing.md",
        "docs/publishing.md",
        "docs/localization.md",
        "docs/safety.md",
        "docs/skill-completeness.md",
    ]
    for raw_path in governance:
        if not (repo_root / raw_path).is_file():
            findings.append(
                Finding(
                    "ERROR",
                    "missing-governance",
                    raw_path,
                    "required governance file is missing",
                )
            )
    catalog_path = repo_root / "catalog" / "skills.yaml"
    if not catalog_path.is_file():
        return ValidationReport(str(repo_root), [], findings, checks)
    try:
        catalog = parse_catalog_yaml(catalog_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, CatalogParseError) as exc:
        findings.append(
            Finding("ERROR", "catalog-parse", "catalog/skills.yaml", str(exc))
        )
        return ValidationReport(str(repo_root), [], findings, checks)

    if catalog.get("schema_version") != 2:
        findings.append(
            Finding(
                "ERROR",
                "schema-version",
                "catalog/skills.yaml",
                "schema_version must be 2",
            )
        )
    catalog_required_locales = catalog.get("required_locales")
    if (
        not isinstance(catalog_required_locales, list)
        or not all(isinstance(locale, str) for locale in catalog_required_locales)
        or len(catalog_required_locales) != len(set(catalog_required_locales))
        or not {"zh_CN", "en_US"} <= set(catalog_required_locales)
    ):
        findings.append(
            Finding(
                "ERROR",
                "catalog-required-locales",
                "catalog/skills.yaml",
                "required_locales must uniquely include zh_CN and en_US",
            )
        )
        catalog_required_locales = ["zh_CN", "en_US"]
    tool_families = catalog.get("tool_families")
    if not _is_nonempty_string_list(tool_families):
        findings.append(
            Finding(
                "ERROR",
                "tool-families",
                "catalog/skills.yaml",
                "tool_families must be a unique non-empty list of strings",
            )
        )
        tool_families = ["shared", "trae", "claude", "codex"]
    tool_family_set = set(tool_families)

    skills = catalog.get("skills")
    if not isinstance(skills, list):
        findings.append(
            Finding(
                "ERROR",
                "catalog-skills",
                "catalog/skills.yaml",
                "skills must be a list",
            )
        )
        return ValidationReport(str(repo_root), [], findings, checks)
    checks["catalog_skills"] = len(skills)
    seen_ids: set[str] = set()
    seen_slugs: set[str] = set()
    selected: list[dict[str, Any]] = []
    for skill in skills:
        if not isinstance(skill, dict):
            findings.append(
                Finding(
                    "ERROR",
                    "catalog-entry",
                    "catalog/skills.yaml",
                    "skill entry must be a mapping",
                )
            )
            continue
        skill_id = skill.get("id")
        slug = skill.get("slug")
        if not isinstance(skill_id, str) or not re.fullmatch(r"SKL-[0-9]{4}", skill_id):
            findings.append(
                Finding(
                    "ERROR",
                    "invalid-id",
                    "catalog/skills.yaml",
                    f"invalid Skill ID: {skill_id!r}",
                )
            )
        elif skill_id in seen_ids:
            findings.append(
                Finding(
                    "ERROR",
                    "duplicate-id",
                    "catalog/skills.yaml",
                    f"duplicate Skill ID: {skill_id}",
                )
            )
        else:
            seen_ids.add(skill_id)
        if not isinstance(slug, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
            findings.append(
                Finding(
                    "ERROR",
                    "invalid-slug",
                    "catalog/skills.yaml",
                    f"invalid slug: {slug!r}",
                )
            )
        elif slug in seen_slugs:
            findings.append(
                Finding(
                    "ERROR",
                    "duplicate-slug",
                    "catalog/skills.yaml",
                    f"duplicate slug: {slug}",
                )
            )
        else:
            seen_slugs.add(slug)
        if skill_filter is None or skill_filter == skill_id or skill_filter == slug:
            selected.append(skill)

    if skill_filter and not selected:
        findings.append(
            Finding(
                "ERROR",
                "unknown-skill",
                "catalog/skills.yaml",
                f"no Skill matches {skill_filter!r}",
            )
        )
    checks["selected_skills"] = len(selected)
    markdown_files: set[Path] = set()
    safety_files: set[Path] = set()
    safety_roots: set[Path] = set()
    registered_package_roots: set[str] = set()

    for skill in selected:
        skill_id = str(skill.get("id", "<unknown>"))
        slug = str(skill.get("slug", "<unknown>"))
        source = f"catalog/skills.yaml::{skill_id}"
        missing_fields = sorted(REQUIRED_SKILL_FIELDS - set(skill))
        if missing_fields:
            findings.append(
                Finding(
                    "ERROR",
                    "missing-skill-fields",
                    source,
                    f"missing fields: {', '.join(missing_fields)}",
                )
            )
        for field in ("title", "category", "summary_zh", "summary_en"):
            value = skill.get(field)
            if not isinstance(value, str) or not value.strip():
                findings.append(
                    Finding(
                        "ERROR",
                        "skill-string-field",
                        source,
                        f"{field} must be a non-empty string",
                    )
                )
        scope = skill.get("scope")
        if not isinstance(scope, str) or scope not in {"shared", "tool-specific"}:
            findings.append(
                Finding(
                    "ERROR",
                    "scope",
                    source,
                    "scope must be shared or tool-specific",
                )
            )
        if not _is_nonempty_string_list(skill.get("tags")):
            findings.append(
                Finding(
                    "ERROR",
                    "tags",
                    source,
                    "tags must be a unique non-empty list of strings",
                )
            )
        status = skill.get("status")
        if not isinstance(status, str) or status not in ALLOWED_STATUSES:
            findings.append(
                Finding("ERROR", "invalid-status", source, f"invalid status: {status}")
            )
        target_tools = skill.get("target_tools")
        if not _is_nonempty_string_list(target_tools):
            findings.append(
                Finding(
                    "ERROR",
                    "target-tools",
                    source,
                    "target_tools must be a unique non-empty list of strings",
                )
            )
            target_tools = []
        elif not set(target_tools) <= tool_family_set:
            findings.append(
                Finding(
                    "ERROR",
                    "target-tool-family",
                    source,
                    "target_tools contains an unknown tool family",
                )
            )
        model_fit = skill.get("model_fit")
        if not isinstance(model_fit, dict) or not all(
            _is_nonempty_string_list(model_fit.get(key))
            for key in ("suitable_for", "not_suitable_for")
        ):
            findings.append(
                Finding(
                    "ERROR",
                    "model-fit",
                    source,
                    "model_fit must contain non-empty suitable_for and not_suitable_for lists",
                )
            )
        variants = skill.get("variants")
        supported_tools = skill.get("supported_tools")
        required_locales = skill.get("required_locales")
        if not isinstance(variants, list):
            findings.append(
                Finding("ERROR", "variants", source, "variants must be a list")
            )
            continue
        if not isinstance(supported_tools, list) or any(
            not isinstance(tool, str) or not tool.strip() for tool in supported_tools
        ):
            findings.append(
                Finding(
                    "ERROR",
                    "supported-tools",
                    source,
                    "supported_tools must be a list of non-empty strings",
                )
            )
            supported_tools = []
        elif len(supported_tools) != len(set(supported_tools)):
            findings.append(
                Finding(
                    "ERROR",
                    "duplicate-supported-tool",
                    source,
                    "supported_tools must not contain duplicates",
                )
            )
        elif not set(supported_tools) <= tool_family_set:
            findings.append(
                Finding(
                    "ERROR",
                    "supported-tool-family",
                    source,
                    "supported_tools contains an unknown tool family",
                )
            )
        if not isinstance(required_locales, list) or not required_locales:
            findings.append(
                Finding(
                    "ERROR",
                    "required-locales",
                    source,
                    "required_locales must be non-empty",
                )
            )
            required_locales = []
        elif (
            not all(isinstance(locale, str) for locale in required_locales)
            or len(required_locales) != len(set(required_locales))
        ):
            findings.append(
                Finding(
                    "ERROR",
                    "required-locales-values",
                    source,
                    "required_locales must contain unique locale strings",
                )
            )
            required_locales = list(
                dict.fromkeys(
                    locale for locale in required_locales if isinstance(locale, str)
                )
            )
        if not set(catalog_required_locales) <= {
            locale for locale in required_locales if isinstance(locale, str)
        }:
            findings.append(
                Finding(
                    "ERROR",
                    "required-locales-policy",
                    source,
                    "Skill required_locales must include repository required_locales",
                )
            )
        if not variants:
            if status != "candidate":
                findings.append(
                    Finding(
                        "ERROR",
                        "candidate-status",
                        source,
                        "a Skill without variants must remain candidate",
                    )
                )
            if supported_tools:
                findings.append(
                    Finding(
                        "ERROR",
                        "candidate-supported-tools",
                        source,
                        "a Skill without variants must not list supported_tools",
                    )
                )
            continue

        variant_tool_list = [
            variant.get("tool")
            for variant in variants
            if isinstance(variant, dict) and isinstance(variant.get("tool"), str)
        ]
        variant_tools = set(variant_tool_list)
        if len(variant_tool_list) != len(variant_tools):
            findings.append(
                Finding("ERROR", "duplicate-variant", source, "variant tools must be unique")
            )
        if set(supported_tools) != variant_tools:
            findings.append(
                Finding(
                    "ERROR",
                    "supported-tool-mismatch",
                    source,
                    f"supported_tools {supported_tools} != variant tools {sorted(variant_tools)}",
                )
            )
        variant_ranks: list[int] = []
        for variant in variants:
            checks["variants"] += 1
            if not isinstance(variant, dict):
                findings.append(
                    Finding("ERROR", "variant-entry", source, "variant must be a mapping")
                )
                continue
            tool = str(variant.get("tool", "<unknown>"))
            variant_source = f"{source}/{tool}"
            variant_tool = variant.get("tool")
            if not isinstance(variant_tool, str) or variant_tool not in tool_family_set:
                findings.append(
                    Finding(
                        "ERROR",
                        "variant-tool-family",
                        variant_source,
                        "variant tool must be a known tool family",
                    )
                )
            missing_variant = sorted(REQUIRED_VARIANT_FIELDS - set(variant))
            if missing_variant:
                findings.append(
                    Finding(
                        "ERROR",
                        "missing-variant-fields",
                        variant_source,
                        f"missing fields: {', '.join(missing_variant)}",
                    )
                )
            variant_status = variant.get("status")
            if (
                not isinstance(variant_status, str)
                or variant_status not in ALLOWED_STATUSES
            ):
                findings.append(
                    Finding(
                        "ERROR",
                        "invalid-variant-status",
                        variant_source,
                        f"invalid status: {variant_status}",
                    )
                )
            rank = _status_rank(variant_status)
            if rank is not None:
                variant_ranks.append(rank)
            expected_package = f"skills/{tool}/{slug}"
            expected_examples = f"examples/{tool}/{slug}"
            package_root_value = variant.get("package_root")
            if isinstance(package_root_value, str):
                registered_package_roots.add(package_root_value)
            fields_to_resolve = ["package_root", "readme_file", "status_file"]
            if rank is not None and rank >= STATUS_RANK["sampled"]:
                fields_to_resolve.append("examples_root")
            expected_kinds = {
                "package_root": "directory",
                "readme_file": "file",
                "status_file": "file",
                "examples_root": "directory",
            }
            for field in fields_to_resolve:
                path = _resolve_repo_path(
                    repo_root,
                    variant.get(field),
                    findings,
                    variant_source,
                    field,
                    expected_kinds[field],
                )
                if path and path.suffix == ".md":
                    markdown_files.add(path)
                if field in {"package_root", "examples_root"} and path and path.is_dir():
                    safety_roots.add(path)
            if variant.get("package_root") != expected_package:
                findings.append(
                    Finding(
                        "ERROR",
                        "package-root",
                        variant_source,
                        f"package_root must be {expected_package}",
                    )
                )
            if variant.get("readme_file") != f"{expected_package}/README.md":
                findings.append(
                    Finding(
                        "ERROR",
                        "readme-path",
                        variant_source,
                        "readme_file must be package_root/README.md",
                    )
                )
            if variant.get("status_file") != f"{expected_package}/STATUS.md":
                findings.append(
                    Finding(
                        "ERROR",
                        "status-path",
                        variant_source,
                        "status_file must be package_root/STATUS.md",
                    )
                )
            if variant.get("examples_root") != expected_examples:
                findings.append(
                    Finding(
                        "ERROR",
                        "examples-root",
                        variant_source,
                        f"examples_root must be {expected_examples}",
                    )
                )
            expected_examples_path = repo_root / expected_examples
            if expected_examples_path.is_dir():
                safety_roots.add(expected_examples_path)
            locale_roots = variant.get("locale_roots")
            if not isinstance(locale_roots, dict):
                findings.append(
                    Finding(
                        "ERROR",
                        "locale-roots",
                        variant_source,
                        "locale_roots must be a mapping",
                    )
                )
                continue
            if not all(isinstance(locale, str) for locale in locale_roots):
                findings.append(
                    Finding(
                        "ERROR",
                        "locale-root-keys",
                        variant_source,
                        "locale_roots keys must be locale strings",
                    )
                )
            missing_locales = sorted(set(required_locales) - set(locale_roots))
            if missing_locales:
                findings.append(
                    Finding(
                        "ERROR",
                        "missing-locales",
                        variant_source,
                        f"missing locales: {', '.join(missing_locales)}",
                    )
                )
            locale_ranks: list[int] = []
            locales_to_check = list(
                dict.fromkeys(
                    [
                        *required_locales,
                        *(
                            locale
                            for locale in locale_roots
                            if isinstance(locale, str)
                        ),
                    ]
                )
            )
            for locale in locales_to_check:
                info = locale_roots.get(locale)
                if not isinstance(info, dict):
                    continue
                checks["locales"] += 1
                locale_source = f"{variant_source}/{locale}"
                missing_locale_fields = sorted(REQUIRED_LOCALE_FIELDS - set(info))
                if missing_locale_fields:
                    findings.append(
                        Finding(
                            "ERROR",
                            "missing-locale-fields",
                            locale_source,
                            f"missing fields: {', '.join(missing_locale_fields)}",
                        )
                    )
                locale_status = info.get("status")
                if (
                    not isinstance(locale_status, str)
                    or locale_status not in ALLOWED_STATUSES
                ):
                    findings.append(
                        Finding(
                            "ERROR",
                            "invalid-locale-status",
                            locale_source,
                            f"invalid status: {locale_status}",
                        )
                    )
                locale_rank = _status_rank(locale_status)
                if locale in required_locales and locale_rank is not None:
                    locale_ranks.append(locale_rank)
                expected_import = f"{expected_package}/{locale}"
                expected_skill_file = f"{expected_import}/SKILL.md"
                expected_locale_examples = f"{expected_examples}/{locale}"
                if info.get("import_root") != expected_import:
                    findings.append(
                        Finding(
                            "ERROR",
                            "import-root",
                            locale_source,
                            f"import_root must be {expected_import}",
                        )
                    )
                if info.get("skill_file") != expected_skill_file:
                    findings.append(
                        Finding(
                            "ERROR",
                            "skill-file",
                            locale_source,
                            f"skill_file must be {expected_skill_file}",
                        )
                    )
                if info.get("examples_root") != expected_locale_examples:
                    findings.append(
                        Finding(
                            "ERROR",
                            "locale-examples-root",
                            locale_source,
                            f"examples_root must be {expected_locale_examples}",
                        )
                    )
                import_root = _resolve_repo_path(
                    repo_root,
                    info.get("import_root"),
                    findings,
                    locale_source,
                    "import_root",
                    "directory",
                )
                skill_file = _resolve_repo_path(
                    repo_root,
                    info.get("skill_file"),
                    findings,
                    locale_source,
                    "skill_file",
                    "file",
                )
                examples_root = None
                if locale_rank is not None and locale_rank >= STATUS_RANK["sampled"]:
                    examples_root = _resolve_repo_path(
                        repo_root,
                        info.get("examples_root"),
                        findings,
                        locale_source,
                        "examples_root",
                        "directory",
                    )
                if import_root and skill_file and skill_file.is_file():
                    findings.extend(
                        check_skill_frontmatter(skill_file, repo_root, slug)
                    )
                    markdown_files.add(skill_file)
                    references_dir = import_root / "references"
                    if references_dir.is_dir():
                        markdown_files.update(references_dir.rglob("*.md"))
                if examples_root and examples_root.is_dir():
                    example_files = set(examples_root.rglob("*.md"))
                    markdown_files.update(example_files)
                    safety_files.update(example_files)
                evidence = info.get("evidence")
                if not isinstance(evidence, dict):
                    findings.append(
                        Finding(
                            "ERROR",
                            "evidence",
                            locale_source,
                            "evidence must be a mapping",
                        )
                    )
                    evidence = {}
                for evidence_key, evidence_path in evidence.items():
                    resolved = _resolve_repo_path(
                        repo_root,
                        evidence_path,
                        findings,
                        locale_source,
                        f"evidence.{evidence_key}",
                        "file",
                    )
                    if resolved and resolved.is_file():
                        safety_files.add(resolved)
                        if resolved.suffix == ".md":
                            markdown_files.add(resolved)
                    expected_sample_path = {
                        "sample_input": f"{expected_locale_examples}/sample-input.md",
                        "sample_output": f"{expected_locale_examples}/sample-output.md",
                    }.get(evidence_key)
                    if expected_sample_path and evidence_path != expected_sample_path:
                        findings.append(
                            Finding(
                                "ERROR",
                                "sample-evidence-path",
                                locale_source,
                                f"evidence.{evidence_key} must be {expected_sample_path}",
                            )
                        )
                if locale_rank is not None and locale_rank >= STATUS_RANK["sampled"]:
                    for key in ("sample_input", "sample_output"):
                        if key not in evidence:
                            findings.append(
                                Finding(
                                    "ERROR",
                                    "sample-evidence",
                                    locale_source,
                                    f"{locale_status} requires evidence.{key}",
                                )
                            )
                if (
                    locale_rank is not None
                    and locale_rank >= STATUS_RANK["trial-validated"]
                    and not (TRIAL_EVIDENCE_KEYS & set(evidence))
                ):
                    findings.append(
                        Finding(
                            "ERROR",
                            "trial-evidence",
                            locale_source,
                            f"{locale_status} requires trial output or trial note",
                        )
                    )
            ready_without_validated_locales = (
                variant_status == "ready"
                and locale_ranks
                and min(locale_ranks) < STATUS_RANK["trial-validated"]
            )
            status_above_locales = (
                variant_status != "ready"
                and locale_ranks
                and rank is not None
                and rank > min(locale_ranks)
            )
            if ready_without_validated_locales or status_above_locales:
                findings.append(
                    Finding(
                        "ERROR",
                        "variant-status-aggregation",
                        variant_source,
                        "variant status is higher than its least-mature required locale",
                    )
                )
        skill_rank = _status_rank(status)
        if variant_ranks and skill_rank is not None and skill_rank > min(variant_ranks):
            findings.append(
                Finding(
                    "ERROR",
                    "skill-status-aggregation",
                    source,
                    "Skill status is higher than its least-mature implemented variant",
                )
            )

    if skill_filter is None:
        skills_root = repo_root / "skills"
        family_roots = (
            sorted(
                (path for path in skills_root.iterdir() if path.is_dir()),
                key=lambda path: path.name,
            )
            if skills_root.is_dir()
            else []
        )
        for family_root in family_roots:
            for package_root in sorted(
                (path for path in family_root.iterdir() if path.is_dir()),
                key=lambda path: path.name,
            ):
                if not any(package_root.glob("*/SKILL.md")):
                    continue
                relative_package = _relative(repo_root, package_root)
                if relative_package not in registered_package_roots:
                    findings.append(
                        Finding(
                            "ERROR",
                            "unregistered-package",
                            relative_package,
                            "implemented Skill package is not registered in catalog/skills.yaml",
                        )
                    )

    scan_roots = {repo_root} if skill_filter is None else safety_roots
    safety_files.update(_collect_public_text_files(repo_root, scan_roots, findings))
    _check_markdown_links(repo_root, sorted(markdown_files), findings)
    safety_files.update(markdown_files)
    _check_public_safety(repo_root, sorted(safety_files), findings)
    checks["markdown_files"] = len(markdown_files)
    checks["safety_files"] = len(safety_files)
    selected_names = [
        f"{skill.get('id')}:{skill.get('slug')}" for skill in selected
    ]
    findings.sort(key=lambda item: (item.level != "ERROR", item.code, item.path))
    return ValidationReport(str(repo_root), selected_names, findings, checks)


def _report_dict(report: ValidationReport) -> dict[str, Any]:
    return {
        "repo_root": "<repo-root>",
        "selected_skills": report.selected_skills,
        "summary": {
            "errors": len(report.errors),
            "warnings": len(report.warnings),
        },
        "checks": report.checks,
        "findings": [dataclasses.asdict(finding) for finding in report.findings],
        "manual_review_required": [
            "behavioral locale parity",
            "nuanced public-safety and screenshot review",
            "trial metadata completeness, semantics, authenticity, and status claims",
        ],
    }


def format_text(report: ValidationReport) -> str:
    lines = [
        "Agentarium deterministic validation",
        f"Selected: {', '.join(report.selected_skills) or '(none)'}",
        f"Errors: {len(report.errors)}",
        f"Warnings: {len(report.warnings)}",
    ]
    for key, value in report.checks.items():
        lines.append(f"{key}: {value}")
    if report.findings:
        lines.append("")
        lines.append("Findings:")
        for finding in report.findings:
            lines.append(
                f"- [{finding.level}] {finding.code} {finding.path}: {finding.message}"
            )
    lines.extend(
        [
            "",
            "Manual review still required: behavioral locale parity, nuanced",
            "public-safety/screenshot review, and trial metadata/semantics/authenticity.",
        ]
    )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run deterministic checks against an Agentarium repository."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="Agentarium repository root. Defaults to the current directory.",
    )
    parser.add_argument(
        "--skill",
        help="Optional Skill ID or slug. Without it, validate every catalog entry.",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return non-zero for warnings as well as errors.",
    )
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    report = validate_repository(args.repo_root, args.skill)
    if args.format == "json":
        print(json.dumps(_report_dict(report), ensure_ascii=False, indent=2))
    else:
        print(format_text(report))
    if report.errors or (args.strict and report.warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
