# Link and Reference Checklist

## SKILL.md Runtime References

- Every `references/...` file listed in `SKILL.md` must exist.
- Reference paths are relative to that locale's `SKILL.md`.
- If one locale adds a reference, the other locale should have an equivalent behavior reference.

## Markdown Links

- Check that relative links resolve from the current file location.
- Check that link targets are inside the repository unless they are explicitly public external documentation.
- Do not use local absolute paths as public links.

## Example Paths

- `sample-input.md` and `sample-output.md` should live under `examples/<package-family>/<slug>/<locale>/`.
- Catalog evidence paths should point to real files.
- `examples_root` should point to the locale directory or Skill examples root, without mixing nonexistent paths.

## Broken Link Report Format

Each broken-link finding includes:

- Referencing file.
- Original link or path.
- Base directory used for resolution.
- Expected target.
- Recommended corrected path.
