# Skill Completeness Checklist

Use this checklist before calling a Skill ready for public use.

## Required Repository Structure

- [ ] `skills/<tool>/<skill-name>/README.md`
- [ ] `skills/<tool>/<skill-name>/STATUS.md`
- [ ] `skills/<tool>/<skill-name>/zh_CN/SKILL.md`
- [ ] `skills/<tool>/<skill-name>/zh_CN/references/`
- [ ] `skills/<tool>/<skill-name>/en_US/SKILL.md`
- [ ] `skills/<tool>/<skill-name>/en_US/references/`
- [ ] `examples/<tool>/<skill-name>/zh_CN/sample-input.md`
- [ ] `examples/<tool>/<skill-name>/zh_CN/sample-output.md`
- [ ] `examples/<tool>/<skill-name>/en_US/sample-input.md`
- [ ] `examples/<tool>/<skill-name>/en_US/sample-output.md`

## Required Content

- [ ] `SKILL.md` has YAML frontmatter with `name` and `description`.
- [ ] The trigger description is specific enough for the agent to know when to use the Skill.
- [ ] The workflow is concise and actionable.
- [ ] Reference files are linked from `SKILL.md`.
- [ ] Examples are redacted and public-safe.
- [ ] Chinese and English versions are behaviorally aligned.
- [ ] Locale-specific templates are clearly labeled.
- [ ] Public-safety boundaries are explicit.

## Validation

- [ ] The Skill can be imported or copied as a directory containing `SKILL.md`.
- [ ] The sample input produces the expected output shape.
- [ ] Missing screenshots, source links, or marketplace links are marked as placeholders.
- [ ] No secrets or private paths are present.
- [ ] `STATUS.md` reflects the current readiness.

