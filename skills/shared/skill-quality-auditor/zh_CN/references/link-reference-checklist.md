# 链接和引用检查

## SKILL.md runtime 引用

- `SKILL.md` 中列出的每个 `references/...` 文件必须存在。
- 引用路径应相对于该 locale 的 `SKILL.md`。
- 如果一个 locale 新增引用，另一个 locale 应有对应行为的引用。

## Markdown 链接

- 检查相对链接是否能从当前文件位置解析。
- 检查链接目标是否在仓库内，除非明确是公开外部文档。
- 不要把本地绝对路径作为公开链接。

## 样例路径

- `sample-input.md` 和 `sample-output.md` 应位于 `examples/<package-family>/<slug>/<locale>/`。
- catalog evidence 路径应指向真实文件。
- `examples_root` 应指向 locale 目录或 Skill 示例根目录，不应混用不存在路径。

## 断链报告格式

每个断链 finding 包含：

- 引用文件。
- 原始链接或路径。
- 解析基准目录。
- 期望存在的目标。
- 建议修复路径。
