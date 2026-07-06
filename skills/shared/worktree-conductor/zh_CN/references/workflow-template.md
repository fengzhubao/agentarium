# Worktree Conductor 输出模板

````markdown
# Worktree Conductor Plan

## 1. 并行可行性判断

- 结论：适合并行 / 需要先做共享基础 / 不建议并行。
- 原因：
  - <原因 1>
  - <原因 2>
- 建议并行度：<数量>

## 2. 推荐分支 / worktree 拆分

| 任务 | 分支 | Worktree 路径 | 负责人/助手 | 目标 |
| --- | --- | --- | --- | --- |
| 共享基础 | `feat/shared-foundation` | `../repo-foundation` | <owner> | <目标> |
| 子任务 A | `feat/<name-a>` | `../repo-<name-a>` | <owner> | <目标> |

## 3. 文件归属与禁止触碰范围

| 任务 | 允许修改 | 禁止触碰 | 依赖 |
| --- | --- | --- | --- |
| <任务> | `<path>` | `<path>` | <依赖> |

## 4. 共享文件风险表

| 文件/区域 | 风险 | 原因 | 策略 |
| --- | --- | --- | --- |
| `<path>` | 高/中/低 | <原因> | <策略> |

## 5. 命令安全预检查

```bash
git branch --show-current
git status --short
git worktree list
git branch --list feat/<task>
```

运行 `git worktree add` 前，确认目标 worktree 路径尚不存在。
不要使用 `git reset --hard`、`git clean -fd`、force push 或破坏性清理，除非用户明确要求该操作。

## 6. 推荐命令

```bash
git fetch origin
git switch <base-branch>
git pull --ff-only
git worktree add ../repo-<task> -b feat/<task>
```

注意：命令需要按实际仓库、分支和本地路径调整。

## 7. 分支验收清单

| 分支 | 必跑检查 | 通过标准 |
| --- | --- | --- |
| `feat/<task>` | `<command>` | <标准> |

## 8. 集成顺序

1. 合并 `feat/shared-foundation`。
2. 合并底层模块。
3. 合并依赖底层模块的功能。
4. 合并示例和文档。
5. 在 `integration/round-1` 上跑全量验证。

## 9. 给各助手的任务提示词

### 助手 A

```text
你负责 <任务>。
分支：<branch>
Worktree：<path>
允许修改：<paths>
禁止修改：<paths>
依赖：<dependencies>
验收命令：<commands>
输出要求：说明改动、验证结果、风险和后续事项。
不要回滚他人改动，不要扩大文件范围。
```

## 10. 需要人工确认的问题

- <问题 1>
- <问题 2>
````
