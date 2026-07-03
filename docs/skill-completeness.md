# Skill Completeness Checklist

Use this checklist before calling a Skill ready for public use.

## Required Repository Structure

- [ ] `AGENTS.md` rules have been followed.
- [ ] `catalog/skills.yaml` contains a unique Skill ID, correct variant paths, required locales, and importable locale roots.
- [ ] `skills/<tool>/<skill-name>/README.md`
- [ ] `skills/<tool>/<skill-name>/STATUS.md`
- [ ] `skills/<tool>/<skill-name>/zh_CN/SKILL.md`
- [ ] `skills/<tool>/<skill-name>/zh_CN/references/` exists if the Chinese `SKILL.md` links runtime references.
- [ ] `skills/<tool>/<skill-name>/en_US/SKILL.md`
- [ ] `skills/<tool>/<skill-name>/en_US/references/` exists if the English `SKILL.md` links runtime references.
- [ ] `examples/<tool>/<skill-name>/zh_CN/sample-input.md`
- [ ] `examples/<tool>/<skill-name>/zh_CN/sample-output.md`
- [ ] `examples/<tool>/<skill-name>/en_US/sample-input.md`
- [ ] `examples/<tool>/<skill-name>/en_US/sample-output.md`

## Required Content

- [ ] `SKILL.md` has YAML frontmatter with `name` and `description`.
- [ ] The trigger description is specific enough for the agent to know when to use the Skill.
- [ ] The workflow is concise and actionable.
- [ ] Reference files linked from `SKILL.md` resolve within the importable locale directory.
- [ ] Examples are redacted and public-safe.
- [ ] Chinese and English versions are behaviorally aligned.
- [ ] Locale-specific templates are clearly labeled.
- [ ] Public-safety boundaries are explicit.
- [ ] Catalog status matches or is more conservative than `STATUS.md`.

## Validation

- [ ] The Skill can be imported or copied as a directory containing `SKILL.md`.
- [ ] Each required locale directory can be imported independently as a Skill root.
- [ ] The sample input produces the expected output shape.
- [ ] Missing screenshots, source links, or marketplace links are marked as placeholders.
- [ ] No secrets or private paths are present.
- [ ] `STATUS.md` reflects the current readiness.
- [ ] Trial or ready status has evidence required by `catalog/status-policy.md`.
- [ ] Relative links from `SKILL.md` and references resolve correctly.

