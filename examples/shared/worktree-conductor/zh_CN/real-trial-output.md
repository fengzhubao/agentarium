# SKL-0002 zh_CN Codex 真实试跑记录

## 试跑信息

- Tool: Codex
- Tool version: `codex-cli 0.144.4`；session 底层模型和服务 build 未暴露
- Trial date: `2026-07-16`（Asia/Shanghai）
- Locale: `zh_CN`
- Import root: `<repo-root>/skills/shared/worktree-conductor/zh_CN`
- Input summary: 检查公开仓库 `agentarium` 的当前分支、工作区、已有 worktree、目标分支和相关目录，为实现 SKL-0004 `agent-context-sync` 规划安全的多 worktree 开发方案。
- Output or artifact path: `examples/shared/worktree-conductor/zh_CN/real-trial-output.md`
- Known failures or warnings: 当前 `main` 有已授权的 SKL-0003 发布状态改动，因此计划明确禁止立即创建 worktree，要求先由集成负责人提交或处理这些改动。
- Public-safety review: Pass；记录只使用公开仓库名、相对仓库路径和示例 worktree 路径，不包含本机绝对路径、账号、个人信息、私有 URL、凭据或截图。

## 观察结果

PASS。Skill 生成了完整的十段式计划，识别了脏工作区和高风险共享文件，给出串行 shared foundation、后续并行边界、验收命令、集成顺序和可分发任务提示词。试跑只执行只读 Git 预检查，没有创建分支或 worktree。

# Worktree Conductor Plan

## 1. 并行可行性判断

- 结论：适合在共享接口锁定后并行；当前不能立即创建 worktree。
- 原因：
  - `catalog/skills.yaml`、根 `README.md`、CI workflow 和两个 locale 的脚本副本属于共享高风险区域。
  - 中文说明、英文说明和核心脚本/测试可以在接口确定后分开处理。
  - 当前 `main` 有 SKL-0003 发布复核改动，必须先由当前集成负责人保留并提交，不能让新 worktree 绕过这批未提交状态。
- 建议并行度：shared foundation 串行完成后，最多 3 个实现任务加 1 个集成任务。

## 2. 推荐分支 / worktree 拆分

| 任务 | 分支 | Worktree 路径 | 负责人 | 目标 |
| --- | --- | --- | --- | --- |
| Shared foundation | `feat/context-sync-foundation` | `../agentarium-context-foundation` | Integrator | 锁定 marker、配置 schema、CLI 和退出码 |
| 核心脚本与测试 | `feat/context-sync-core` | `../agentarium-context-core` | Core agent | 实现双语包内相同脚本和标准库测试 |
| 中文包 | `feat/context-sync-zh` | `../agentarium-context-zh` | zh agent | 编写中文 SKILL、reference 和示例 |
| 英文包 | `feat/context-sync-en` | `../agentarium-context-en` | en agent | 编写英文 SKILL、reference 和示例 |
| 集成与目录 | `integration/context-sync` | `../agentarium-context-integration` | Integrator | 同步 catalog、README、STATUS、CI 并全量验证 |

## 3. 文件归属与禁止触碰范围

| 任务 | 允许修改 | 禁止触碰 | 依赖 |
| --- | --- | --- | --- |
| Shared foundation | 设计记录或集成负责人指定文件 | 现有 Skill 包 | 当前 SKL-0003 改动先提交 |
| 核心脚本与测试 | 两个 locale 的 `scripts/sync_agent_context.py`、`tests/test_sync_agent_context.py` | catalog、README、locale 文档 | 已锁定 CLI 契约 |
| 中文包 | `skills/shared/agent-context-sync/zh_CN/`、对应中文 examples | 英文包、catalog、测试 | CLI 契约 |
| 英文包 | `skills/shared/agent-context-sync/en_US/`、对应英文 examples | 中文包、catalog、测试 | CLI 契约 |
| 集成与目录 | package README/STATUS、`catalog/skills.yaml`、根 README、CI | 无关 Skill 内容 | 所有子任务 |

## 4. 共享文件风险表

| 文件/区域 | 风险 | 原因 | 策略 |
| --- | --- | --- | --- |
| `catalog/skills.yaml` | 高 | 决定状态、路径和证据聚合 | 只由集成负责人修改 |
| `.github/workflows/validate-agentarium.yml` | 高 | 影响所有平台 CI | 只在集成阶段修改 |
| 两个 locale 的同步脚本 | 高 | 必须保持字节一致 | 同一 core owner 同时维护 |
| `tests/` | 中 | 覆盖公共行为契约 | 由 core owner 修改，集成负责人复核 |
| 两个 locale 的 `SKILL.md` | 中 | 行为必须一致 | 分开编写后做双语 parity review |
| 根 `README.md` | 中 | 同时包含 SKL-0003 状态变更 | 只由当前集成负责人修改 |

