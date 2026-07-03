# Publishing Guide

## Goal

Each Skill in this repository should be easy to inspect, copy, import, and discuss from a public link.

Agents working in this repository should read `AGENTS.md` first, then use `catalog/skills.yaml` as the Skill registry and `catalog/status-policy.md` for status rules.

This guide applies to Skill packages, examples, catalog metadata, and related repository docs.

## Repository Organization

Skills are organized by tool family, Skill name, and language:

```text
skills/<tool>/<skill-name>/<locale>/
examples/<tool>/<skill-name>/<locale>/
```

Examples:

```text
skills/trae/solo-project-publisher/zh_CN/
skills/trae/solo-project-publisher/en_US/
examples/trae/solo-project-publisher/zh_CN/
examples/trae/solo-project-publisher/en_US/
```

Use these tool family names unless there is a strong reason to add another:

- `trae`
- `claude`
- `codex`

## Recommended Skill Package

```text
skills/<tool>/<skill-name>/<locale>/
├── SKILL.md
└── references/  # optional; include only when SKILL.md links supporting files
    └── ...
```

Optional supporting material:

```text
examples/<tool>/<skill-name>/<locale>/
docs/
```

## Language Requirement

Every implemented public Skill must include at least:

- `zh_CN`
- `en_US`

Other locales can be added later. See `docs/localization.md`.

Candidate Skills may be registered before implementation, but implemented public Skills should not be marked `ready` until both required locales exist.

## Before Publishing

1. Keep the Skill package small and focused.
2. Add a clear description in `SKILL.md` frontmatter.
3. Move detailed templates or checklists into `references/` when such supporting files are needed.
4. Add redacted example inputs and outputs under `examples/<tool>/<skill-name>/<locale>/`.
5. Add a Skill root `README.md` and `STATUS.md` when the Skill has multiple languages.
6. Keep Chinese and English versions behaviorally aligned.
7. Register or update the Skill in `catalog/skills.yaml`.
8. Run a public-safety check.
9. Link directly to the correct Skill directory from community posts.
10. Complete or review the checklist in `docs/skill-completeness.md` before marking the Skill ready.

Use only statuses defined in `catalog/status-policy.md`.

## Link Format

For SOLO Project Publisher Chinese version:

```text
https://github.com/fengzhubao/agentarium/tree/main/skills/trae/solo-project-publisher/zh_CN
```

For the Skill root with all languages:

```text
https://github.com/fengzhubao/agentarium/tree/main/skills/trae/solo-project-publisher
```

## Versioning

For now, use normal Git commits. If a Skill becomes widely reused, add tags or release notes later.
