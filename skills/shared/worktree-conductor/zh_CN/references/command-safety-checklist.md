# 命令安全检查清单

在推荐或执行任何 Git/worktree 命令前使用这份清单。

## 预检查

- 用 `git branch --show-current` 检查当前分支。
- 用 `git status --short` 检查工作区状态。
- 用 `git worktree list` 查看已有 worktree。
- 用 `git branch --list <branch>` 检查计划分支是否已存在。
- 确认每个目标 worktree 路径尚不存在。
- 确认基线分支正确，并且足够新。

## 命令规则

- 默认不要执行 Git 命令；除非用户明确要求执行，否则只把命令作为计划输出。
- 优先使用 `git pull --ff-only`，避免产生隐式 merge commit。
- 不要推荐 `git reset --hard`、`git clean -fd`、force push 或破坏性清理，除非用户明确要求并且风险已说明。
- 如果工作区不干净，先让用户确认或指定 owner，再创建 worktree。
- 如果必须更新生成物或锁文件，指定唯一集成负责人。

## 公开输出

- 将私有仓库名、客户名、机器路径和账号标识替换为示例值。
- 使用 `../repo-runtime` 这类示例 worktree 路径，不要输出真实本地绝对路径。
