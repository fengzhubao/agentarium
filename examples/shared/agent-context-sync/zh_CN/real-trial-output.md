# SKL-0004 zh_CN Codex 真实试跑记录

## 结论

PASS。`check → diff → sync → check` 完整流程按预期工作，工具专属前言和尾注保持不变，缺失目标被创建，最终检查为 0 drift。

## 试跑信息

- Tool: Codex
- Tool version: `codex-cli 0.144.4`；session 底层模型和服务 build 未暴露
- Python version: `3.14.3`
- Trial date: `2026-07-16`（Asia/Shanghai）
- Locale: `zh_CN`
- Import root: `<repo-root>/skills/shared/agent-context-sync/zh_CN`
- Input summary: 在公开安全临时仓库中，从一个中文共享源同步三个目标；`AGENTS.md` 有旧受管区块和区块外内容，`CLAUDE.md` 只有工具专属内容，Cursor 目标不存在。
- Output or artifact path: `examples/shared/agent-context-sync/zh_CN/real-trial-output.md`
- Known failures or warnings: 首次 `check` 和 `diff` 按设计以退出码 `1` 报告 3 个 drift；没有运行错误。
- Public-safety review: Pass；临时路径已替换为 `<trial-repo>`，记录不包含凭据、个人信息、私有 URL、账号数据或截图。

## 执行流程

从中文 import root 使用 locale-local 脚本执行：

```text
python -S scripts/sync_agent_context.py check --repo-root <trial-repo>
python -S scripts/sync_agent_context.py diff --repo-root <trial-repo>
python -S scripts/sync_agent_context.py sync --repo-root <trial-repo>
python -S scripts/sync_agent_context.py check --repo-root <trial-repo>
```

首次检查：

```text
DRIFT AGENTS.md: managed block differs
DRIFT CLAUDE.md: managed block missing
DRIFT .cursor/rules/shared.mdc: target missing
Summary: 0 synced, 3 drifted
```

同步：

```text
UPDATED AGENTS.md
UPDATED CLAUDE.md
UPDATED .cursor/rules/shared.mdc
Summary: 3 updated, 0 already synced
```

最终检查：

```text
OK AGENTS.md
OK CLAUDE.md
OK .cursor/rules/shared.mdc
Summary: 3 synced, 0 drifted
```

## 人工复核

- `diff` 只替换 `AGENTS.md` 的受管区块。
- `CLAUDE.md` 的工具专属内容逐字保留，受管区块追加在文件末尾。
- 缺失的 Cursor 目标只包含受管区块。
- `check` 和 `diff` 没有写入；只有明确执行 `sync` 后目标才变化。
- 同步脚本 SHA-256：`675AC02438904895A09F35FDED5477081FE453B3174AC010EC3C4AD21FF06984`；两个 locale 副本字节一致。

## 范围边界

- 本次真实试跑运行在 Codex；未声称 TRAE、Claude 或 Cursor 已导入该 Skill。
- CRLF、UTF-8 BOM、marker 损坏、敏感路径、路径越界和无部分写入行为由 18 项回归测试覆盖。
- 没有自动 commit 或 push。
