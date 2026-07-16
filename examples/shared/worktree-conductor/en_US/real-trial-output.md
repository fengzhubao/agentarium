# SKL-0002 en_US Codex Trial Record

## Trial Record

- Tool: Codex
- Tool version: `codex-cli 0.144.4`; the underlying session model and service build were not exposed
- Trial date: `2026-07-16` (`Asia/Shanghai`)
- Locale: `en_US`
- Import root: `<repo-root>/skills/shared/worktree-conductor/en_US`
- Input summary: Inspected the public `agentarium` repository's current branch, worktree state, existing worktrees, target branches, and relevant directories, then planned safe multi-worktree delivery of SKL-0004 `agent-context-sync`.
- Output or artifact path: `examples/shared/worktree-conductor/en_US/real-trial-output.md`
- Known failures or warnings: `main` contained authorized SKL-0003 release-status edits, so the plan correctly prohibited immediate worktree creation and assigned those changes to the integrator first.
- Public-safety review: Pass; the record uses only the public repository name, repository-relative paths, and example worktree paths. It contains no local absolute path, account data, personal information, private URL, credential, or screenshot.

## Observed Result

PASS. The Skill produced the complete ten-section plan, detected the dirty worktree and high-risk shared files, and supplied a serial shared-foundation stage, parallel boundaries, acceptance checks, integration order, and reusable agent prompts. The trial ran read-only Git preflight commands only; it did not create branches or worktrees.

# Worktree Conductor Plan

## 1. Parallel Feasibility

- Decision: parallel work is appropriate after locking the shared interface; worktrees must not be created immediately.
- Reasons:
  - `catalog/skills.yaml`, the root `README.md`, the CI workflow, and the two locale script copies are high-risk shared areas.
  - Chinese content, English content, and core script/tests can be separated after the interface is stable.
  - `main` currently contains the SKL-0003 release-review edits; the current integrator must preserve and commit them before new worktrees start.
- Recommended parallelism: serial shared foundation, then at most three implementation tasks plus one integration task.

## 2. Recommended Branch / Worktree Split

| Task | Branch | Worktree Path | Owner | Goal |
| --- | --- | --- | --- | --- |
| Shared foundation | `feat/context-sync-foundation` | `../agentarium-context-foundation` | Integrator | Lock markers, config schema, CLI, and exit codes |
| Core script and tests | `feat/context-sync-core` | `../agentarium-context-core` | Core agent | Implement identical locale scripts and standard-library tests |
| Chinese package | `feat/context-sync-zh` | `../agentarium-context-zh` | zh agent | Write Chinese SKILL, reference, and examples |
| English package | `feat/context-sync-en` | `../agentarium-context-en` | en agent | Write English SKILL, reference, and examples |
| Catalog and integration | `integration/context-sync` | `../agentarium-context-integration` | Integrator | Update catalog, README, STATUS, CI, and full validation |

## 3. File Ownership And Forbidden Areas

| Task | Allowed Paths | Forbidden Paths | Dependencies |
| --- | --- | --- | --- |
| Shared foundation | Design record or integrator-assigned file | Existing Skill packages | Commit current SKL-0003 changes first |
| Core script and tests | Both locale `scripts/sync_agent_context.py` copies and `tests/test_sync_agent_context.py` | Catalog, README, locale docs | Locked CLI contract |
| Chinese package | `skills/shared/agent-context-sync/zh_CN/` and Chinese examples | English package, catalog, tests | CLI contract |
| English package | `skills/shared/agent-context-sync/en_US/` and English examples | Chinese package, catalog, tests | CLI contract |
| Catalog and integration | Package README/STATUS, `catalog/skills.yaml`, root README, CI | Unrelated Skill content | All subtasks |

## 4. Shared-File Risk Table

| File/Area | Risk | Reason | Strategy |
| --- | --- | --- | --- |
| `catalog/skills.yaml` | High | Controls status, paths, and evidence aggregation | Integrator only |
| `.github/workflows/validate-agentarium.yml` | High | Affects all CI platforms | Integration stage only |
| Two locale sync scripts | High | Must remain byte-identical | One core owner edits both |
| `tests/` | Medium | Encodes the shared behavior contract | Core owner; integrator review |
| Two locale `SKILL.md` files | Medium | Behavior must remain aligned | Separate authors plus parity review |
| Root `README.md` | Medium | Also contains the SKL-0003 status change | Current integrator only |

