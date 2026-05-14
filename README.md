# Agentarium

Agentarium is a public collection of reusable agent workflows and Skills.

The repository is organized by agent/tool family first, then by Skill name, then by language. It starts with TRAE SOLO contest work, but the structure is intentionally broad enough for TRAE, Claude, Codex, MCP agents, and related workflows.

## Skills

| Tool | Skill | Languages | Status | Purpose |
| --- | --- | --- | --- | --- |
| TRAE | SOLO Project Publisher | `zh_CN`, `en_US` | Draft | Turn real project evidence into a publishable community post or project report. |

## Repository Layout

```text
agentarium/
├── skills/
│   ├── trae/
│   │   └── solo-project-publisher/
│   │       ├── zh_CN/
│   │       └── en_US/
│   ├── claude/
│   └── codex/
├── examples/
│   ├── trae/
│   │   └── solo-project-publisher/
│   │       ├── zh_CN/
│   │       └── en_US/
│   ├── claude/
│   └── codex/
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
skills/trae/solo-project-publisher/zh_CN/SKILL.md
```

For the English TRAE version:

```text
skills/trae/solo-project-publisher/en_US/SKILL.md
```

The Skill expects a target project, a publishing channel, a public-safety boundary, and any available evidence such as screenshots, command outputs, generated files, or links.

For importing details, see `docs/importing.md`.

For Skill-specific status and notes, see:

```text
skills/trae/solo-project-publisher/README.md
skills/trae/solo-project-publisher/STATUS.md
```

Before calling a Skill complete, check `docs/skill-completeness.md`.

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
