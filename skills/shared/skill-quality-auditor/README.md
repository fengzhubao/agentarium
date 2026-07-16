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

## Deterministic Preflight

Each locale is independently importable and includes the same zero-third-party-dependency validator. It requires Python 3.10 or newer. Run it from the selected locale root:

```text
python scripts/validate_agentarium.py --repo-root <repo-root> --skill <ID-or-slug> --strict
```

Omit `--skill` to validate the full catalog, or add `--format json` for machine-readable output. The preflight checks deterministic catalog, path, frontmatter, evidence-envelope, link, and high-confidence public-safety rules. It intentionally leaves behavioral locale parity, nuanced public-safety review, screenshots, and trial authenticity to an agent or human reviewer.

To stay dependency-free, the catalog reader supports the YAML subset used by schema v2: block mappings and sequences, quoted or simple scalars, simple inline lists, and inline comments. Advanced YAML features such as anchors, tags, merge keys, and block scalars are outside its supported input. If the catalog adopts those features, update the reader or use a full YAML implementation before relying on automated results.

## Current Status

Ready.

Both locale import roots were independently run in Codex on 2026-07-16 with public-safe evidence, strict deterministic validation, and manual parity, evidence, link, and safety review. A final maintainer release review confirmed the bilingual package, links, evidence, safety boundary, regression tests, and cross-platform CI. This release claim applies to the canonical shared package; it does not claim TRAE- or Claude-specific execution.

See `STATUS.md` for readiness details.
