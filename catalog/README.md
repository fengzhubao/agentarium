# Skill Catalog

This directory tracks Agentarium Skills by stable global ID, status, scope, tool support, and repository path.

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

Do not encode the tool family in the ID. A workflow may start as a TRAE Skill and later gain Codex or Claude variants while keeping the same ID.

## Path Model

`package_root` points to the multi-locale Skill package directory, for example:

```text
skills/trae/solo-project-publisher
```

`import_root` points to one locale-specific importable Skill directory. It must contain `SKILL.md` directly:

```text
skills/trae/solo-project-publisher/zh_CN
skills/trae/solo-project-publisher/en_US
```

Do not use a parent package directory as an import root unless it directly contains `SKILL.md`.

## Current Registry

| ID | Slug | Scope | Status | Target Tools | Supported Tools | Purpose |
| --- | --- | --- | --- | --- | --- | --- |
| SKL-0001 | `solo-project-publisher` | shared | draft | trae | trae | Turn real project evidence into a publishable community post or report. `zh_CN` is trial-validated; `en_US` is draft. |
| SKL-0002 | `worktree-conductor` | shared | draft | trae | trae | Plan safe parallel development across Git worktrees and agents. |
| SKL-0003 | `skill-quality-auditor` | shared | candidate | trae, claude, codex | none | Audit Skill package quality, safety, examples, and catalog alignment. |
| SKL-0004 | `agent-context-sync` | shared | candidate | trae, claude, codex | none | Keep cross-agent instruction files aligned from a single source of truth. |
| SKL-0005 | `ci-failure-triage` | shared | candidate | trae, claude, codex | none | Triage CI failures and produce minimal fix plans. |
| SKL-0006 | `mcp-risk-review` | shared | candidate | trae, claude, codex | none | Review MCP server permissions, data exposure, and safety risks before adoption. |

## Required Updates

Update `skills.yaml` when:

- Adding a new Skill idea.
- Creating a new Skill package.
- Adding a new tool variant.
- Changing status.
- Moving a Skill or examples directory.
- Deprecating a Skill.

For status definitions, see `status-policy.md`.

For import automation, use `variants[].locale_roots.<locale>.import_root`, not the multi-locale package root.
