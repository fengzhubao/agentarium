# Worktree Conductor 示例输入

请使用 Worktree Conductor，帮我把下面这个开发任务拆成多个可以并行开发的 worktree 计划。

## 仓库

示例仓库：`metanc_hmi_dsl`

目标基线分支：`main`

## 总目标

同时开发一个 HMI DSL 的几个部分：

- 运行时 DSL 解析。
- UI 组件生成。
- 示例工程。
- 文档和使用指南。

## 希望并行方式

希望让 3 到 4 个助手并行工作，可以分别交给 TRAE、Claude、Codex 或不同会话。

## 已知模块和共享区域

- `runtime/`：运行时解析逻辑。
- `generator/`：组件生成逻辑。
- `examples/`：示例工程。
- `docs/`：文档。
- `definition/*.yaml`：共享 DSL 契约，高风险。
- `schema/`：Schema 定义，高风险。
- `generated/`：生成物，不希望多个助手同时改。
- `package-lock.json`：锁文件，不希望多个助手同时改。

## 验证命令

```bash
npm run lint
npm test
npm run build
```

## 输出要求

- 判断是否适合并行。
- 给出分支和 worktree 拆分。
- 给出文件归属和禁止触碰范围。
- 标出共享文件风险。
- 给出推荐命令。
- 给出每个分支的验收清单。
- 给出集成顺序。
- 给出可以复制给不同助手的任务提示词。
