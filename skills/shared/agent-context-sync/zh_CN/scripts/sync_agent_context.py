#!/usr/bin/env python3
"""Synchronize one shared Markdown source into managed target-file blocks."""

from __future__ import annotations

import argparse
import codecs
import difflib
import json
import os
import stat
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Sequence


DEFAULT_CONFIG = ".agent-context-sync.json"
START_MARKER = "<!-- agent-context-sync:start -->"
END_MARKER = "<!-- agent-context-sync:end -->"
FORBIDDEN_BASENAMES = {
    ".netrc",
    ".npmrc",
    ".pypirc",
    "auth.json",
    "credentials",
    "credentials.json",
    "id_ed25519",
    "id_rsa",
}
FORBIDDEN_SUFFIXES = {".key", ".p12", ".pem", ".pfx"}


def _configure_cli_streams() -> None:
    """Emit exact Unicode output even under legacy redirected code pages."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if not callable(reconfigure):
            continue
        try:
            reconfigure(encoding="utf-8")
        except (OSError, ValueError):
            pass


class SyncError(Exception):
    """A configuration or target-state error that prevents safe synchronization."""


@dataclass(frozen=True)
class SyncConfig:
    source: str
    targets: tuple[str, ...]


@dataclass(frozen=True)
class TextFile:
    text: str
    has_bom: bool


@dataclass(frozen=True)
class TargetPlan:
    relative_path: str
    path: Path
    current: str
    expected: str
    has_bom: bool
    existed: bool
    reason: str | None

    @property
    def changed(self) -> bool:
        return self.current != self.expected


def _normalize_relative_path(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SyncError(f"{label} must be a non-empty string")

    raw = value.strip()
    normalized = raw.replace("\\", "/")
    posix = PurePosixPath(normalized)
    windows = PureWindowsPath(raw)

    if posix.is_absolute() or windows.is_absolute() or windows.drive:
        raise SyncError(f"{label} must be repository-relative: {raw}")
    if any(part in {"", ".", ".."} for part in posix.parts):
        raise SyncError(f"{label} must not contain empty, dot, or parent segments: {raw}")

    return posix.as_posix()


def _resolve_inside(repo_root: Path, relative_path: str, label: str) -> Path:
    parts = PurePosixPath(relative_path).parts
    candidate = repo_root.joinpath(*parts).resolve(strict=False)
    try:
        candidate.relative_to(repo_root)
    except ValueError as exc:
        raise SyncError(f"{label} resolves outside the repository: {relative_path}") from exc
    return candidate


def _reject_sensitive_path(relative_path: str, label: str) -> None:
    parts = [part.casefold() for part in PurePosixPath(relative_path).parts]
    name = parts[-1]
    suffix = PurePosixPath(name).suffix
    if ".git" in parts:
        raise SyncError(f"{label} must not point inside .git: {relative_path}")
    if (
        name == ".env"
        or name.startswith(".env.")
        or name in FORBIDDEN_BASENAMES
        or suffix in FORBIDDEN_SUFFIXES
    ):
        raise SyncError(f"{label} uses a forbidden sensitive filename: {relative_path}")


def _read_utf8(path: Path, label: str) -> TextFile:
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise SyncError(f"cannot read {label}: {exc}") from exc

    has_bom = data.startswith(codecs.BOM_UTF8)
    payload = data[len(codecs.BOM_UTF8) :] if has_bom else data
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SyncError(f"{label} is not valid UTF-8: {path.name}") from exc
    if "\x00" in text:
        raise SyncError(f"{label} contains a NUL byte: {path.name}")
    return TextFile(text=text, has_bom=has_bom)


def load_config(repo_root: Path, config_relative: str) -> SyncConfig:
    _reject_sensitive_path(config_relative, "config path")
    config_path = _resolve_inside(repo_root, config_relative, "config path")
    if not config_path.is_file():
        raise SyncError(f"config file does not exist: {config_relative}")

    config_text = _read_utf8(config_path, "config file").text
    try:
        raw = json.loads(config_text)
    except json.JSONDecodeError as exc:
        raise SyncError(
            f"config file is not valid JSON at line {exc.lineno}, column {exc.colno}"
        ) from exc

    if not isinstance(raw, dict):
        raise SyncError("config root must be a JSON object")
    unknown = sorted(set(raw) - {"source", "targets"})
    if unknown:
        raise SyncError(f"config contains unsupported fields: {', '.join(unknown)}")

    source = _normalize_relative_path(raw.get("source"), "source")
    _reject_sensitive_path(source, "source")
    target_values = raw.get("targets")
    if not isinstance(target_values, list) or not target_values:
        raise SyncError("targets must be a non-empty JSON array")

    targets = tuple(
        _normalize_relative_path(value, f"targets[{index}]")
        for index, value in enumerate(target_values)
    )
    folded = [target.casefold() for target in targets]
    for index, target in enumerate(targets):
        _reject_sensitive_path(target, f"targets[{index}]")
    if len(folded) != len(set(folded)):
        raise SyncError("targets must be unique, including across case-insensitive filesystems")
    if source.casefold() in set(folded):
        raise SyncError("source must not also be listed as a target")
    if config_relative.casefold() in set(folded):
        raise SyncError("config file must not also be listed as a target")

    return SyncConfig(source=source, targets=targets)


def _to_lf(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _detect_newline(text: str) -> str:
    first_lf = text.find("\n")
    if first_lf == -1:
        return "\n"
    if first_lf > 0 and text[first_lf - 1] == "\r":
        return "\r\n"
    return "\n"


def _managed_block(source_lf: str, newline: str) -> str:
    body = source_lf.replace("\n", newline)
    return f"{START_MARKER}{newline}{body}{newline}{END_MARKER}"


def _marker_position(text: str, marker: str, label: str) -> tuple[int, int] | None:
    count = text.count(marker)
    if count == 0:
        return None
    if count != 1:
        raise SyncError(f"{label} contains {count} copies of {marker}")

    start = text.index(marker)
    before_ok = start == 0 or text[start - 1] == "\n"
    end = start + len(marker)
    after_ok = end == len(text) or text[end] in {"\r", "\n"}
    if not before_ok or not after_ok:
        raise SyncError(f"{label} must place {marker} on its own line")
    return start, end


def _append_block(text: str, block: str, newline: str) -> str:
    if not text:
        return block + newline

    result = text
    if not result.endswith(("\n", "\r")):
        result += newline
    if not result.endswith(newline + newline):
        result += newline
    return result + block + newline


def _plan_target(path: Path, relative_path: str, source_lf: str) -> TargetPlan:
    if not path.exists():
        expected = _managed_block(source_lf, "\n") + "\n"
        return TargetPlan(
            relative_path=relative_path,
            path=path,
            current="",
            expected=expected,
            has_bom=False,
            existed=False,
            reason="target missing",
        )
    if not path.is_file():
        raise SyncError(f"target is not a regular file: {relative_path}")

    target = _read_utf8(path, f"target {relative_path}")
    newline = _detect_newline(target.text)
    start = _marker_position(target.text, START_MARKER, relative_path)
    end = _marker_position(target.text, END_MARKER, relative_path)

    if (start is None) != (end is None):
        raise SyncError(f"target has an unmatched managed-block marker: {relative_path}")

    block = _managed_block(source_lf, newline)
    if start is None and end is None:
        expected = _append_block(target.text, block, newline)
        reason = "managed block missing"
    else:
        assert start is not None and end is not None
        if start[0] >= end[0]:
            raise SyncError(f"managed-block markers are out of order: {relative_path}")
        expected = target.text[: start[0]] + block + target.text[end[1] :]
        reason = None if expected == target.text else "managed block differs"

    return TargetPlan(
        relative_path=relative_path,
        path=path,
        current=target.text,
        expected=expected,
        has_bom=target.has_bom,
        existed=True,
        reason=reason,
    )


def build_plan(repo_root: Path, config_relative: str = DEFAULT_CONFIG) -> list[TargetPlan]:
    root = repo_root.resolve()
    if not root.is_dir():
        raise SyncError(f"repository root does not exist or is not a directory: {repo_root}")

    normalized_config = _normalize_relative_path(config_relative, "config path")
    config = load_config(root, normalized_config)
    source_path = _resolve_inside(root, config.source, "source")
    if not source_path.is_file():
        raise SyncError(f"source file does not exist: {config.source}")

    source = _to_lf(_read_utf8(source_path, "source file").text).strip("\n")
    if not source.strip():
        raise SyncError("source file must contain non-whitespace shared instructions")
    if START_MARKER in source or END_MARKER in source:
        raise SyncError("source file must not contain managed-block markers")

    plans: list[TargetPlan] = []
    for target in config.targets:
        target_path = _resolve_inside(root, target, f"target {target}")
        plans.append(_plan_target(target_path, target, source))
    return plans


def _atomic_write(plan: TargetPlan) -> None:
    plan.path.parent.mkdir(parents=True, exist_ok=True)
    encoded = plan.expected.encode("utf-8")
    if plan.has_bom:
        encoded = codecs.BOM_UTF8 + encoded

    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{plan.path.name}.", suffix=".tmp", dir=plan.path.parent
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(encoded)
        if plan.existed:
            os.chmod(temporary_path, stat.S_IMODE(plan.path.stat().st_mode))
        os.replace(temporary_path, plan.path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def _print_check(plans: Sequence[TargetPlan]) -> None:
    for plan in plans:
        if plan.changed:
            print(f"DRIFT {plan.relative_path}: {plan.reason}")
        else:
            print(f"OK {plan.relative_path}")
    changed = sum(plan.changed for plan in plans)
    print(f"Summary: {len(plans) - changed} synced, {changed} drifted")


def _print_diff(plans: Sequence[TargetPlan]) -> None:
    emitted = False
    for plan in plans:
        if not plan.changed:
            continue
        current = _to_lf(plan.current).splitlines(keepends=True)
        expected = _to_lf(plan.expected).splitlines(keepends=True)
        diff = "".join(
            difflib.unified_diff(
                current,
                expected,
                fromfile=f"a/{plan.relative_path}",
                tofile=f"b/{plan.relative_path}",
            )
        )
        if diff:
            print(diff, end="" if diff.endswith("\n") else "\n")
            emitted = True
    if not emitted:
        print("No drift.")


def _print_sync(plans: Sequence[TargetPlan]) -> None:
    for plan in plans:
        if plan.changed:
            _atomic_write(plan)
            print(f"UPDATED {plan.relative_path}")
        else:
            print(f"OK {plan.relative_path}")
    changed = sum(plan.changed for plan in plans)
    print(f"Summary: {changed} updated, {len(plans) - changed} already synced")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Synchronize shared agent instructions into managed target blocks."
    )
    parser.add_argument("command", choices=("check", "diff", "sync"))
    parser.add_argument("--repo-root", default=".", help="Repository root directory")
    parser.add_argument(
        "--config",
        default=DEFAULT_CONFIG,
        help=f"Repository-relative JSON config path (default: {DEFAULT_CONFIG})",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        plans = build_plan(Path(args.repo_root), args.config)
    except SyncError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.command == "check":
        _print_check(plans)
    elif args.command == "diff":
        _print_diff(plans)
    else:
        try:
            _print_sync(plans)
        except OSError as exc:
            print(f"ERROR: cannot update target: {exc}", file=sys.stderr)
            return 2

    return 1 if args.command in {"check", "diff"} and any(
        plan.changed for plan in plans
    ) else 0


if __name__ == "__main__":
    _configure_cli_streams()
    raise SystemExit(main())
