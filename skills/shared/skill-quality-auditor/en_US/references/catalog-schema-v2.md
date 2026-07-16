# Catalog Schema v2 Checks

## Required Top-Level Fields

Each Skill entry in `catalog/skills.yaml` should include:

- `id`
- `slug`
- `title`
- `category`
- `scope`
- `status`
- `summary_zh`
- `summary_en`
- `model_fit`
- `supported_tools`
- `target_tools`
- `required_locales`
- `variants`
- `tags`

## ID and Status

- `id` must match `^SKL-[0-9]{4}$`.
- IDs must not encode the tool family; do not use IDs like `TRAE-0001`.
- `status` must come from `catalog/status-policy.md`.
- The top-level status must not be higher than the conservative aggregate of implemented variants.
- `title`, `category`, `summary_zh`, and `summary_en` must be non-empty strings.
- `scope` must be `shared` or `tool-specific`.
- `tags`, `target_tools`, and non-empty `supported_tools` must contain unique, non-empty strings.
- Tool values must be declared by catalog `tool_families`.

## Package And Tool Fields

- `target_tools` lists intended agent tool families, including tools not implemented yet.
- `supported_tools` lists only package families with usable variants, such as `shared`, `trae`, `codex`, or `claude`.
- If `supported_tools` is non-empty, `variants` should contain matching package variants.
- If `variants` is empty, the status should usually be `candidate`.

## Agent And Model Fit

- `model_fit` is a mapping with non-empty `suitable_for` and `not_suitable_for` string lists. These lists describe capability requirements, not guaranteed compatibility with a changing model brand or version.
- Good entries mention required agent/model capabilities such as file access, repository inspection, command/tool use, code reasoning, long-context comparison, security review, writing quality, or public-safety judgment.
- If a Skill is claimed to work with a specific model or agent version, the matching `STATUS.md` or evidence should record that trial.

## Variant Fields

Each implemented variant should include:

- `tool`
- `status`
- `package_root`
- `readme_file`
- `status_file`
- `examples_root`
- `locale_roots`

Each locale root should include:

- `status`
- `import_root`
- `skill_file`
- `examples_root`
- `evidence`

## Path Rules

- `package_root` points to the multi-locale Skill package root.
- `import_root` points to an independently importable locale directory and must directly contain `SKILL.md`.
- `skill_file` must equal the matching `import_root/SKILL.md`.
- Example paths should live under `examples/<package-family>/<slug>/<locale>/`.
