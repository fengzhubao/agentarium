# 配置与行为契约

## 配置文件

默认读取仓库根目录下的 `.agent-context-sync.json`：

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

- 只支持 `source` 和 `targets` 两个字段。
- `source` 必须是非空 UTF-8 文本文件。
- `targets` 必须是非空、无重复的字符串数组。
- 路径相对于仓库根目录。脚本兼容 `/` 和 `\` 输入，但输出统一使用 `/`。
- 绝对路径、盘符路径、`..` 和解析后越出仓库的路径会被拒绝。
- 配置文件和共享源不能同时列为目标。
- `.git` 内部路径、`.env`、认证文件和私钥类文件名会被拒绝。

使用其他配置文件：

```text
python scripts/sync_agent_context.py check --repo-root <repo-root> --config config/agent-sync.json
```

## 受管区块

脚本维护固定 marker 之间的内容：

```markdown
<!-- agent-context-sync:start -->
<共享源内容>
<!-- agent-context-sync:end -->
```

- 目标没有 marker 时，`sync` 在末尾追加一个区块。
- 目标不存在时，`sync` 创建只含该区块的新 UTF-8 文件。
- 目标已有一个合法区块时，只替换区块内容。
- 任一 marker 缺失、重复、顺序错误或不独占一行时，整个计划失败，写入开始前停止。
- 共享源不能包含 marker。

## 行尾和编码

- 共享源和目标必须是 UTF-8。
- 现有 UTF-8 BOM 会保留。
- 现有目标的 LF 或 CRLF 风格用于新受管内容。
- 受管区块外的文本保持不变。
- 新文件默认使用 LF。

## 命令和退出码

| 命令 | 写入 | 退出码 0 | 退出码 1 | 退出码 2 |
| --- | --- | --- | --- | --- |
| `check` | 否 | 所有目标一致 | 存在漂移 | 配置或安全错误 |
| `diff` | 否 | 没有漂移 | 输出差异 | 配置或安全错误 |
| `sync` | 是 | 同步完成 | 不使用 | 配置、marker 或写入错误 |

脚本先为所有目标建立安全计划；如果任一目标 marker 损坏，不会先更新前面的目标。
