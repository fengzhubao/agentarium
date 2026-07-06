# Audit Workflow

## 1. Establish Scope

- Record the Skill ID, slug, tool family, target status, and locales to inspect.
- Decide whether the user requested a read-only audit or explicitly asked for fixes.
- If the user did not specify a target status, audit against the current claims in `catalog/skills.yaml` and `STATUS.md`.

## 2. Read Governance Material

Read at least:

- `AGENTS.md`
- `README.md`
- `catalog/skills.yaml`
- `catalog/status-policy.md`
- `docs/importing.md`
- `docs/localization.md`
- `docs/safety.md`
- `docs/skill-completeness.md`

## 3. Collect Target Skill Files

Check whether these paths exist and record any missing items:

- `skills/<package-family>/<slug>/README.md`
- `skills/<package-family>/<slug>/STATUS.md`
- `skills/<package-family>/<slug>/zh_CN/SKILL.md`
- `skills/<package-family>/<slug>/en_US/SKILL.md`
- `references/` for both locales
- `examples/<package-family>/<slug>/zh_CN/sample-input.md`
- `examples/<package-family>/<slug>/zh_CN/sample-output.md`
- `examples/<package-family>/<slug>/en_US/sample-input.md`
- `examples/<package-family>/<slug>/en_US/sample-output.md`

## 4. Run Checks

Run checks in this order:

1. Catalog schema and path checks.
2. Skill package structure checks.
3. `SKILL.md` frontmatter checks.
4. Bilingual behavior parity checks.
5. Reference, link, and example path checks.
6. Status evidence gate checks.
7. Public-safety checks.

## 5. Report

- Start with a verdict.
- Order findings by BLOCKER, HIGH, MEDIUM, and LOW.
- Each finding includes location, issue, impact, and recommended fix.
- If there are no blockers, still list residual risk and unchecked areas.
