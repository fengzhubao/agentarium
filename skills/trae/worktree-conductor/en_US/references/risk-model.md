# Shared-File Risk Model

## Low Risk

Typical files:

- `README.md`
- `CHANGELOG.md`
- Append-only notes or simple docs.

Strategy:

- Parallel append-only edits are acceptable.
- Assign one integrator to clean up tone and duplication.

## Medium Risk

Typical files:

- Shared utilities.
- Shared docs pages.
- Sample data.
- Common test fixtures.
- Config templates used by multiple modules.

Strategy:

- Assign one owner.
- Other tasks should request changes instead of editing directly.
- If concurrent edits are necessary, declare dependency order first.

## High Risk

Typical files:

- Schemas.
- Interface contracts.
- IR or DSL core definitions.
- Code generators.
- Generated outputs.
- Database migrations.
- Package lockfiles.
- Git submodule pointers.

Strategy:

- Do not let multiple tasks edit these concurrently.
- If changes are required, create `feat/shared-foundation` first.
- Generated outputs should be updated by one integration task.
- Submodule pointers should be updated by one integrator.

## Decision Rules

- Separate directories do not guarantee separate ownership.
- Whoever changes a contract must explain downstream impact.
- Whoever changes a generator must update generated outputs or explicitly hand that to integration.
- If a file is needed by three or more tasks, default it to at least medium risk.

