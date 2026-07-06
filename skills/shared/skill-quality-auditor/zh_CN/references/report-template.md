# 审计报告模板

```markdown
# Skill Quality Audit Report

## Verdict

<PASS | PASS WITH WARNINGS | FAIL>

Target: <SKL-ID / slug>
Claimed status: <status>
Supported status: <status>

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
