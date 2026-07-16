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
- `docs/publishing.md`
- `docs/localization.md`
- `docs/safety.md`
- `docs/skill-completeness.md`

## 3. 收集目标 Skill 文件

先根据 catalog 状态和 `SKILL.md` 的实际引用确定必需文件，再检查路径并记录缺失项。对所有已实现 variant，要求：

- `skills/<package-family>/<slug>/README.md`
- `skills/<package-family>/<slug>/STATUS.md`
- `skills/<package-family>/<slug>/zh_CN/SKILL.md`
- `skills/<package-family>/<slug>/en_US/SKILL.md`

仅当对应 `SKILL.md` 引用 supporting files 时，还要求该 locale 的 `references/` 及被引用文件。

仅当声明状态为 `sampled` 或更高时，还要求：

- `examples/<package-family>/<slug>/zh_CN/sample-input.md`
- `examples/<package-family>/<slug>/zh_CN/sample-output.md`
- `examples/<package-family>/<slug>/en_US/sample-input.md`
- `examples/<package-family>/<slug>/en_US/sample-output.md`

仅当声明状态为 `trial-validated` 或更高时，还要求每个 required locale 的真实试运行证据路径。

`candidate` 没有已实现 variant 时，不要求这些 package 路径存在。

## 4. 执行检查

如果当前 locale 包含 `scripts/validate_agentarium.py` 且 Python 可用，先运行：

```text
python scripts/validate_agentarium.py --repo-root <repo-root> --skill <ID-or-slug> --strict
```

记录命令、退出码和发现。脚本负责 schema、路径、frontmatter、证据文件外壳、相对链接和高置信公开安全模式；它不判断试运行元数据是否完整，也不判断证据语义或真实性。这些内容以及双语语义一致性、截图脱敏仍必须按 `catalog/status-policy.md` 人工判断。

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
