# Skill Quality Audit Report

## Verdict

PASS WITH WARNINGS

Target: SKL-0002 / `worktree-conductor`
Claimed status: `sampled`
Supported status: `sampled`

当前文件结构、双语说明、runtime references 和样例证据支持 `sampled`。还不能支持 `trial-validated`，因为当前已实现包没有真实目标工具试运行输出或脱敏试运行记录。

## Findings

### BLOCKER

- None.

### HIGH

- None.

### MEDIUM

- `skills/shared/worktree-conductor/STATUS.md`: 当前已实现包的真实目标工具试运行证据仍缺失。Impact: 不能提级到 `trial-validated` 或 `ready`。Fix: 为 `zh_CN` 和 `en_US` 各补一条公开安全的试运行记录，包含工具、locale、日期或上下文、输入摘要、观察结果和公开安全结论。

### LOW

- `skills/shared/worktree-conductor/STATUS.md`: 截图和最终社区帖仍是可选 pending 项。Impact: 不阻断 `sampled`，但会影响公开投稿材料完整度。Fix: 完成真实试运行后再补脱敏截图和最终帖子。

## Check Matrices

| Check | Result | Notes |
| --- | --- | --- |
| Catalog schema v2 | pass | ID、package variant、locale roots 和 evidence 路径存在。 |
| Package structure | pass | 根 README/STATUS、两个 locale 的 `SKILL.md` 和 references 存在。 |
| Locale parity | pass | 中英文版本覆盖同一类 worktree 编排、命令安全和输出结构。 |
| References and links | pass | `SKILL.md` 引用的 runtime reference 文件存在。 |
| Evidence gates | pass with warning | 样例支持 `sampled`；真实试运行证据缺失。 |
| Public safety | pass | 样例使用占位路径和公开安全项目名，未发现密钥或私有 URL。 |

## Required Next Actions

- 保持当前状态为 `sampled`。
- 不要标记为 `trial-validated`，直到两个 locale 都有真实工具试运行证据。
- 公开发布前重新运行公开安全检查。

## Files Inspected

- `catalog/skills.yaml`
- `catalog/status-policy.md`
- `skills/shared/worktree-conductor/README.md`
- `skills/shared/worktree-conductor/STATUS.md`
- `skills/shared/worktree-conductor/zh_CN/SKILL.md`
- `skills/shared/worktree-conductor/en_US/SKILL.md`
- `skills/shared/worktree-conductor/zh_CN/references/`
- `skills/shared/worktree-conductor/en_US/references/`
- `examples/shared/worktree-conductor/zh_CN/`
- `examples/shared/worktree-conductor/en_US/`

## Not Checked / Assumptions

- 未运行真实目标工具导入和调用。
- 未检查截图，因为当前样例没有提交截图文件。
