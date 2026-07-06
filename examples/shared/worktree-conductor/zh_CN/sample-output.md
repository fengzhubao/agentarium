# Worktree Conductor 示例输出

说明：这是脱敏示例，用于展示 Skill 的目标输出形态。真实试跑当前已实现包后，应保存目标工具的实际输出和公开安全证据。

````markdown
# Worktree Conductor Plan

## 1. 并行可行性判断

结论：适合并行，但需要先做一轮共享基础确认。

原因：

- `runtime/`、`generator/`、`examples/`、`docs/` 可以拆成相对独立任务。
- `definition/*.yaml`、`schema/`、`generated/` 和 `package-lock.json` 是共享高风险区域，不能让多个助手同时修改。
- 如果 DSL 契约需要调整，应先放入 `feat/shared-foundation`，再让其他任务从这个基础分支切出。

建议并行度：3 个实现任务 + 1 个文档/示例任务。

## 2. 推荐分支 / worktree 拆分

| 任务 | 分支 | Worktree 路径 | 负责人/助手 | 目标 |
| --- | --- | --- | --- | --- |
| 共享基础 | `feat/shared-foundation` | `../metanc-hmi-foundation` | Integrator | 确认 DSL 契约、Schema 和生成边界 |
| 运行时解析 | `feat/runtime-parser` | `../metanc-hmi-runtime` | Codex | 实现 runtime 解析逻辑 |
| UI 组件生成 | `feat/ui-generator` | `../metanc-hmi-generator` | TRAE | 实现组件生成逻辑 |
| 示例工程 | `feat/examples` | `../metanc-hmi-examples` | Claude | 补示例工程和演示输入 |
| 文档 | `feat/docs` | `../metanc-hmi-docs` | TRAE 或人工 | 编写使用指南和集成说明 |

## 3. 文件归属与禁止触碰范围

| 任务 | 允许修改 | 禁止触碰 | 依赖 |
| --- | --- | --- | --- |
| 共享基础 | `definition/*.yaml`, `schema/` | 业务实现目录 | 无 |
| 运行时解析 | `runtime/`, `tests/runtime/` | `definition/*.yaml`, `schema/`, `generated/` | `feat/shared-foundation` |
| UI 组件生成 | `generator/`, `tests/generator/` | `definition/*.yaml`, `schema/`, `package-lock.json` | `feat/shared-foundation` |
| 示例工程 | `examples/` | `definition/*.yaml`, `schema/`, `generated/` | runtime 和 generator 稳定后 |
| 文档 | `docs/` | 代码实现目录、锁文件 | 其他分支输出 |

## 4. 共享文件风险表

| 文件/区域 | 风险 | 原因 | 策略 |
| --- | --- | --- | --- |
| `definition/*.yaml` | 高 | DSL 契约影响所有模块 | 只允许 shared foundation 修改 |
| `schema/` | 高 | 下游 runtime 和 generator 都依赖 | 只允许 shared foundation 修改 |
| `generated/` | 高 | 生成物容易被多个分支覆盖 | 集成分支统一生成 |
| `package-lock.json` | 高 | 并行修改很容易冲突 | 除非必要，不在子任务里修改 |
| `docs/` | 中 | 多个任务都会引用 | 文档任务 owner 统一整理 |
| `examples/` | 中 | 依赖 runtime 和 generator 输出 | 放在后半段集成 |

## 5. 命令安全预检查

```bash
git branch --show-current
git status --short
git worktree list
git branch --list feat/shared-foundation
git branch --list feat/runtime-parser
git branch --list feat/ui-generator
git branch --list feat/examples
git branch --list feat/docs
git branch --list integration/round-1
```

运行 `git worktree add` 前，确认目标路径尚不存在：

```text
../metanc-hmi-foundation
../metanc-hmi-runtime
../metanc-hmi-generator
../metanc-hmi-examples
../metanc-hmi-docs
../metanc-hmi-integration
```

不要使用 `git reset --hard`、`git clean -fd`、force push 等破坏性命令，除非用户明确要求并接受风险。

## 6. 推荐命令

```bash
git fetch origin
git switch main
git pull --ff-only
git switch -c feat/shared-foundation
git worktree add ../metanc-hmi-runtime -b feat/runtime-parser
git worktree add ../metanc-hmi-generator -b feat/ui-generator
git worktree add ../metanc-hmi-examples -b feat/examples
git worktree add ../metanc-hmi-docs -b feat/docs
git worktree add ../metanc-hmi-integration -b integration/round-1
```

命令里的路径和分支名需要按真实仓库调整。

## 7. 分支验收清单

| 分支 | 必跑检查 | 通过标准 |
| --- | --- | --- |
| `feat/shared-foundation` | `npm run lint`, `npm test` | Schema 和契约变更不破坏已有测试 |
| `feat/runtime-parser` | `npm test -- runtime` | runtime 测试通过 |
| `feat/ui-generator` | `npm test -- generator`, `npm run build` | 生成器测试和构建通过 |
| `feat/examples` | `npm run build` | 示例能引用当前 DSL 结构 |
| `feat/docs` | 文档链接检查或人工阅读 | 步骤能被新用户复现 |
| `integration/round-1` | `npm run lint`, `npm test`, `npm run build` | 全量通过 |

## 8. 集成顺序

