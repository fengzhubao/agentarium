# 样例输入：审计 Agent Context Sync

请使用 Skill Quality Auditor 审计 Agentarium 中的 SKL-0004 `agent-context-sync`。

目标：

- 判断 catalog、README、STATUS、双语 `SKILL.md`、references 和 examples 是否支持当前状态。
- 当前目标状态是 `trial-validated`。
- 默认只输出审计报告，不修改文件。

审计范围：

- `catalog/skills.yaml`
- `catalog/status-policy.md`
- `skills/shared/agent-context-sync/README.md`
- `skills/shared/agent-context-sync/STATUS.md`
- `skills/shared/agent-context-sync/zh_CN/SKILL.md`
- `skills/shared/agent-context-sync/en_US/SKILL.md`
- `skills/shared/agent-context-sync/zh_CN/references/`
- `skills/shared/agent-context-sync/en_US/references/`
- `examples/shared/agent-context-sync/zh_CN/`
- `examples/shared/agent-context-sync/en_US/`
