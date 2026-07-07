# Localization Policy

Agentarium publishes Skills by package family and language.

Language localization is separate from package-family placement. A shared Skill should keep behavior aligned across locales and, where possible, across future tool-specific variants. Skill packages under `skills/shared/...` and examples under `examples/shared/...` are canonical tool-agnostic package examples.

This policy applies to Skill instructions, examples, catalog language metadata, and docs that describe language requirements.

## Directory Rule

Use this structure:

```text
skills/<package-family>/<skill-name>/<locale>/
examples/<package-family>/<skill-name>/<locale>/
```

Examples:

```text
skills/shared/<skill-name>/zh_CN/
skills/shared/<skill-name>/en_US/
examples/shared/<skill-name>/zh_CN/
examples/shared/<skill-name>/en_US/
```

## Required Languages

Every implemented public Skill must include at least:

- `zh_CN`: Simplified Chinese
- `en_US`: English

Additional languages can be added later, for example:

- `ja_JP`
- `ko_KR`
- `fr_FR`
- `de_DE`

This requirement is also enforced at the repository-instruction level in `AGENTS.md` and tracked in `catalog/skills.yaml`. Candidate Skills may be registered before these packages exist.

## Consistency Rules

- Keep the same Skill name across locales unless the target tool requires otherwise.
- Keep behavior equivalent across languages.
- Locale-specific examples may differ, but the safety boundaries and output requirements should remain aligned.
- Agent/model fit should remain behaviorally aligned across locales. Do not describe a Skill as suitable for stronger or broader model capabilities in one locale unless the difference is intentional and documented.
- Before changing either `zh_CN` or `en_US`, read both locale `SKILL.md` files and their linked references or examples.
- When updating one locale, check whether the other locales need the same update.
- When adding a Skill to `catalog/skills.yaml`, list `zh_CN` and `en_US` under `required_locales`.
- Locale exceptions must follow `catalog/status-policy.md`; do not introduce undefined statuses.
- Avoid hard-coding one locale's output format as the default in another locale. If a Chinese contest requires Chinese headings, label that section as a Chinese-channel template inside the English version.

## Link Rule

When linking a Skill from a community post, link to the locale-specific directory. Shared package example:

```text
https://github.com/<owner>/<repo>/tree/main/skills/shared/worktree-conductor/zh_CN
```

Current TRAE package example:

```text
https://github.com/<owner>/<repo>/tree/main/skills/trae/solo-project-publisher/zh_CN
```

If the audience is mixed, link to the Skill root and list available languages:

```text
https://github.com/<owner>/<repo>/tree/main/skills/trae/solo-project-publisher
```
