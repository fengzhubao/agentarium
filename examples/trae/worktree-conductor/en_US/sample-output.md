# Worktree Conductor Sample Output

Note: this is a redacted sample showing the intended output shape. Save real TRAE SOLO trial output and screenshots after testing.

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
| Shared foundation | `feat/shared-foundation` | `../metanc-hmi-foundation` | Integrator | Confirm DSL contract, schema, and generation boundaries |
| Runtime parser | `feat/runtime-parser` | `../metanc-hmi-runtime` | Codex | Implement runtime parsing |
| UI generator | `feat/ui-generator` | `../metanc-hmi-generator` | TRAE | Implement component generation |
| Examples | `feat/examples` | `../metanc-hmi-examples` | Claude | Add example projects and demo inputs |
| Docs | `feat/docs` | `../metanc-hmi-docs` | TRAE or human | Write usage and integration guides |

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

## 5. Recommended Commands

```bash
git fetch origin
git switch main
git pull
git switch -c feat/shared-foundation
git worktree add ../metanc-hmi-runtime -b feat/runtime-parser
git worktree add ../metanc-hmi-generator -b feat/ui-generator
git worktree add ../metanc-hmi-examples -b feat/examples
git worktree add ../metanc-hmi-docs -b feat/docs
git worktree add ../metanc-hmi-integration -b integration/round-1
```

Adjust paths and branch names to the actual repository.

## 6. Branch Acceptance Checks

| Branch | Required Checks | Passing Standard |
| --- | --- | --- |
| `feat/shared-foundation` | `npm run lint`, `npm test` | Schema and contract changes do not break existing tests |
| `feat/runtime-parser` | `npm test -- runtime` | Runtime tests pass |
| `feat/ui-generator` | `npm test -- generator`, `npm run build` | Generator tests and build pass |
| `feat/examples` | `npm run build` | Examples can consume the current DSL shape |
| `feat/docs` | docs link check or human review | Steps can be followed by a new user |
| `integration/round-1` | `npm run lint`, `npm test`, `npm run build` | Full validation passes |

## 7. Integration Order

1. Merge `feat/shared-foundation`.
2. Merge `feat/runtime-parser`.
3. Merge `feat/ui-generator`.
4. Merge `feat/examples`.
5. Merge `feat/docs`.
6. Regenerate outputs and run full validation on `integration/round-1`.

## 8. Task Prompts For Agents

### Codex: Runtime Parser

```text
You are responsible for runtime DSL parsing. You are not alone in this repository.

Branch: feat/runtime-parser
Worktree: ../metanc-hmi-runtime
Allowed paths:
- runtime/
- tests/runtime/

Forbidden paths:
- definition/*.yaml
- schema/
- generated/
- package-lock.json

Validation commands:
- npm test -- runtime
- npm run lint

Finish with a change summary, validation results, risks, and follow-ups. Do not revert others' work. Do not expand the file scope.
```

## 9. Questions For Human Confirmation

- Is the DSL contract stable, or must shared foundation happen first?
- Can any subtask edit the lockfile?
- Should `generated/` be committed, or regenerated only in integration?
````
