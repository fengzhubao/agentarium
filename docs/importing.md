# Importing Skills

Different agent tools handle Skills differently. This repository keeps the Skill packages as plain directories so they can be copied or imported manually.

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

The directory you import should contain:

```text
SKILL.md
references/
```

For multi-language Skills, choose one locale directory at a time.

