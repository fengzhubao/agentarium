# Worktree Conductor

Worktree Conductor is a shared workflow Skill for planning parallel development across multiple Git worktrees. The current importable package is the canonical shared package.

It helps a developer split a larger repository task into clear branches, worktree paths, file ownership boundaries, shared-file risk levels, validation checks, integration order, and per-agent task prompts.

## Languages

- `zh_CN`: Simplified Chinese
- `en_US`: English

## Package And Tool Support

- Current implemented package: shared package under `skills/shared/worktree-conductor/`.
- Intended shared workflow target: TRAE, Codex, Claude, and multi-agent human workflows.
- Future tool-specific package variants should preserve the same planning behavior while adapting import paths or tool-specific runtime details.

## Agent / Model Fit

- Suitable for code-capable agents that can inspect repository structure and reason about Git branches, worktrees, file ownership, and validation commands.
- Best with models that handle multi-step planning, conflict-risk analysis, command-safety review, and precise task handoff prompts.
- Not suitable for chat-only models without repository context when the user needs an executable worktree plan.
- Not suitable for agents that may run destructive Git commands without explicit user approval.

## Main Use Cases

- Multiple agents or developers working on one repository.
- A monorepo or multi-module repository with shared contracts, generated outputs, or shared docs.
- Planning safe `git worktree` based development before code changes begin.
- Preparing a merge and validation plan for parallel feature branches.

## Current Status

Trial-validated.

Both locale import roots were run in Codex on 2026-07-16 against the real Agent Context Sync planning task. The trials detected the dirty base worktree, protected shared files, and produced behaviorally aligned plans without running mutating Git commands. This validates the canonical shared planning workflow in Codex; it does not claim TRAE- or Claude-specific execution.

See `STATUS.md` for readiness details.
