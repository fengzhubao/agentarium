# Agent Context Sync 示例输出

说明：这是公开安全样例，路径和规则内容均为占位示例。

## 只读检查

```text
python scripts/sync_agent_context.py check --repo-root <repo-root>
```

```text
DRIFT AGENTS.md: managed block differs
DRIFT CLAUDE.md: managed block missing
DRIFT .cursor/rules/shared.mdc: target missing
Summary: 0 synced, 3 drifted
```

退出码：`1`。没有文件被修改。

## 差异复核

```text
python scripts/sync_agent_context.py diff --repo-root <repo-root>
```

差异显示：

- `AGENTS.md` 只更新已有受管区块。
- `CLAUDE.md` 保留开头的 Claude 专属说明，并在末尾追加受管区块。
- `.cursor/rules/shared.mdc` 将被创建，只包含受管区块。

目标中的受管区块形态：

```markdown
<!-- agent-context-sync:start -->
- 先读取仓库说明再修改文件。
- 保留用户已有改动。
- 提交前运行仓库验证。
<!-- agent-context-sync:end -->
```

## 授权同步

```text
python scripts/sync_agent_context.py sync --repo-root <repo-root>
```

```text
UPDATED AGENTS.md
UPDATED CLAUDE.md
UPDATED .cursor/rules/shared.mdc
Summary: 3 updated, 0 already synced
```

## 最终验证

再次运行 `check`：

```text
OK AGENTS.md
OK CLAUDE.md
OK .cursor/rules/shared.mdc
Summary: 3 synced, 0 drifted
```

退出码：`0`。

人工复核：三个目标的工具专属前言和尾注均保持不变；新建目标只包含受管区块。没有执行 commit 或 push。