## 5. Command Safety Preflight

```text
git branch --show-current
git status --short
git worktree list
git branch --list feat/context-sync-foundation
git branch --list feat/context-sync-core
git branch --list feat/context-sync-zh
git branch --list feat/context-sync-en
git branch --list integration/context-sync
```

The current branch is `main`, only one worktree exists, and the target branches are absent, but the worktree is dirty. The current owner must commit or explicitly handle the SKL-0003 changes before any `git worktree add`. Do not use `git reset --hard`, `git clean -fd`, or force push.

## 6. Recommended Commands

Only read-only preflight is recommended now. After the worktree is clean, adjust paths as needed and run:

```text
git fetch origin
git switch main
git pull --ff-only
git worktree add ../agentarium-context-foundation -b feat/context-sync-foundation
```

After merging shared foundation, create the core, zh, en, and integration worktrees from the updated base.

## 7. Branch Acceptance Checks

| Branch | Required Checks | Passing Standard |
| --- | --- | --- |
| `feat/context-sync-core` | `python -m unittest tests.test_sync_agent_context -v` | check/diff/sync, path safety, and LF/CRLF tests pass |
| `feat/context-sync-zh` | Focused Skill audit | Frontmatter, references, examples, and safety pass |
| `feat/context-sync-en` | Focused Skill audit | Behavior matches Chinese; references and examples pass |
| `integration/context-sync` | Full strict validator, unittest, `git diff --check` | 0 errors, 0 warnings, all tests pass |

## 8. Integration Order

1. Complete and lock the shared-foundation marker, config, and CLI contract.
2. Merge the core script and tests.
3. Merge the Chinese and English packages.
4. Let the integrator synchronize script copies and update catalog, README, STATUS, and CI.
5. Run full validation, locale parity review, and public-safety review.

## 9. Task Prompts For Agents

### Core agent

```text
You own the deterministic Agent Context Sync script and tests.
Branch: feat/context-sync-core
Worktree: ../agentarium-context-core
Allowed: both locale scripts/sync_agent_context.py files and tests/test_sync_agent_context.py.
Forbidden: catalog, root README, package README/STATUS, SKILL.md files, and examples.
Implement check/diff/sync, managed blocks, repository path containment, preservation of unmanaged content, and LF/CRLF behavior.
Run focused unittest and confirm both script copies are byte-identical.
Do not revert others' work or expand the file scope.
```

### zh agent

```text
You own the Agent Context Sync Chinese package and public-safe Chinese examples.
Branch: feat/context-sync-zh
Worktree: ../agentarium-context-zh
Allowed: skills/shared/agent-context-sync/zh_CN/ and examples/shared/agent-context-sync/zh_CN/.
Forbidden: English package, scripts, tests, catalog, and root README.
Follow the locked CLI contract. Do not invent different defaults.
Finish with trigger, input, output, risk boundary, and validation notes.
```

### en agent

```text
You own the Agent Context Sync English package and public-safe English examples.
Branch: feat/context-sync-en
Worktree: ../agentarium-context-en
Allowed: skills/shared/agent-context-sync/en_US/ and examples/shared/agent-context-sync/en_US/.
Forbidden: Chinese package, scripts, tests, catalog, and root README.
Follow the locked CLI contract and keep behavior aligned with zh_CN.
Finish with scope, validation, risks, and follow-ups. Do not revert others' work.
```

### Integrator

```text
You own integration/context-sync.
Allowed: package README/STATUS, catalog/skills.yaml, root README, CI, and required integration records.
Preserve and commit the current SKL-0003 release edits first, then integrate core, zh, and en in order.
Confirm the locale scripts are byte-identical and run the full strict validator, all unittest, and line-ending checks.
Do not force push or modify unrelated Skills.
```

## 10. Questions For Human Confirmation

- Should the maintainer actually create separate worktrees, or implement serially in the current workspace while following the same ownership plan?
- Should the default shared source path be `.agent-context/shared.md`?
- May `sync` create a missing target? The plan recommends yes, writing only the managed block.

## Trial Boundary

- This trial validates planning output; it did not create worktrees or branches.
- Active execution constraints required serial delivery in the current workspace while preserving this plan's ownership and integration order.
