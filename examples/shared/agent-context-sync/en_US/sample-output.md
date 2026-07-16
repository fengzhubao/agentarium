# Agent Context Sync Sample Output

Note: this is a public-safe sample using placeholder paths and rules.

## Read-Only Check

```text
python scripts/sync_agent_context.py check --repo-root <repo-root>
```

```text
DRIFT AGENTS.md: managed block differs
DRIFT CLAUDE.md: managed block missing
DRIFT .cursor/rules/shared.mdc: target missing
Summary: 0 synced, 3 drifted
```

Exit code: `1`. No files changed.

## Diff Review

```text
python scripts/sync_agent_context.py diff --repo-root <repo-root>
```

The diff shows:

- `AGENTS.md` changes only its existing managed block.
- `CLAUDE.md` preserves its Claude-specific preface and appends a managed block.
- `.cursor/rules/shared.mdc` will be created with only the managed block.

Managed-block shape:

```markdown
<!-- agent-context-sync:start -->
- Read repository instructions before editing files.
- Preserve existing user changes.
- Run repository validation before committing.
<!-- agent-context-sync:end -->
```

## Authorized Synchronization

```text
python scripts/sync_agent_context.py sync --repo-root <repo-root>
```

```text
UPDATED AGENTS.md
UPDATED CLAUDE.md
UPDATED .cursor/rules/shared.mdc
Summary: 3 updated, 0 already synced
```

## Final Validation

Run `check` again:

```text
OK AGENTS.md
OK CLAUDE.md
OK .cursor/rules/shared.mdc
Summary: 3 synced, 0 drifted
```

Exit code: `0`.

Manual review: target-specific prefaces and trailing notes remained unchanged; the new target contains only the managed block. No commit or push was performed.
