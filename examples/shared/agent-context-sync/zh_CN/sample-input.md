# Agent Context Sync 示例输入

请检查并同步一个示例仓库里的公共 agent 规则。

## 范围

- 仓库根目录：`<repo-root>`
- 共享源：`.agent-context/shared.md`
- 目标：`AGENTS.md`、`CLAUDE.md`、`.cursor/rules/shared.mdc`
- 默认先执行只读 `check` 和 `diff`。
- 我确认差异只涉及受管区块后，允许执行 `sync`。

## 配置

```json
{
  "source": ".agent-context/shared.md",
  "targets": [
    "AGENTS.md",
    "CLAUDE.md",
    ".cursor/rules/shared.mdc"
  ]
}
```

## 共享源摘要

- 先读取仓库说明再修改文件。
- 保留用户已有改动。
- 提交前运行仓库验证。

## 输出要求

- 报告每个目标是否漂移。
- 展示拟议差异。
- 同步后再次检查。
- 证明目标文件里的工具专属规则没有被覆盖。
