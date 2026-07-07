# Agent Instructions

## Project Purpose

Agentarium is a public repository of reusable agent workflows and Skills. Treat every committed file as public-facing.

Default to shared, tool-agnostic workflows when the behavior can apply across agent tools. Use `skills/shared/` for canonical packages that are not tied to one agent tool. Tool-family directories such as `skills/trae/`, `skills/codex/`, and `skills/claude/` are tool-specific import variants. TRAE SOLO is the origin context for the first published Skill, not the default direction for unrelated Skills.

## Read Order

When working in this repository, read these files before changing Skills, examples, catalog entries, or repository docs:

1. `README.md`
2. `catalog/skills.yaml`
3. `catalog/status-policy.md`
4. `docs/importing.md`
5. `docs/publishing.md`
6. `docs/localization.md`
7. `docs/safety.md`
8. `docs/skill-completeness.md`
9. For Skill work, the target Skill's `README.md`, `STATUS.md`, `zh_CN/SKILL.md`, `en_US/SKILL.md`, and linked references or examples for both locales

## Repository Layout

Use this structure:

```text
skills/<package-family>/<skill-name>/<locale>/
examples/<package-family>/<skill-name>/<locale>/
```

Supported package family names are currently:

- `shared`
- `trae`
- `claude`
- `codex`

## Skill Package Rules

- Every implemented public Skill must include both `zh_CN` and `en_US` versions unless it is explicitly marked as `candidate` in `catalog/skills.yaml`.
- Keep Chinese and English versions behaviorally aligned.
- When updating one locale, read the other locale before deciding whether it needs the same behavior update.
- Keep `SKILL.md` frontmatter limited to `name` and `description`.
- Put detailed templates, checklists, or long references in `references/`, not directly in `SKILL.md`.
- Add redacted examples under `examples/<package-family>/<skill-name>/<locale>/`.
- Keep `README.md` and `STATUS.md` at the Skill root when a Skill has multiple locales.
- Each locale directory must remain independently importable and contain every required runtime reference.

## Catalog Rules

- Register every Skill or planned Skill in `catalog/skills.yaml`.
- Use global stable IDs such as `SKL-0001`; do not encode the tool family in the ID.
- Use `scope: shared` for workflows that can apply across tools.
- Use `scope: tool-specific` for workflows tied to one agent tool or platform.
- `scope` describes workflow portability; `supported_tools` describes implemented package families.
- For shared Skills, keep the core workflow tool-neutral and isolate tool-specific commands, UI assumptions, screenshots, marketplace links, or import steps inside the matching variant directory.
- `target_tools` may list planned tools before those variants exist. Do not treat missing planned variants as evidence against the implemented variant's current status.
- Record agent/model fit as capability requirements, not as promises tied to one changing model brand or version. Prefer wording such as file access, repository inspection, tool use, long-context reasoning, code reasoning, safety review, or writing quality.
- Keep catalog status aligned with or more conservative than each Skill's `STATUS.md`.
- Record importable locale roots under `variants[].locale_roots.<locale>.import_root`.
- If a Skill is only a candidate, leave implementation variants empty, record intended `target_tools`, and mark `status: candidate`.

## Public Safety Rules

- Do not commit `.env`, tokens, cookies, private keys, credentials, private repository URLs, customer data, internal hostnames, personal information, account identifiers, or unredacted screenshots.
- Do not quote personal names, handles, emails, phone numbers, avatars, machine names, sensitive local absolute paths, or account/workspace labels in public examples unless they are intentionally redacted placeholders.
- Review screenshots before committing them.
- Prefer placeholders for missing screenshots, public links, or marketplace links.

## Editing Rules

- Follow existing structure and naming before adding new patterns.
- When updating one locale, check whether the other locale needs the same behavior update.
- When adding or renaming a Skill, update `catalog/skills.yaml`, root `README.md`, and relevant examples.
- When changing readiness, update the Skill's `STATUS.md` and the matching catalog entry.
- Fix broken relative links when encountered in touched files.

## Validation Checklist

Before calling a Skill ready:

- `catalog/skills.yaml` has a unique ID and correct paths.
- `zh_CN` and `en_US` Skill packages exist.
- Examples exist for both required locales.
- `SKILL.md` has clear trigger frontmatter.
- References linked from `SKILL.md` exist, if any.
- Each locale directory can be imported as a Skill root containing `SKILL.md`.
- Catalog status follows `catalog/status-policy.md`, including locale status and evidence requirements.
- Public-safety rules have been checked.
- `STATUS.md` reflects the real validation state.