## 5. 命令安全预检查

```text
git branch --show-current
git status --short
git worktree list
git branch --list feat/context-sync-foundation
git branch --list feat/context-sync-core
git branch --list feat/context-sync-zh
git branch --list feat/context-sync-en
git branch --list integration/context-sync
```

观察到当前为 `main`、只有一个 worktree，目标分支不存在，但工作区不干净。先由当前负责人提交或明确处理 SKL-0003 改动，再执行任何 `git worktree add`。不要使用 `git reset --hard`、`git clean -fd` 或 force push。

## 6. 推荐命令

当前只推荐预检查。工作区干净后，可按实际路径调整并执行：

```text
git fetch origin
git switch main
git pull --ff-only
git worktree add ../agentarium-context-foundation -b feat/context-sync-foundation
```

shared foundation 合并后，再从更新后的基线创建 core、zh、en 和 integration worktree。

## 7. 分支验收清单

| 分支 | 必跑检查 | 通过标准 |
| --- | --- | --- |
| `feat/context-sync-core` | `python -m unittest tests.test_sync_agent_context -v` | check/diff/sync、路径安全和 LF/CRLF 测试通过 |
| `feat/context-sync-zh` | 聚焦 Skill 审计 | frontmatter、引用、示例和安全检查通过 |
| `feat/context-sync-en` | 聚焦 Skill 审计 | 与中文行为一致，引用和示例通过 |
| `integration/context-sync` | 全仓 strict validator、unittest、`git diff --check` | 0 errors、0 warnings、全部测试通过 |

## 8. 集成顺序

1. 先完成并锁定 shared foundation 的 marker、配置和 CLI 契约。
2. 合并核心脚本与测试。
3. 合并中文包和英文包。
4. 集成负责人同步两个脚本副本，更新 catalog、README、STATUS 和 CI。
5. 运行全量验证、双语一致性检查和公开安全检查。

## 9. 给各助手的任务提示词

### Core agent

```text
你负责 Agent Context Sync 的确定性脚本和测试。
分支：feat/context-sync-core
Worktree：../agentarium-context-core
允许修改：两个 locale 的 scripts/sync_agent_context.py、tests/test_sync_agent_context.py。
禁止修改：catalog、根 README、package README/STATUS、SKILL.md 和 examples。
目标：实现 check/diff/sync、managed block、仓库路径约束、原有内容保护及 LF/CRLF 行为。
验收：运行聚焦 unittest；确认两个脚本副本字节一致。
不要回滚他人改动，不要扩大文件范围。
```

### zh agent

```text
你负责 Agent Context Sync 中文包和中文公开安全示例。
分支：feat/context-sync-zh
Worktree：../agentarium-context-zh
允许修改：skills/shared/agent-context-sync/zh_CN/ 和 examples/shared/agent-context-sync/zh_CN/。
禁止修改：英文包、脚本、测试、catalog 和根 README。
必须遵守已经锁定的 CLI 契约，不要发明不同的默认行为。
完成后说明触发条件、输入、输出、风险边界和验证结果。
```

### en agent

```text
You own the Agent Context Sync English package and public-safe English examples.
Branch: feat/context-sync-en
Worktree: ../agentarium-context-en
Allowed: skills/shared/agent-context-sync/en_US/ and examples/shared/agent-context-sync/en_US/.
Forbidden: Chinese package, scripts, tests, catalog, and root README.
Follow the locked CLI contract and keep behavior aligned with zh_CN.
Finish with scope, validation, risks, and follow-ups. Do not revert others' work.
```

### Integrator

```text
你负责 integration/context-sync。
允许修改：package README/STATUS、catalog/skills.yaml、根 README、CI 和必要的集成记录。
先保留并提交当前 SKL-0003 发布改动，再按 core、zh、en 顺序集成。
确认两个 locale 脚本字节一致，运行全仓 strict validator、全部 unittest 和行尾检查。
不要 force push，不要修改无关 Skill。
```

## 10. 需要人工确认的问题

- 当前维护者是否希望真正创建多个 worktree，还是按同一计划在单一工作区串行实施？
- 目标仓库的公共规则源默认名称是否采用 `.agent-context/shared.md`？
- 缺失目标文件时，`sync` 是否允许创建文件？本计划建议允许，但只写 managed block。

## 试跑边界

- 本次验证的是规划输出，没有实际创建 worktree 或分支。
- 后续实施受当前执行约束影响，在单一工作区串行完成，但仍沿用本计划的文件所有权和集成顺序。
