# Localization Policy

Agentarium publishes Skills by tool family and language.

## Directory Rule

Use this structure:

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

## Required Languages

Every public Skill should include at least:

- `zh_CN`: Simplified Chinese
- `en_US`: English

Additional languages can be added later, for example:

- `ja_JP`
- `ko_KR`
- `fr_FR`
- `de_DE`

## Consistency Rules

- Keep the same Skill name across locales unless the target tool requires otherwise.
- Keep behavior equivalent across languages.
- Locale-specific examples may differ, but the safety boundaries and output requirements should remain aligned.
- When updating one locale, check whether the other locales need the same update.
- Avoid hard-coding one locale's output format as the default in another locale. If a Chinese contest requires Chinese headings, label that section as a Chinese-channel template inside the English version.

## Link Rule

When linking a Skill from a community post, link to the locale-specific directory:

```text
https://github.com/fengzhubao/agentarium/tree/main/skills/trae/solo-project-publisher/zh_CN
```

If the audience is mixed, link to the Skill root and list available languages:

```text
https://github.com/fengzhubao/agentarium/tree/main/skills/trae/solo-project-publisher
```
