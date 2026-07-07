# Publishing Guide

## Goal

Each Skill in this repository should be easy to inspect, copy, import, and discuss from a public link.

Agents working in this repository should read `AGENTS.md` first, then use `catalog/skills.yaml` as the Skill registry and `catalog/status-policy.md` for status rules.

This guide applies to Skill packages, examples, catalog metadata, and related repository docs.

Design shared workflows first and tool-specific package variants second. TRAE SOLO contest wording belongs only in Skills or examples where it is intentionally part of the target use case, not in unrelated shared workflows.

## Repository Organization

Skills are organized by package family, Skill name, and language:

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

Use `shared` for canonical tool-agnostic packages. Use a tool-specific package family only when the Skill needs tool-specific import behavior, UI assumptions, runtime constraints, screenshots, or marketplace links.

Use these package family names unless there is a strong reason to add another:

- `shared`
- `trae`
- `claude`
- `codex`

## Recommended Skill Package

```text
skills/<package-family>/<skill-name>/<locale>/
├── SKILL.md
└── references/  # optional; include only when SKILL.md links supporting files
    └── ...
```

Optional supporting material:

```text
examples/<package-family>/<skill-name>/<locale>/
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
4. Add redacted example inputs and outputs under `examples/<package-family>/<skill-name>/<locale>/`.
5. Add a Skill root `README.md` and `STATUS.md` when the Skill has multiple languages.
6. Keep Chinese and English versions behaviorally aligned.
7. Register or update the Skill in `catalog/skills.yaml`.
8. Run a public-safety check.
9. Link directly to the correct Skill directory from community posts.
10. Complete or review the checklist in `docs/skill-completeness.md` before marking the Skill ready.

For shared Skills, keep the core workflow tool-neutral. Put tool-specific import steps, UI references, screenshots, marketplace links, and runtime constraints in the relevant variant docs or examples.

Document agent/model fit before publishing. Use capability requirements instead of fragile model-name claims: file access, repository inspection, command/tool use, code reasoning, long-context comparison, security review, writing quality, or public-safety judgment. Only mention a specific model or agent version when trial evidence records it.

Use only statuses defined in `catalog/status-policy.md`.

## Link Format

For a shared package such as Worktree Conductor Chinese version:

```text
https://github.com/<owner>/<repo>/tree/main/skills/shared/worktree-conductor/zh_CN
```

For a current TRAE-packaged Skill such as SOLO Project Publisher Chinese version:

```text
https://github.com/<owner>/<repo>/tree/main/skills/trae/solo-project-publisher/zh_CN
```

For the Skill root with all languages:

```text
https://github.com/<owner>/<repo>/tree/main/skills/trae/solo-project-publisher
```

## Versioning

For now, use normal Git commits. If a Skill becomes widely reused, add tags or release notes later.
