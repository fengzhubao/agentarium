# Worktree Conductor 示例输出

说明：这是脱敏示例，用于展示 Skill 的目标输出形态。真实试跑后应保存 TRAE SOLO 的实际输出和截图。

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

## 5. 推荐命令

```bash
git fetch origin
git switch main
git pull
git switch -c feat/shared-foundation
git worktree add ../metanc-hmi-runtime -b feat/runtime-parser
git worktree add ../metanc-hmi-generator -b feat/ui-generator
git worktree add ../metanc-hmi-examples -b feat/examples
git worktree add ../metanc-hmi-docs -b feat/docs
git worktree add ../metanc-hmi-integration -b integration/round-1
```

命令里的路径和分支名需要按真实仓库调整。

## 6. 分支验收清单

| 分支 | 必跑检查 | 通过标准 |
| --- | --- | --- |
| `feat/shared-foundation` | `npm run lint`, `npm test` | Schema 和契约变更不破坏已有测试 |
| `feat/runtime-parser` | `npm test -- runtime` | runtime 测试通过 |
| `feat/ui-generator` | `npm test -- generator`, `npm run build` | 生成器测试和构建通过 |
| `feat/examples` | `npm run build` | 示例能引用当前 DSL 结构 |
| `feat/docs` | 文档链接检查或人工阅读 | 步骤能被新用户复现 |
| `integration/round-1` | `npm run lint`, `npm test`, `npm run build` | 全量通过 |

## 7. 集成顺序

1. 先合并 `feat/shared-foundation`。
2. 合并 `feat/runtime-parser`。
3. 合并 `feat/ui-generator`。
4. 合并 `feat/examples`。
5. 合并 `feat/docs`。
6. 在 `integration/round-1` 上统一更新生成物并跑全量验证。

## 8. 给各助手的任务提示词

### Codex：运行时解析

```text
你负责运行时 DSL 解析，不是独占整个仓库。

分支：feat/runtime-parser
Worktree：../metanc-hmi-runtime
允许修改：
- runtime/
- tests/runtime/

禁止修改：
- definition/*.yaml
- schema/
- generated/
- package-lock.json

验收命令：
- npm test -- runtime
- npm run lint

完成后说明改动、验证结果、风险和后续事项。不要回滚他人改动，不要扩大文件范围。
```

## 9. 需要人工确认的问题

- DSL 契约是否已经稳定，还是必须先做 shared foundation？
- 是否允许任何子任务修改锁文件？
- `generated/` 是否必须提交，还是可以在集成分支统一生成？
````
