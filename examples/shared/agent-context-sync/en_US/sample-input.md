# Agent Context Sync Sample Input

Check and synchronize shared agent rules in an example repository.

## Scope

- Repository root: `<repo-root>`
- Shared source: `.agent-context/shared.md`
- Targets: `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/shared.mdc`
- Run read-only `check` and `diff` first.
- After I confirm that the diff affects only managed blocks, `sync` is authorized.

## Configuration

```json
{
  "source": ".agent-context/shared.md",
  "targets": [
    "AGENTS.md",
    "CLAUDE.md",
    ".cursor/rules/shared.mdc"
  ]
}
```

## Shared Source Summary

- Read repository instructions before editing files.
- Preserve existing user changes.
- Run repository validation before committing.

## Output Requirements

- Report drift for every target.
- Show the proposed diff.
- Check again after synchronization.
- Demonstrate that target-specific rules were not overwritten.
