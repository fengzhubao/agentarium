# Worktree Conductor Sample Input

Use Worktree Conductor to split this development task into a parallel git worktree plan.

## Repository

Example repository: `example_hmi_dsl`

Base branch: `main`

## Goal

Develop several HMI DSL areas at the same time:

- Runtime DSL parsing.
- UI component generation.
- Example projects.
- Documentation and usage guides.

## Desired Parallelism

Use 3 to 4 parallel agents. The tasks may be handed to TRAE, Claude, Codex, or separate sessions.

## Known Modules And Shared Areas

- `runtime/`: runtime parser logic.
- `generator/`: component generator logic.
- `examples/`: example projects.
- `docs/`: documentation.
- `definition/*.yaml`: shared DSL contract, high risk.
- `schema/`: schema definitions, high risk.
- `generated/`: generated outputs, should not be edited by multiple agents.
- `package-lock.json`: lockfile, should not be edited by multiple agents.

## Validation Commands

```bash
npm run lint
npm test
npm run build
```

## Output Requirements

- Decide whether parallel work is appropriate.
- Propose branches and worktree paths.
- Define file ownership and forbidden areas.
- Mark shared-file risks.
- Provide recommended commands.
- Provide branch acceptance checks.
- Provide integration order.
- Provide task prompts that can be copied to different agents.
