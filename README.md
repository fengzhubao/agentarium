# Agentarium

Agentarium is a public collection of reusable agent workflows and Skills.

Agentarium is meant to be cross-agent by default: catalog entries describe reusable workflows first, and package-family directories describe importable packages second. The first published package came from TRAE SOLO contest work, but TRAE SOLO is not the default target, template, or direction for unrelated Skills.

The repository is organized by package family first, then by Skill name, then by language. Use `skills/shared/` for canonical tool-agnostic packages. Use `skills/trae/`, `skills/codex/`, or `skills/claude/` only when a package needs tool-specific import behavior, UI assumptions, or runtime instructions.

For agent-facing repository instructions, read `AGENTS.md` first. For the machine-readable Skill registry, see `catalog/skills.yaml`.

## Implemented Skills

| ID | Implemented Package(s) | Target Tools | Skill | Scope | Languages | Status | Purpose |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SKL-0001 | `trae` | `trae` | SOLO Project Publisher | shared | `zh_CN`, `en_US` | `zh_CN` trial validated, `en_US` draft | Turn real project evidence into a publishable community post or project report. |
| SKL-0002 | `shared` | `trae`, `codex`, `claude` | Worktree Conductor | shared | `zh_CN`, `en_US` | Ready | Plan safe parallel development across Git worktrees, branches, file ownership boundaries, and integration order. |
| SKL-0003 | `shared` | `trae`, `codex`, `claude` | Skill Quality Auditor | shared | `zh_CN`, `en_US` | Ready | Audit Skill package quality, catalog alignment, locale parity, evidence, links, and public-safety risk. Includes an independently importable deterministic validator in both locales. |
| SKL-0004 | `shared` | `trae`, `codex`, `claude` | Agent Context Sync | shared | `zh_CN`, `en_US` | Ready | Check, diff, and synchronize one shared rule source across agent instruction files without overwriting tool-specific content. |

Planned and candidate Skills are tracked in `catalog/skills.yaml`.

## Agent And Model Fit

Agentarium records two different compatibility layers:

- Package and agent support: `supported_tools` lists package families that exist today, such as `shared` or `trae`; `target_tools` lists planned agent-tool support such as TRAE, Codex, or Claude.
- Model capability: `model_fit` describes what the underlying model or agent runtime must be good at, such as file access, repository inspection, Git reasoning, long-context comparison, code reasoning, safety review, or public writing.

Do not treat a Skill as validated for a specific model brand or version unless its `STATUS.md` or evidence explicitly records that trial.

## Repository Layout

```text
agentarium/
├── AGENTS.md
├── catalog/
│   ├── README.md
│   ├── skills.yaml
│   └── status-policy.md
├── skills/
│   ├── shared/
│   │   ├── agent-context-sync/
│   │   │   ├── zh_CN/
│   │   │   └── en_US/
│   │   ├── worktree-conductor/
│   │   │   ├── zh_CN/
│   │   │   └── en_US/
│   │   └── skill-quality-auditor/
│   │       ├── zh_CN/
│   │       └── en_US/
│   └── trae/
│       └── solo-project-publisher/
│           ├── zh_CN/
│           └── en_US/
├── examples/
│   ├── shared/
│   │   ├── agent-context-sync/
│   │   │   ├── zh_CN/
│   │   │   └── en_US/
│   │   ├── worktree-conductor/
│   │   │   ├── zh_CN/
│   │   │   └── en_US/
│   │   └── skill-quality-auditor/
│   │       ├── zh_CN/
│   │       └── en_US/
│   └── trae/
│       └── solo-project-publisher/
│           ├── zh_CN/
│           └── en_US/
└── docs/
    ├── importing.md
    ├── localization.md
    ├── publishing.md
    ├── skill-completeness.md
    └── safety.md
```

## Usage

Open the package and language directory you need, then import or copy that Skill into your agent tool if it supports local Skill folders. Shared packages live under `skills/shared/`. Tool-specific variants can later be added under `skills/trae/`, `skills/codex/`, `skills/claude/`, or another package family without changing the stable catalog ID.

For the Chinese import root of the shared Worktree Conductor package:

```text
skills/shared/worktree-conductor/zh_CN/
```

For the English import root of the shared Worktree Conductor package:

```text
skills/shared/worktree-conductor/en_US/
```

The Skill expects a repository, an overall development goal, known modules/shared files, desired parallelism, and validation commands.

For the Chinese import root of the shared Skill Quality Auditor package:

```text
skills/shared/skill-quality-auditor/zh_CN/
```

For the English import root of the shared Skill Quality Auditor package:

```text
skills/shared/skill-quality-auditor/en_US/
```

The Skill expects a Skill ID or package path, target status or review goal, and permission boundaries for read-only audit versus fixes.

For the Chinese import root of the shared Agent Context Sync package:

```text
skills/shared/agent-context-sync/zh_CN/
```

For the English import root:

```text
skills/shared/agent-context-sync/en_US/
```

The Skill expects a repository-local JSON config, one shared Markdown source, target instruction files, and explicit authorization before write-mode synchronization.

For the Chinese TRAE package of SOLO Project Publisher:

```text
skills/trae/solo-project-publisher/zh_CN/
```

For the English TRAE package:

```text
skills/trae/solo-project-publisher/en_US/
```

Each locale directory contains its own `SKILL.md` and any runtime references.

SOLO Project Publisher expects a target project, a publishing channel, a public-safety boundary, and any available evidence such as screenshots, command outputs, generated files, or links.

For importing details, see `docs/importing.md`.

For Skill-specific status and notes, see:

```text
skills/trae/solo-project-publisher/README.md
skills/trae/solo-project-publisher/STATUS.md
skills/shared/worktree-conductor/README.md
skills/shared/worktree-conductor/STATUS.md
skills/shared/skill-quality-auditor/README.md
skills/shared/skill-quality-auditor/STATUS.md
skills/shared/agent-context-sync/README.md
skills/shared/agent-context-sync/STATUS.md
```

Before calling a Skill complete, check `docs/skill-completeness.md`.

When adding, renaming, or changing the readiness of a Skill, update `catalog/skills.yaml` and the Skill root `STATUS.md`.

## Localization

Each public Skill should include at least:

- `zh_CN`: Simplified Chinese
- `en_US`: English

Additional language versions can be added later under the same Skill directory. See `docs/localization.md`.

## Public Safety

Do not publish credentials, private keys, tokens, cookies, internal hostnames, private repository links, customer data, personal information, account identifiers, or machine-specific secrets in this repository.

See `docs/safety.md` before adding a new Skill.

## License

MIT License. See `LICENSE`.
