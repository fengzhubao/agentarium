# Agentarium

Agentarium is a public collection of reusable agent workflows and Skills.

The repository is organized by agent/tool family first, then by Skill name, then by language. It starts with TRAE SOLO contest work, but the structure is intentionally broad enough for TRAE, Claude, Codex, MCP agents, and related workflows.

For agent-facing repository instructions, read `AGENTS.md` first. For the machine-readable Skill registry, see `catalog/skills.yaml`.

## Implemented Skills

| ID | Tool | Skill | Scope | Languages | Status | Purpose |
| --- | --- | --- | --- | --- | --- | --- |
| SKL-0001 | TRAE | SOLO Project Publisher | shared | `zh_CN`, `en_US` | `zh_CN` trial validated, `en_US` draft | Turn real project evidence into a publishable community post or project report. |
| SKL-0002 | TRAE | Worktree Conductor | shared | `zh_CN`, `en_US` | Draft | Plan safe parallel development across Git worktrees, branches, file ownership boundaries, and integration order. |

Planned and candidate Skills are tracked in `catalog/skills.yaml`.

## Repository Layout

```text
agentarium/
├── AGENTS.md
├── catalog/
│   ├── README.md
│   ├── skills.yaml
│   └── status-policy.md
├── skills/
│   └── trae/
│       ├── solo-project-publisher/
│       │   ├── zh_CN/
│       │   └── en_US/
│       └── worktree-conductor/
│           ├── zh_CN/
│           └── en_US/
├── examples/
│   └── trae/
│       ├── solo-project-publisher/
│       │   ├── zh_CN/
│       │   └── en_US/
│       └── worktree-conductor/
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

Open the tool and language directory you need, then import or copy that Skill into your agent tool if it supports local Skill folders.

For the Chinese TRAE version of SOLO Project Publisher:

```text
skills/trae/solo-project-publisher/zh_CN/
```

For the English TRAE version:

```text
skills/trae/solo-project-publisher/en_US/
```

Each locale directory contains its own `SKILL.md` and any runtime references.

The Skill expects a target project, a publishing channel, a public-safety boundary, and any available evidence such as screenshots, command outputs, generated files, or links.

For the Chinese TRAE version of Worktree Conductor:

```text
skills/trae/worktree-conductor/zh_CN/
```

For the English TRAE version:

```text
skills/trae/worktree-conductor/en_US/
```

The Skill expects a repository, an overall development goal, known modules/shared files, desired parallelism, and validation commands.

For importing details, see `docs/importing.md`.

For Skill-specific status and notes, see:

```text
skills/trae/solo-project-publisher/README.md
skills/trae/solo-project-publisher/STATUS.md
skills/trae/worktree-conductor/README.md
skills/trae/worktree-conductor/STATUS.md
```

Before calling a Skill complete, check `docs/skill-completeness.md`.

When adding, renaming, or changing the readiness of a Skill, update `catalog/skills.yaml` and the Skill root `STATUS.md`.

## Localization

Each public Skill should include at least:

- `zh_CN`: Simplified Chinese
- `en_US`: English

Additional language versions can be added later under the same Skill directory. See `docs/localization.md`.

## Public Safety

Do not publish credentials, private keys, tokens, cookies, internal hostnames, private repository links, customer data, or machine-specific secrets in this repository.

See `docs/safety.md` before adding a new Skill.

## License

MIT License. See `LICENSE`.
