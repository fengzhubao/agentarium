# Agent Context Sync

Agent Context Sync is a shared workflow Skill for keeping one shared instruction source aligned across files such as `AGENTS.md`, `CLAUDE.md`, and repository-specific agent rule files without overwriting tool-specific content.

It uses a deterministic, zero-third-party-dependency Python script with three modes:

- `check`: report drift without writing.
- `diff`: print the proposed managed-block changes without writing.
- `sync`: update only the marked managed block after explicit authorization.

## Languages

- `zh_CN`: Simplified Chinese
- `en_US`: English

## Package And Tool Support

- Current implemented package: shared package under `skills/shared/agent-context-sync/`.
- Intended workflow targets: TRAE, Codex, Claude, Cursor, and other repository agents that use text instruction files.
- The package is tool-neutral. Target filenames are repository configuration, not hard-coded behavior.

## Agent / Model Fit

- Suitable for agents that can inspect repository files, run a local Python script, review diffs, and preserve tool-specific instruction boundaries.
- Best with models that can distinguish shared policy from tool-specific rules and explain synchronization risk before writing.
- Not suitable for chat-only models without repository file access.
- Not suitable for agents that would replace whole instruction files instead of maintaining the managed block.

## Safety Boundary

- Configuration paths must remain inside the repository.
- The source and targets must be UTF-8 text.
- Malformed or duplicate markers stop the run before any target is written.
- Existing content outside the managed block is preserved.
- `check` and `diff` are read-only; use `sync` only when the user authorized changes.

## Current Status

Ready. Both locale import roots completed public-safe Codex trials on 2026-07-16 using the full `check → diff → sync → check` workflow. A follow-up Windows multi-repository pilot preserved tool-specific content, created missing targets, exposed and verified a legacy redirected-output encoding fix, and ended with zero drift. Nineteen regression tests pass in the cross-platform suite. This release applies to the canonical shared package; it does not claim tool-specific TRAE, Claude, or Cursor execution.

See `STATUS.md` for readiness details.
