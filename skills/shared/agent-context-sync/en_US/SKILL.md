---
name: agent-context-sync
description: Use when a repository needs to check, diff, or synchronize shared instructions from one source into AGENTS.md, CLAUDE.md, Cursor rules, or other agent context files. Preserve tool-specific content through managed blocks; run check/diff read-only by default and run sync only after explicit authorization.
---

# Agent Context Sync

Maintain shared rules from one Markdown source across agent instruction files while preserving tool-specific content outside the managed block.

## Default Behavior

- Run `check` first, then `diff` when drift exists.
- `check` and `diff` do not modify files.
- Run `sync` only when the user explicitly asks to synchronize, fix, or update files.
- Do not copy whole target files manually; use the deterministic locale-local script.
- Stop on path escape, duplicate targets, invalid UTF-8, or missing/duplicate markers instead of guessing a repair.

## Inputs

Confirm or infer:

- Repository root.
- Configuration file; default `.agent-context-sync.json` at the repository root.
- One shared source file.
- One or more target instruction files.
- Whether the user requested read-only inspection or explicitly authorized synchronization.

See `references/configuration.md` for the config schema, markers, and exit codes.

## Workflow

1. Inspect scope
   - Confirm the repository root and config stay inside the repository.
   - Inspect target files for tool-specific rules and existing managed blocks.
   - Do not read or synchronize credentials, authentication config, private data, or sensitive files unrelated to agent instructions.

2. Check read-only

   ```text
   python scripts/sync_agent_context.py check --repo-root <repo-root>
   ```

   Exit `0` means synchronized, `1` means drift, and `2` means a configuration or safety error.

3. Review the diff

   ```text
   python scripts/sync_agent_context.py diff --repo-root <repo-root>
   ```

   Confirm changes affect only content between `<!-- agent-context-sync:start -->` and `<!-- agent-context-sync:end -->`, or append a new block to a target that has none.

4. Synchronize after explicit authorization

   ```text
   python scripts/sync_agent_context.py sync --repo-root <repo-root>
   ```

   `sync` may create a missing target, but a new file contains only the managed block. Existing content outside the block must remain unchanged.

5. Validate
   - Run `check` again and require exit `0`.
   - Inspect `git diff -- <targets>` and confirm tool-specific rules did not change.
   - Run repository-specific validation commands.

## Output

Report:

- Config and shared-source repository-relative paths.
- Whether each target is `OK`, `DRIFT`, or `UPDATED`.
- Whether any target was created.
- Validation commands and exit codes.
- Unchecked areas, risks, and differences requiring human confirmation.

## Safety Boundary

- Accept only repository-relative config, source, and target paths.
- Do not use authentication files, `.env`, keys, cookies, tokens, or private config as a source or target.
- Never delete unmanaged target content.
- Do not commit or push synchronization results automatically.
- Do not write when markers are malformed.
