# Catalog Schema v2 检查

## 必填顶层字段

`catalog/skills.yaml` 中每个 Skill 条目应包含：

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

## ID 与状态

- `id` 必须匹配 `^SKL-[0-9]{4}$`。
- ID 不应编码工具族，例如不要使用 `TRAE-0001`。
- `status` 必须来自 `catalog/status-policy.md`。
- 顶层状态必须不高于所有已实现 variant 的保守聚合状态。

## 包与工具字段

- `target_tools` 表示计划支持的 agent 工具族，可以包含尚未实现的工具。
- `supported_tools` 只列已经有可用 variant 的 package family，例如 `shared`、`trae`、`codex` 或 `claude`。
- 如果 `supported_tools` 非空，`variants` 应包含对应 package variant。
- 如果 `variants` 为空，状态通常应为 `candidate`。

## Agent 与模型适配

- `model_fit` 应描述能力要求，不要承诺适配某个会变化的模型品牌或版本。
- 好的条目应说明所需能力，例如文件访问、仓库检查、命令/工具使用、代码推理、长上下文对比、安全审查、写作质量或公开安全判断。
- 如果声称某个 Skill 已适配具体模型或 agent 版本，对应的 `STATUS.md` 或证据应记录这次试跑。

## Variant 字段

每个已实现 variant 应包含：

- `tool`
- `status`
- `package_root`
- `readme_file`
- `status_file`
- `examples_root`
- `locale_roots`

每个 locale root 应包含：

- `status`
- `import_root`
- `skill_file`
- `examples_root`
- `evidence`

## 路径规则

- `package_root` 指向多语言 Skill 包根目录。
- `import_root` 指向可独立导入的 locale 目录，并且必须直接包含 `SKILL.md`。
- `skill_file` 必须等于对应 `import_root/SKILL.md`。
- examples 路径应在 `examples/<package-family>/<slug>/<locale>/` 下。
