# Skill Completeness Checklist

Use this checklist before calling a Skill ready for public use.

## Required Repository Structure

- [ ] `AGENTS.md` rules have been followed.
- [ ] `catalog/skills.yaml` contains a unique Skill ID, correct variant paths, required locales, and importable locale roots.
- [ ] `skills/<package-family>/<skill-name>/README.md`
- [ ] `skills/<package-family>/<skill-name>/STATUS.md`
- [ ] `skills/<package-family>/<skill-name>/zh_CN/SKILL.md`
- [ ] `skills/<package-family>/<skill-name>/zh_CN/references/` exists if the Chinese `SKILL.md` links runtime references.
- [ ] `skills/<package-family>/<skill-name>/en_US/SKILL.md`
- [ ] `skills/<package-family>/<skill-name>/en_US/references/` exists if the English `SKILL.md` links runtime references.
- [ ] `examples/<package-family>/<skill-name>/zh_CN/sample-input.md`
- [ ] `examples/<package-family>/<skill-name>/zh_CN/sample-output.md`
- [ ] `examples/<package-family>/<skill-name>/en_US/sample-input.md`
- [ ] `examples/<package-family>/<skill-name>/en_US/sample-output.md`

## Required Content

- [ ] `SKILL.md` has YAML frontmatter with `name` and `description`.
- [ ] The trigger description is specific enough for the agent to know when to use the Skill.
- [ ] The workflow is concise and actionable.
- [ ] For `scope: shared` Skills, the core workflow is tool-neutral except for clearly labeled variant-specific import, UI, runtime, screenshot, or marketplace details.
- [ ] TRAE SOLO, contest, or community-post wording appears only where it is intentionally part of that Skill or example, not inherited by unrelated shared Skills.
- [ ] `catalog/skills.yaml` records `model_fit` or equivalent agent/model capability notes.
- [ ] Skill README explains suitable agent/model capabilities and unsuitable contexts.
- [ ] Reference files linked from `SKILL.md` resolve within the importable locale directory.
- [ ] Examples are redacted and public-safe.
- [ ] Examples do not expose personal names, handles, emails, phone numbers, avatars, account identifiers, machine names, or user/workspace labels.
- [ ] Chinese and English versions are behaviorally aligned.
- [ ] Locale-specific templates are clearly labeled.
- [ ] Public-safety boundaries are explicit.
- [ ] Catalog status matches or is more conservative than `STATUS.md`.

## Validation

- [ ] The Skill can be imported or copied as a directory containing `SKILL.md`.
- [ ] Each required locale directory can be imported independently as a Skill root.
- [ ] The sample input produces the expected output shape.
- [ ] Missing screenshots, source links, or marketplace links are marked as placeholders.
- [ ] No secrets, personal information, account identifiers, machine names, or private paths are present.
- [ ] `STATUS.md` reflects the current readiness.
- [ ] Trial or ready status has evidence required by `catalog/status-policy.md`.
- [ ] Relative links from `SKILL.md` and references resolve correctly.
