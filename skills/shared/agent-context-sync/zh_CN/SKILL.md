---
name: agent-context-sync
description: 当仓库需要从一个共享规则源检查、比较或同步 AGENTS.md、CLAUDE.md、Cursor rules 等多个 agent 指令文件时使用。通过受管区块保留各工具专属内容；默认只读执行 check/diff，只有用户明确授权修改时才运行 sync。
---

# Agent Context Sync

使用一个共享 Markdown 源维护多个 agent 指令文件中的公共规则，同时保留受管区块以外的工具专属内容。

## 默认行为

- 默认先运行 `check`，发现漂移后运行 `diff`。
- `check` 和 `diff` 不修改文件。
- 只有用户明确要求同步、修复或更新时才运行 `sync`。
- 不要手工复制整份目标文件；使用 locale 内的确定性脚本。
- 发现路径越界、重复目标、无效 UTF-8、缺失/重复 marker 时停止，不尝试猜测修复。

## 输入

确认或推断：

- 仓库根目录。
- 配置文件；默认是仓库根目录下的 `.agent-context-sync.json`。
- 一个共享源文件。
- 一个或多个目标指令文件。
- 用户是否只要检查，还是明确授权同步。

配置格式、marker 和退出码见 `references/configuration.md`。

## 工作流

1. 检查范围
   - 确认仓库根目录和配置文件位于仓库内。
   - 查看目标文件中是否已有工具专属规则和受管区块。
   - 不读取或同步凭据、认证配置、私有数据或与 agent 指令无关的敏感文件。

2. 只读检查

   ```text
   python scripts/sync_agent_context.py check --repo-root <repo-root>
   ```

   返回 `0` 表示一致，`1` 表示存在漂移，`2` 表示配置或安全错误。

3. 查看差异

   ```text
   python scripts/sync_agent_context.py diff --repo-root <repo-root>
   ```

   复核差异只涉及 `<!-- agent-context-sync:start -->` 与 `<!-- agent-context-sync:end -->` 之间的内容，或者给尚无区块的目标追加新区块。

4. 明确授权后同步

   ```text
   python scripts/sync_agent_context.py sync --repo-root <repo-root>
   ```

   `sync` 可以创建缺失目标，但新文件只包含受管区块。已有目标中受管区块以外的内容必须保持不变。

5. 验证
   - 再运行 `check`，必须返回 `0`。
   - 检查 `git diff -- <targets>`，确认工具专属规则未改变。
   - 运行仓库自己的验证命令。

## 输出

报告：

- 使用的配置和共享源相对路径。
- 每个目标是 `OK`、`DRIFT` 还是 `UPDATED`。
- 是否创建了新目标。
- 验证命令和退出码。
- 未检查内容、风险和需要人工确认的差异。

## 安全边界

- 只接受仓库内相对配置路径、源路径和目标路径。
- 不把认证文件、`.env`、密钥、Cookie、Token 或私有配置作为共享源或目标。
- 不删除目标文件中的非受管内容。
- 不自动提交或推送同步结果。
- 不在 marker 损坏时进行写入。
