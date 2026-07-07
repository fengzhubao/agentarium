# Worktree Conductor Sample Output

Note: this is a redacted sample showing the intended output shape. Save real target-tool trial output and public-safe evidence after testing the current implemented package.

````markdown
# Worktree Conductor Plan

## 1. Parallel Feasibility

Decision: suitable for parallel work, but a shared-foundation pass should happen first.

Reasons:

- `runtime/`, `generator/`, `examples/`, and `docs/` can be split into mostly independent tasks.
- `definition/*.yaml`, `schema/`, `generated/`, and `package-lock.json` are high-risk shared areas and should not be edited concurrently.
- If the DSL contract must change, it should happen in `feat/shared-foundation` before other branches start.

Recommended parallelism: 3 implementation tasks plus 1 docs/examples task.

## 2. Recommended Branch / Worktree Split

| Task | Branch | Worktree Path | Owner/Agent | Goal |
| --- | --- | --- | --- | --- |
| Shared foundation | `feat/shared-foundation` | `../example-hmi-foundation` | Integrator | Confirm DSL contract, schema, and generation boundaries |
| Runtime parser | `feat/runtime-parser` | `../example-hmi-runtime` | Codex | Implement runtime parsing |
| UI generator | `feat/ui-generator` | `../example-hmi-generator` | TRAE | Implement component generation |
| Examples | `feat/examples` | `../example-hmi-examples` | Claude | Add example projects and demo inputs |
| Docs | `feat/docs` | `../example-hmi-docs` | TRAE or human | Write usage and integration guides |

## 3. File Ownership And Forbidden Areas

| Task | Allowed Paths | Forbidden Paths | Dependencies |
| --- | --- | --- | --- |
| Shared foundation | `definition/*.yaml`, `schema/` | implementation directories | none |
| Runtime parser | `runtime/`, `tests/runtime/` | `definition/*.yaml`, `schema/`, `generated/` | `feat/shared-foundation` |
| UI generator | `generator/`, `tests/generator/` | `definition/*.yaml`, `schema/`, `package-lock.json` | `feat/shared-foundation` |
| Examples | `examples/` | `definition/*.yaml`, `schema/`, `generated/` | stable runtime and generator |
| Docs | `docs/` | implementation code, lockfiles | outputs from other branches |

## 4. Shared-File Risk Table

| File/Area | Risk | Reason | Strategy |
| --- | --- | --- | --- |
| `definition/*.yaml` | High | DSL contract affects all modules | Only shared foundation edits it |
| `schema/` | High | Runtime and generator both depend on it | Only shared foundation edits it |
| `generated/` | High | Generated outputs are easy to overwrite | Regenerate in integration branch |
| `package-lock.json` | High | Concurrent edits often conflict | Avoid edits in subtasks |
| `docs/` | Medium | Several tasks will reference it | Assign one docs owner |
| `examples/` | Medium | Depends on runtime and generator behavior | Integrate after implementation branches |

## 5. Command Safety Preflight

```bash
git branch --show-current
git status --short
git worktree list
git branch --list feat/shared-foundation
git branch --list feat/runtime-parser
git branch --list feat/ui-generator
git branch --list feat/examples
git branch --list feat/docs
git branch --list integration/round-1
```

Before running `git worktree add`, confirm the target paths do not already exist:

```text
../example-hmi-foundation
../example-hmi-runtime
../example-hmi-generator
../example-hmi-examples
../example-hmi-docs
../example-hmi-integration
```

Do not use destructive commands such as `git reset --hard`, `git clean -fd`, or force push unless the user explicitly asks for them and accepts the risk.

## 6. Recommended Commands

```bash
git fetch origin
git switch main
git pull --ff-only
git switch -c feat/shared-foundation
git worktree add ../example-hmi-runtime -b feat/runtime-parser
git worktree add ../example-hmi-generator -b feat/ui-generator
git worktree add ../example-hmi-examples -b feat/examples
git worktree add ../example-hmi-docs -b feat/docs
git worktree add ../example-hmi-integration -b integration/round-1
```

Adjust paths and branch names to the actual repository.

## 7. Branch Acceptance Checks

| Branch | Required Checks | Passing Standard |
| --- | --- | --- |
| `feat/shared-foundation` | `npm run lint`, `npm test` | Schema and contract changes do not break existing tests |
| `feat/runtime-parser` | `npm test -- runtime` | Runtime tests pass |
| `feat/ui-generator` | `npm test -- generator`, `npm run build` | Generator tests and build pass |
| `feat/examples` | `npm run build` | Examples can consume the current DSL shape |
| `feat/docs` | docs link check or human review | Steps can be followed by a new user |
| `integration/round-1` | `npm run lint`, `npm test`, `npm run build` | Full validation passes |

## 8. Integration Order

1. Merge `feat/shared-foundation`.
2. Merge `feat/runtime-parser`.
3. Merge `feat/ui-generator`.
4. Merge `feat/examples`.
5. Merge `feat/docs`.
6. Regenerate outputs and run full validation on `integration/round-1`.

