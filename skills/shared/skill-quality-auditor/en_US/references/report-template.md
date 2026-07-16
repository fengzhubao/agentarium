# Audit Report Template

```markdown
# Skill Quality Audit Report

## Verdict

<PASS | PASS WITH WARNINGS | FAIL>

Target: <SKL-ID / slug>
Claimed status: <status>
Supported status: <status>

## Deterministic Preflight

- Command: `python scripts/validate_agentarium.py --repo-root <repo-root> --skill <ID-or-slug> --strict`
- Exit code: <code>
- Errors: <count>
- Warnings: <count>
- Script findings: <findings or None>

## Manual Judgment

- Behavioral locale parity: <result and notes>
- Evidence metadata, semantics, and authenticity: <result and notes>
- Nuanced public-safety and screenshot review: <result and notes>

## Findings

### BLOCKER

- <file:line> <issue>. Impact: <impact>. Fix: <fix>.

### HIGH

- <file:line> <issue>. Impact: <impact>. Fix: <fix>.

### MEDIUM

- <file:line> <issue>. Impact: <impact>. Fix: <fix>.

### LOW

- <file:line> <issue>. Impact: <impact>. Fix: <fix>.

## Check Matrices

| Check | Result | Notes |
| --- | --- | --- |
| Catalog schema v2 | <pass/fail> | <notes> |
| Package structure | <pass/fail> | <notes> |
| Locale parity | <pass/fail> | <notes> |
| References and links | <pass/fail> | <notes> |
| Evidence gates | <pass/fail> | <notes> |
| Public safety | <pass/fail> | <notes> |

## Required Next Actions

- <action>

## Files Inspected

- <path>

## Not Checked / Assumptions

- <assumption>
```
