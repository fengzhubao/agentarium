# Worktree Conductor Output Template

````markdown
# Worktree Conductor Plan

## 1. Parallel Feasibility

- Decision: suitable for parallel work / needs shared foundation first / not recommended for parallel work.
- Reasons:
  - <reason 1>
  - <reason 2>
- Recommended parallelism: <number>

## 2. Recommended Branch / Worktree Split

| Task | Branch | Worktree Path | Owner/Agent | Goal |
| --- | --- | --- | --- | --- |
| Shared foundation | `feat/shared-foundation` | `../repo-foundation` | <owner> | <goal> |
| Task A | `feat/<name-a>` | `../repo-<name-a>` | <owner> | <goal> |

## 3. File Ownership And Forbidden Areas

| Task | Allowed Paths | Forbidden Paths | Dependencies |
| --- | --- | --- | --- |
| <task> | `<path>` | `<path>` | <dependency> |

## 4. Shared-File Risk Table

| File/Area | Risk | Reason | Strategy |
| --- | --- | --- | --- |
| `<path>` | High/Medium/Low | <reason> | <strategy> |

## 5. Command Safety Preflight

```bash
git branch --show-current
git status --short
git worktree list
git branch --list feat/<task>
```

Confirm target worktree paths do not already exist before running `git worktree add`.
Do not use `git reset --hard`, `git clean -fd`, force push, or destructive cleanup unless the user explicitly asks for that operation.

## 6. Recommended Commands

```bash
git fetch origin
git switch <base-branch>
git pull --ff-only
git worktree add ../repo-<task> -b feat/<task>
```

Adjust commands to the actual repository, branch names, and local paths.

## 7. Branch Acceptance Checks

| Branch | Required Checks | Passing Standard |
| --- | --- | --- |
| `feat/<task>` | `<command>` | <standard> |

## 8. Integration Order

1. Merge `feat/shared-foundation`.
2. Merge low-level modules.
3. Merge features that depend on low-level modules.
4. Merge examples and docs.
5. Run full validation on `integration/round-1`.

## 9. Task Prompts For Agents

### Agent A

```text
You are responsible for <task>.
Branch: <branch>
Worktree: <path>
Allowed paths: <paths>
Forbidden paths: <paths>
Dependencies: <dependencies>
Validation commands: <commands>
Output requirements: summarize changes, validation results, risks, and follow-ups.
Do not revert others' work. Do not expand the file scope.
```

## 10. Questions For Human Confirmation

- <question 1>
- <question 2>
````
