# Importing Skills

Different agent tools handle Skills differently. This repository keeps the Skill packages as plain directories so they can be copied or imported manually.

For the repository's complete Skill list, read `catalog/skills.yaml`. For agent-facing editing rules, read `AGENTS.md`.

For editing or publishing work, also read `catalog/status-policy.md`, `docs/publishing.md`, `docs/localization.md`, `docs/safety.md`, and `docs/skill-completeness.md`.

When automating imports from the catalog, use `variants[].locale_roots.<locale>.import_root`. A multi-locale package root is not itself importable unless it directly contains `SKILL.md`.

## TRAE

For TRAE SOLO, use the locale-specific Skill directory:

```text
skills/trae/solo-project-publisher/zh_CN/
```

or:

```text
skills/trae/solo-project-publisher/en_US/
```

If TRAE expects a folder containing `SKILL.md`, import or copy the locale directory itself, not the parent `solo-project-publisher/` directory.

## Codex

Codex-style Skills also expect a `SKILL.md` at the Skill root. Use a locale directory as the root if importing this Skill into a Codex-compatible environment.

## Claude

Claude-specific Skills should live under:

```text
skills/claude/<skill-name>/<locale>/
```

No Claude-specific Skill is published yet.

## General Rule

The directory you import must contain:

```text
SKILL.md
```

It may contain:

```text
references/
```

Do not create an empty `references/` directory only to satisfy import rules.

For multi-language Skills, choose one locale directory at a time. Repository maintenance still requires reading and keeping both `zh_CN` and `en_US` aligned.

