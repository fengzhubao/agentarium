# Catalog Status Policy

Use these statuses in `catalog/skills.yaml`.

## Status Values

- `candidate`: Proposed but not implemented. Paths may be empty.
- `draft`: Implemented enough for review, but not trial validated.
- `sampled`: Has sample input and output, but no real tool trial yet.
- `trial-validated`: Has been run in the target agent tool at least once with recorded public-safe evidence or a redacted trial note.
- `ready`: Complete public package with both required locales, examples, safety review, and validation evidence.
- `deprecated`: Kept for history, but not recommended for new use.

## Status Rules

- `supported_tools` lists implemented tool variants. `target_tools` lists planned or intended tool support.
- `package_root` may point to a multi-locale Skill package. Importable paths must be listed under `variants[].locale_roots.<locale>.import_root`.
- Top-level `status` must be conservative across required locales and implemented variants. Use `status_note` and locale-level statuses to record stronger partial validation.
- Do not mark a Skill `ready` unless both `zh_CN` and `en_US` packages exist.
- Do not mark a Skill `ready` unless `examples/<tool>/<skill-name>/zh_CN/` and `examples/<tool>/<skill-name>/en_US/` both contain public-safe samples.
- Keep `catalog/skills.yaml` status aligned with or more conservative than the Skill root `STATUS.md`.
- If a status differs between tool variants, record the conservative overall status in the main entry and variant-specific status under `variants`.

## Aggregation Rules

Statuses are recorded at three levels:

- Locale status: readiness of one importable locale directory.
- Variant status: conservative aggregate of required locale statuses for one tool.
- Skill status: conservative aggregate of implemented tool variants.

For aggregation, use the least mature required status among non-deprecated children:

```text
candidate < draft < sampled < trial-validated < ready
```

`deprecated` is not part of maturity aggregation and must be set explicitly.

If a Skill has no implemented variants, its status is `candidate`.

## Evidence Gates

### candidate

Required evidence:

- Unique `id` matching `^SKL-[0-9]{4}$`.
- `slug`, `title`, `scope`, summaries, and tags.
- Non-empty `target_tools`.
- No package paths are required.

### draft

Required evidence per implemented tool variant:

- `package_root` exists.
- `README.md` and `STATUS.md` exist under `package_root`.
- Required locale `import_root` directories exist.
- Each `import_root` contains `SKILL.md`.
- `SKILL.md` frontmatter is limited to `name` and `description`.
- Referenced files under `references/` exist.

### sampled

Everything required for `draft`, plus per required locale:

- Public-safe sample input exists.
- Public-safe sample output exists.
- Example paths are under `examples/<tool>/<skill-name>/<locale>/`.

### trial-validated

Everything required for `sampled`, plus per locale:

- A recorded trial in the target tool, represented by public-safe output, redacted screenshot, or redacted trial note.
- Trial evidence identifies tool, locale, date or context, and observed result.
- Sensitive local paths, account data, private repository URLs, and credentials are absent or redacted.

### ready

Everything required for `trial-validated`, plus:

- All required locales are at least `trial-validated`.
- Public-safety checklist has passed.
- Relative links resolve.
- `STATUS.md` has no blocking pending evidence for the ready claim.

## Trial Evidence

`trial-validated` status requires a public-safe note or artifact that records:

- Tool and tool version, if known.
- Trial date.
- Locale tested.
- Input summary.
- Output or generated artifact path.
- Known failures or warnings.
- Public-safety review result.

## Ready Evidence

`ready` status requires:

- Both `zh_CN` and `en_US` Skill packages.
- Public-safe examples for both required locales.
- Importable locale roots with `SKILL.md`.
- Resolved references linked from `SKILL.md`.
- Public-safety review.
- Validation evidence recorded in `STATUS.md` or linked examples.
