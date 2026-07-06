# 审计流程

## 1. 建立审计范围

- 记录 Skill ID、slug、工具族、目标状态和要检查的 locale。
- 判断用户是只要审计报告，还是明确要求修复。
- 如果用户没有指定目标状态，按当前 `catalog/skills.yaml` 与 `STATUS.md` 声明审计。

## 2. 读取治理材料

至少读取：

- `AGENTS.md`
- `README.md`
- `catalog/skills.yaml`
- `catalog/status-policy.md`
- `docs/importing.md`
- `docs/localization.md`
- `docs/safety.md`
- `docs/skill-completeness.md`

## 3. 收集目标 Skill 文件

检查以下路径是否存在，并记录缺失项：

- `skills/<package-family>/<slug>/README.md`
- `skills/<package-family>/<slug>/STATUS.md`
- `skills/<package-family>/<slug>/zh_CN/SKILL.md`
- `skills/<package-family>/<slug>/en_US/SKILL.md`
- 两个 locale 的 `references/`
- `examples/<package-family>/<slug>/zh_CN/sample-input.md`
- `examples/<package-family>/<slug>/zh_CN/sample-output.md`
- `examples/<package-family>/<slug>/en_US/sample-input.md`
- `examples/<package-family>/<slug>/en_US/sample-output.md`

## 4. 执行检查

按顺序执行：

1. 目录 schema 和路径检查。
2. Skill 包结构检查。
3. `SKILL.md` frontmatter 检查。
4. 双语行为一致性检查。
5. 引用、链接和样例路径检查。
6. 状态证据门槛检查。
7. 公开安全检查。

## 5. 输出结论

- 先给出 Verdict。
- Findings 按 BLOCKER、HIGH、MEDIUM、LOW 排序。
- 每条 finding 包含位置、问题、影响和建议。
- 如果没有阻断项，仍列出剩余风险和未验证内容。