1. 先合并 `feat/shared-foundation`。
2. 合并 `feat/runtime-parser`。
3. 合并 `feat/ui-generator`。
4. 合并 `feat/examples`。
5. 合并 `feat/docs`。
6. 在 `integration/round-1` 上统一更新生成物并跑全量验证。

## 9. 给各助手的任务提示词

### Integrator：共享基础

```text
你负责共享 DSL 基础，不是独占整个仓库；其他助手会在这个基础稳定后进入不同 worktree 并行开发。

仓库：metanc_hmi_dsl
分支：feat/shared-foundation
Worktree：../metanc-hmi-foundation
目标：确认 DSL 契约、Schema 边界，以及 generator/runtime 的共同假设。

允许修改：
- definition/*.yaml
- schema/
- docs/architecture/

禁止修改：
- runtime/
- generator/
- generated/
- package-lock.json

共享依赖：
- 后续 runtime parser、UI generator、examples 和 docs 任务都依赖这个分支。

验收命令：
- npm run lint
- npm test

工作要求：
- 只在允许范围内修改文件。
- 不要回滚他人改动。
- 如果发现必须修改生成物或锁文件，先停止并说明原因。
- 完成后给出改动摘要、验证结果、风险和后续建议。
```

### Codex：运行时解析

```text
你负责运行时 DSL 解析，不是独占整个仓库；其他助手正在不同 worktree 中并行开发。

仓库：metanc_hmi_dsl
分支：feat/runtime-parser
Worktree：../metanc-hmi-runtime
目标：基于共享 DSL 契约实现 runtime 解析逻辑。

允许修改：
- runtime/
- tests/runtime/

禁止修改：
- definition/*.yaml
- schema/
- generated/
- package-lock.json

共享依赖：
- feat/shared-foundation

验收命令：
- npm test -- runtime
- npm run lint

完成后说明改动、验证结果、风险和后续事项。不要回滚他人改动，不要扩大文件范围。
```

### TRAE：UI 组件生成

```text
你负责 UI 组件生成，不是独占整个仓库；其他助手正在不同 worktree 中并行开发。

仓库：metanc_hmi_dsl
分支：feat/ui-generator
Worktree：../metanc-hmi-generator
目标：基于共享 DSL 契约实现组件生成逻辑。

允许修改：
- generator/
- tests/generator/

禁止修改：
- definition/*.yaml
- schema/
- generated/
- package-lock.json

共享依赖：
- feat/shared-foundation

验收命令：
- npm test -- generator
- npm run build
- npm run lint

工作要求：
- 只在允许范围内修改文件。
- 除非集成负责人明确分配，不要在本分支更新生成物。
- 完成后给出改动摘要、验证结果、风险和后续建议。
```

### Claude：示例工程

```text
你负责示例工程和演示输入，不是独占整个仓库；其他助手正在不同 worktree 中并行开发。

仓库：metanc_hmi_dsl
分支：feat/examples
Worktree：../metanc-hmi-examples
目标：添加示例工程，展示稳定的 runtime 和 generator 行为。

允许修改：
- examples/
- tests/examples/

禁止修改：
- definition/*.yaml
- schema/
- runtime/
- generator/
- generated/
- package-lock.json

共享依赖：
- feat/runtime-parser
- feat/ui-generator

验收命令：
- npm run build
- npm test

工作要求：
- 只在允许范围内修改文件。
- 如果示例需要契约或生成器改动，先停止并说明依赖需求。
- 完成后给出改动摘要、验证结果、风险和后续建议。
```

### TRAE 或人工：文档

```text
你负责使用和集成文档，不是独占整个仓库；其他助手正在不同 worktree 中并行开发。

仓库：metanc_hmi_dsl
分支：feat/docs
Worktree：../metanc-hmi-docs
目标：编写 DSL、runtime parser、generator、examples 和集成流程说明。

允许修改：
- docs/
- README.md

禁止修改：
- runtime/
- generator/
- definition/*.yaml
- schema/
- generated/
- package-lock.json

共享依赖：
- feat/runtime-parser、feat/ui-generator、feat/examples 的总结

验收命令：
- 文档链接检查或人工阅读
- npm run build

工作要求：
- 只在允许范围内修改文件。
- 不要改写实现代码。
- 完成后给出改动摘要、验证结果、风险和后续建议。
```

### Integrator：集成分支

```text
你负责 integration/round-1，等待功能分支准备好后再开始。

仓库：metanc_hmi_dsl
分支：integration/round-1
Worktree：../metanc-hmi-integration
目标：按计划顺序合并已验收分支，必要时统一更新生成物，处理冲突，并运行全量验证。

允许修改：
- generated/
- package-lock.json
- 人工维护者指定的集成记录或发布说明

禁止修改：
- 集成范围外的无关功能改动

共享依赖：
- feat/shared-foundation
- feat/runtime-parser
- feat/ui-generator
- feat/examples
- feat/docs

验收命令：
- npm run lint
- npm test
- npm run build

工作要求：
- 按计划顺序合并。
- 不要 force push，不要改写其他人的分支。
- 记录冲突、生成物更新、验证结果和剩余风险。
```

## 10. 需要人工确认的问题

- DSL 契约是否已经稳定，还是必须先做 shared foundation？
- 是否允许任何子任务修改锁文件？
- `generated/` 是否必须提交，还是可以在集成分支统一生成？
````
