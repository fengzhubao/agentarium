# Configuration And Behavior Contract

## Configuration File

The default file is `.agent-context-sync.json` at the repository root:

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

- Only `source` and `targets` are supported.
- `source` must be a non-empty UTF-8 text file.
- `targets` must be a non-empty array of unique strings.
- Paths are relative to the repository root. The script accepts `/` or `\` input and reports canonical `/` paths.
- Absolute paths, drive paths, `..`, and paths that resolve outside the repository are rejected.
- The config file and shared source cannot also be targets.
- Paths inside `.git`, `.env` files, authentication files, and private-key filenames are rejected.

Use a different config file with:

```text
python scripts/sync_agent_context.py check --repo-root <repo-root> --config config/agent-sync.json
```

## Managed Block

The script owns content between fixed markers:

```markdown
<!-- agent-context-sync:start -->
<shared source content>
<!-- agent-context-sync:end -->
```

- When a target has no markers, `sync` appends one block.
- When a target is missing, `sync` creates a UTF-8 file containing only the block.
- When a target has one valid block, only that block is replaced.
- A missing, duplicate, reversed, or non-line-isolated marker fails the whole plan before writes begin.
- The shared source must not contain either marker.

## Line Endings And Encoding

- The shared source and targets must be UTF-8.
- An existing UTF-8 BOM is preserved.
- Existing LF or CRLF target style is used inside the managed block.
- Text outside the managed block remains unchanged.
- New files use LF.

## Commands And Exit Codes

| Command | Writes | Exit 0 | Exit 1 | Exit 2 |
| --- | --- | --- | --- | --- |
| `check` | No | All targets synchronized | Drift exists | Config or safety error |
| `diff` | No | No drift | Prints differences | Config or safety error |
| `sync` | Yes | Synchronization completed | Not used | Config, marker, or write error |

The script builds a safe plan for every target first. If any target has malformed markers, earlier targets are not updated.
