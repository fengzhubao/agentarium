# SKL-0004 en_US Codex Trial Record

## Verdict

PASS. The complete `check → diff → sync → check` flow behaved as designed. Tool-specific prefaces and trailing notes remained unchanged, a missing target was created, and the final check reported zero drift.

## Trial Record

- Tool: Codex
- Tool version: `codex-cli 0.144.4`; the underlying session model and service build were not exposed
- Python version: `3.14.3`
- Trial date: `2026-07-16` (`Asia/Shanghai`)
- Locale: `en_US`
- Import root: `<repo-root>/skills/shared/agent-context-sync/en_US`
- Input summary: Synchronized one English shared source into three targets in a public-safe temporary repository. `AGENTS.md` had an old managed block plus unmanaged content, `CLAUDE.md` had tool-specific content only, and the Cursor target was missing.
- Output or artifact path: `examples/shared/agent-context-sync/en_US/real-trial-output.md`
- Known failures or warnings: The initial `check` and `diff` intentionally returned exit code `1` for three drifted targets; no runtime failure occurred.
- Public-safety review: Pass; the temporary path is represented as `<trial-repo>`, and the record contains no credential, personal information, private URL, account data, or screenshot.

## Execution

Run from the English import root with the locale-local script:

```text
python -S scripts/sync_agent_context.py check --repo-root <trial-repo>
python -S scripts/sync_agent_context.py diff --repo-root <trial-repo>
python -S scripts/sync_agent_context.py sync --repo-root <trial-repo>
python -S scripts/sync_agent_context.py check --repo-root <trial-repo>
```

Initial check:

```text
DRIFT AGENTS.md: managed block differs
DRIFT CLAUDE.md: managed block missing
DRIFT .cursor/rules/shared.mdc: target missing
Summary: 0 synced, 3 drifted
```

Synchronization:

```text
UPDATED AGENTS.md
UPDATED CLAUDE.md
UPDATED .cursor/rules/shared.mdc
Summary: 3 updated, 0 already synced
```

Final check:

```text
OK AGENTS.md
OK CLAUDE.md
OK .cursor/rules/shared.mdc
Summary: 3 synced, 0 drifted
```

## Manual Review

- `diff` replaced only the managed block in `AGENTS.md`.
- The Claude-specific content remained byte-for-byte present, with the managed block appended at the end.
- The missing Cursor target contained only the managed block.
- `check` and `diff` did not write; targets changed only after explicit `sync` execution.
- Script SHA-256: `675AC02438904895A09F35FDED5477081FE453B3174AC010EC3C4AD21FF06984`; both locale copies were byte-identical.

## Scope Boundary

- This real trial ran in Codex; it does not claim TRAE, Claude, or Cursor imported the Skill.
- Eighteen regression tests cover CRLF, UTF-8 BOM, malformed markers, sensitive paths, path escape, and no-partial-write behavior.
- No automatic commit or push occurred.
