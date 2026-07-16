# Skill Catalog

This directory tracks Agentarium Skills by stable global ID, status, scope, package support, target agent-tool support, and repository path.

Catalog entries describe reusable workflows first and package-family variants second. `scope` describes whether the workflow can apply across tools; `supported_tools` lists implemented package families such as `shared` or `trae`; `target_tools` lists intended or planned agent-tool support. Use `shared` for canonical tool-agnostic packages.

Use `model_fit` in `skills.yaml` to describe the agent and model capabilities a Skill expects. Prefer capability language such as repository access, tool use, long-context reasoning, code reasoning, safety review, or writing quality. Do not imply that a Skill is validated for a specific model brand or version unless trial evidence records that fact.

Use `skills.yaml` as the machine-readable registry. Use this file as the human-facing overview.

## ID Policy

Skill IDs are global and stable. They must match:

```text
^SKL-[0-9]{4}$
```

Examples:

```text
SKL-0001
SKL-0002
SKL-0003
```

Do not encode the package family or tool family in the ID. A workflow may start as a shared package and later gain TRAE, Codex, or Claude variants while keeping the same ID.

## Path Model

`package_root` points to the multi-locale Skill package directory, for example:

```text
skills/shared/worktree-conductor
```

`import_root` points to one locale-specific importable Skill directory. It must contain `SKILL.md` directly:

```text
skills/shared/worktree-conductor/zh_CN
skills/shared/worktree-conductor/en_US
```

Do not use a parent package directory as an import root unless it directly contains `SKILL.md`.

## Current Registry

| ID | Slug | Scope | Status | Target Tools | Supported Packages | Purpose |
| --- | --- | --- | --- | --- | --- | --- |
| SKL-0001 | `solo-project-publisher` | shared | draft | trae | trae | Turn real project evidence into a publishable community post or report. `zh_CN` is trial-validated; `en_US` is draft. |
| SKL-0002 | `worktree-conductor` | shared | sampled | trae, codex, claude | shared | Plan safe parallel development across Git worktrees and agents. Shared package is sampled; real target-agent trial evidence is pending. |
| SKL-0003 | `skill-quality-auditor` | shared | trial-validated | trae, codex, claude | shared | Audit Skill package quality, safety, examples, and catalog alignment. Both locale packages have public-safe Codex trial records from 2026-07-16. |
| SKL-0004 | `agent-context-sync` | shared | candidate | trae, claude, codex | none | Keep cross-agent instruction files aligned from a single source of truth. |
| SKL-0005 | `ci-failure-triage` | shared | candidate | trae, claude, codex | none | Triage CI failures and produce minimal fix plans. |
| SKL-0006 | `mcp-risk-review` | shared | candidate | trae, claude, codex | none | Review MCP server permissions, data exposure, and safety risks before adoption. |

## Agent And Model Fit

`supported_tools` describes package families that exist today. `target_tools` describes intended agent-tool support. `model_fit` describes the underlying capability profile needed inside that agent environment. For example, a repository audit Skill needs file access and structured review ability; a CI triage Skill needs log analysis and code reasoning; a publishing Skill needs evidence synthesis and public-safety judgment.

When adding a Skill, avoid hard-coding current model names unless the Skill has been trial-validated on that specific model and the evidence is public-safe.

## Required Updates

Update `skills.yaml` when:

- Adding a new Skill idea.
- Creating a new Skill package.
- Adding a new package variant or tool-specific variant.
- Changing status.
- Moving a Skill or examples directory.
- Deprecating a Skill.

For status definitions, see `status-policy.md`.

For import automation, use `variants[].locale_roots.<locale>.import_root`, not the multi-locale package root.
