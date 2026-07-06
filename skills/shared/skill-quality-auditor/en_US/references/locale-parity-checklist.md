# Locale Parity Checklist

Check behavior parity between `zh_CN` and `en_US`, not word-for-word translation.

## Required Checks

- Frontmatter `name` is consistent.
- Frontmatter `description` triggers the same task class.
- Default behavior is consistent, including read-only auditing and file modification rules.
- Workflow steps cover the same checks.
- Reference file lists match.
- Status, evidence, and safety gates match.
- Report output format matches.

## Acceptable Differences

- Different phrasing.
- Chinese terms in the Chinese version and English terms in the English version.
- Localized example project names, as long as audit rules do not change.

## Common Problems

- One locale requires a reference file that the other locale omits.
- One locale modifies files by default while the other audits read-only.
- One locale treats screenshots or forum posts as required evidence while the other marks them optional.
- Severity or verdict labels differ between locales.
