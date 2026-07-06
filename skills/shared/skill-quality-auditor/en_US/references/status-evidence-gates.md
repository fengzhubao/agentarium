# Status Evidence Gates

## candidate

Requires:

- Unique `id`.
- `slug`, `title`, scope, summaries, and tags.
- Non-empty `target_tools`.
- No package paths are required.

## draft

Everything required for candidate, plus each implemented package variant has:

- Existing `package_root`.
- Existing `README.md` and `STATUS.md`.
- Existing required locale `import_root` directories.
- `SKILL.md` directly inside each `import_root`.
- `SKILL.md` frontmatter limited to `name` and `description`.
- Existing `references/` files mentioned by `SKILL.md`.

## sampled

Everything required for draft, plus each required locale has:

- Public-safe `sample-input.md`.
- Public-safe `sample-output.md`.
- Example paths under `examples/<package-family>/<skill-name>/<locale>/`.

## trial-validated

Everything required for sampled, plus real target-tool trial evidence for each required locale:

- Tool and version, if known.
- Trial date or context.
- Locale.
- Input summary.
- Output or generated artifact path.
- Known failures or warnings.
- Public-safety review result.

## ready

Everything required for trial-validated, plus:

- All required locales are at least `trial-validated`.
- Public-safety review has passed.
- Relative links resolve.
- `STATUS.md` has no blocking pending evidence for the ready claim.

## Audit Principle

- Judge by existing evidence, not intent.
- If `STATUS.md` claims a higher status than catalog evidence supports, report a status mismatch.
- If one locale lacks evidence, aggregate the variant and top-level status to the lower status.
