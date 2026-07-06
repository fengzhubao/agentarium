# Skill Quality Auditor

Skill Quality Auditor is a shared workflow Skill for auditing Agentarium Skill packages before publication, status changes, or merge review. The current importable package is the canonical shared package.

It checks catalog schema alignment, import roots, bilingual behavior parity, referenced files, examples, evidence gates, broken links, and public-safety risk. By default it reports findings without changing files unless the user explicitly asks for fixes.

## Languages

- `zh_CN`: Simplified Chinese
- `en_US`: English

## Package And Tool Support

- Current implemented package: shared package under `skills/shared/skill-quality-auditor/`.
- Intended shared workflow target: TRAE, Codex, Claude, and other agents that can inspect repository files.
- Future tool-specific package variants should preserve the same audit criteria while adapting import paths or tool-specific runtime details.

## Agent / Model Fit

- Suitable for agents that can read repository files, compare catalog metadata with package files, and inspect examples and references.
- Best with models that can produce structured review findings, judge bilingual parity, reason about status evidence, and spot public-safety risks.
- Not suitable for models without file access when the audit requires checking real paths, references, or examples.
- Not suitable for agents that cannot separate read-only findings from requested fixes.

## Main Use Cases

- Reviewing a new Skill package before it moves from `candidate` to `draft` or `sampled`.
- Checking whether a Skill has enough evidence for `sampled`, `trial-validated`, or `ready`.
- Auditing bilingual `zh_CN` and `en_US` instructions for behavioral drift.
- Finding missing references, examples, catalog paths, and public-safety issues.
- Producing a concise merge-review report for Skill changes.

## Current Status

Sampled.

The Skill has bilingual instructions, reference checklists, and public-safe sample input/output. It still needs real implemented-variant trial evidence before it can be marked `trial-validated`.

See `STATUS.md` for readiness details.