## 9. Task Prompts For Agents

### Integrator: Shared Foundation

```text
You are responsible for shared DSL foundation. You are not alone in this repository; other agents will work in separate worktrees after this foundation is stable.

Repository: example_hmi_dsl
Branch: feat/shared-foundation
Worktree: ../example-hmi-foundation
Goal: Confirm DSL contract, schema boundaries, and generator/runtime assumptions before parallel implementation starts.

Allowed paths:
- definition/*.yaml
- schema/
- docs/architecture/

Forbidden paths:
- runtime/
- generator/
- generated/
- package-lock.json

Shared dependencies:
- Downstream runtime parser, UI generator, examples, and docs tasks depend on this branch.

Validation commands:
- npm run lint
- npm test

Requirements:
- Only modify files in the allowed scope.
- Do not revert changes made by others.
- If a generated output or lockfile must change, stop and explain why first.
- Finish with a change summary, validation results, risks, and follow-ups.
```

### Codex: Runtime Parser

```text
You are responsible for runtime DSL parsing. You are not alone in this repository; other agents are working in separate worktrees.

Repository: example_hmi_dsl
Branch: feat/runtime-parser
Worktree: ../example-hmi-runtime
Goal: Implement runtime parsing against the shared DSL contract.

Allowed paths:
- runtime/
- tests/runtime/

Forbidden paths:
- definition/*.yaml
- schema/
- generated/
- package-lock.json

Shared dependencies:
- feat/shared-foundation

Validation commands:
- npm test -- runtime
- npm run lint

Finish with a change summary, validation results, risks, and follow-ups. Do not revert others' work. Do not expand the file scope.
```

### TRAE: UI Generator

```text
You are responsible for UI component generation. You are not alone in this repository; other agents are working in separate worktrees.

Repository: example_hmi_dsl
Branch: feat/ui-generator
Worktree: ../example-hmi-generator
Goal: Implement component generation against the shared DSL contract.

Allowed paths:
- generator/
- tests/generator/

Forbidden paths:
- definition/*.yaml
- schema/
- generated/
- package-lock.json

Shared dependencies:
- feat/shared-foundation

Validation commands:
- npm test -- generator
- npm run build
- npm run lint

Requirements:
- Only modify files in the allowed scope.
- Do not update generated outputs in this branch unless the integrator explicitly assigns that task.
- Finish with a change summary, validation results, risks, and follow-ups.
```

### Claude: Examples

```text
You are responsible for example projects and demo inputs. You are not alone in this repository; other agents are working in separate worktrees.

Repository: example_hmi_dsl
Branch: feat/examples
Worktree: ../example-hmi-examples
Goal: Add example projects that demonstrate the stable runtime and generator behavior.

Allowed paths:
- examples/
- tests/examples/

Forbidden paths:
- definition/*.yaml
- schema/
- runtime/
- generator/
- generated/
- package-lock.json

Shared dependencies:
- feat/runtime-parser
- feat/ui-generator

Validation commands:
- npm run build
- npm test

Requirements:
- Only modify files in the allowed scope.
- If examples require contract or generator changes, stop and explain the needed dependency.
- Finish with a change summary, validation results, risks, and follow-ups.
```

### TRAE Or Human: Docs

```text
You are responsible for usage and integration documentation. You are not alone in this repository; other agents are working in separate worktrees.

Repository: example_hmi_dsl
Branch: feat/docs
Worktree: ../example-hmi-docs
Goal: Write guides that explain the DSL, runtime parser, generator, examples, and integration workflow.

Allowed paths:
- docs/
- README.md

Forbidden paths:
- runtime/
- generator/
- definition/*.yaml
- schema/
- generated/
- package-lock.json

Shared dependencies:
- summaries from feat/runtime-parser, feat/ui-generator, and feat/examples

Validation commands:
- docs link check or human review
- npm run build

Requirements:
- Only modify files in the allowed scope.
- Do not rewrite implementation code.
- Finish with a change summary, validation results, risks, and follow-ups.
```

### Integrator: Integration Round

```text
You are responsible for integration/round-1 after feature branches are ready.

Repository: example_hmi_dsl
Branch: integration/round-1
Worktree: ../example-hmi-integration
Goal: Merge approved branches in order, regenerate outputs if required, resolve conflicts, and run full validation.

Allowed paths:
- generated/
- package-lock.json
- integration notes or release notes assigned by the human maintainer

Forbidden paths:
- Unrelated feature changes outside integration scope

Shared dependencies:
- feat/shared-foundation
- feat/runtime-parser
- feat/ui-generator
- feat/examples
- feat/docs

Validation commands:
- npm run lint
- npm test
- npm run build

Requirements:
- Merge in the planned order.
- Do not force push or rewrite others' branches.
- Document conflicts, generated output updates, validation results, and remaining risks.
```

## 10. Questions For Human Confirmation

- Is the DSL contract stable, or must shared foundation happen first?
- Can any subtask edit the lockfile?
- Should `generated/` be committed, or regenerated only in integration?
````
