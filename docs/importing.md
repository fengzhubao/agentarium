# Importing Skills

Different agent tools handle Skills differently. This repository keeps the Skill packages as plain directories so they can be copied or imported manually.

For the repository's complete Skill list, read `catalog/skills.yaml`. For agent-facing editing rules, read `AGENTS.md`.

For editing or publishing work, also read `catalog/status-policy.md`, `docs/publishing.md`, `docs/localization.md`, `docs/safety.md`, and `docs/skill-completeness.md`.

When automating imports from the catalog, use `variants[].locale_roots.<locale>.import_root`. A multi-locale package root is not itself importable unless it directly contains `SKILL.md`.

## Shared Workflow Vs Variant

Agentarium Skills should be understood as reusable workflows first and package-family variants second. A tool-agnostic shared Skill should live under `skills/shared/...`. Tool-specific packages belong under `skills/trae/...`, `skills/codex/...`, `skills/claude/...`, or another package family only when the package needs tool-specific import behavior or runtime instructions.

Use `supported_tools` in `catalog/skills.yaml` to find package families that exist today. Use `target_tools` to understand intended agent-tool support.

Also check `model_fit` before importing a Skill. It describes whether the Skill expects capabilities such as repository file access, Git or command reasoning, long-context comparison, security review, or public-writing quality. A chat-only model can sometimes discuss a Skill, but it should not be treated as able to execute repository, audit, CI, or safety workflows without the required file/tool context.

## Shared Package

For tool-agnostic Skills such as Worktree Conductor and Skill Quality Auditor, use the locale-specific shared directory:

```text
skills/shared/worktree-conductor/zh_CN/
skills/shared/skill-quality-auditor/en_US/
```

If an agent tool can import a plain folder containing `SKILL.md`, start with the shared package before creating a tool-specific variant.

## TRAE Variant

For the current SKL-0001 TRAE package, use the locale-specific Skill directory:

```text
skills/trae/solo-project-publisher/zh_CN/
```

If TRAE expects a folder containing `SKILL.md`, import or copy the locale directory itself, not the parent Skill package directory.

## Codex

Codex-style Skills also expect a `SKILL.md` at the Skill root. Use a locale directory as the root if importing a compatible Skill into a Codex-compatible environment.

No Codex-specific package variant is published yet. For shared Skills, keep the workflow intent aligned when adding one under `skills/codex/<skill-name>/<locale>/`.

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
