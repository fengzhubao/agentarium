# 状态证据门槛

## candidate

需要：

- 唯一 `id`。
- `slug`、`title`、scope、summary、tags。
- 非空 `target_tools`。
- 不要求文件路径存在。

## draft

除 candidate 外，需要每个已实现 package variant 具备：

- `package_root` 存在。
- `README.md` 和 `STATUS.md` 存在。
- Required locale 的 `import_root` 存在。
- 每个 `import_root` 直接包含 `SKILL.md`。
- `SKILL.md` frontmatter 只有 `name` 和 `description`。
- `SKILL.md` 提到的 `references/` 文件存在。

## sampled

除 draft 外，需要每个 required locale 具备：

- 公开安全的 `sample-input.md`。
- 公开安全的 `sample-output.md`。
- 样例路径位于 `examples/<package-family>/<skill-name>/<locale>/`。

## trial-validated

除 sampled 外，需要每个 required locale 具备真实工具试运行证据：

- 工具和版本，如已知。
- 试运行日期或上下文。
- locale。
- 输入摘要。
- 输出或产物路径。
- 已知失败或警告。
- 公开安全检查结果。

## ready

除 trial-validated 外，需要：

- 所有 required locale 至少为 `trial-validated`。
- 公开安全检查通过。
- 相对链接可解析。
- `STATUS.md` 没有阻断 ready 声明的 pending evidence。

## 审计原则

- 只按已有证据判断，不按计划判断。
- 若 `STATUS.md` 高于 catalog 证据，报告为状态不一致。
- 若某个 locale 缺证据，variant 和顶层状态都要按较低状态聚合。
