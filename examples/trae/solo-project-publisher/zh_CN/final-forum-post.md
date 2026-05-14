# 〖Skill 创作〗SOLO Project Publisher：把真实项目过程整理成能发布的社区帖

## 1、Skill简介

SOLO Project Publisher 是我给自己做的一个发布整理 Skill。

它解决的不是“帮我把文字写好看”这种问题，而是更具体的一件事：当我做完一个工具、脚本、项目阶段，或者准备参加一次社区活动时，帮我把真实材料整理成一篇能发出去、能复查、也方便别人讨论的帖子。

它会围绕几个问题展开：

- 这个项目为什么值得写？
- 哪些材料可以公开？
- 哪些结论有文件、截图、命令结果或链接支撑？
- 发帖前还有哪些截图、源码链接、说明需要补？
- 有没有不该公开的配置、账号、Token、路径或内部信息？

所以我更愿意把它理解成一个“项目发布整理流程”，不是一个单纯的写作模板。

## 2、使用场景

这次做它的直接原因，就是准备参加 TRAE SOLO 技能创作赛。

一开始我手里只有几个分散的材料：

- 官方比赛公告和投稿指南
- `solo-skill-contest` 目录下的规划文档
- `solo-project-publisher` 的 Skill 草稿
- 几个参考作品链接
- 后续要放到 GitHub 的公开 Skill 仓库

如果手动整理，最大的问题不是写不出来，而是容易漏：

- 漏掉官方要求的 7 段结构
- 漏掉创作过程
- 漏掉真实截图和源码链接
- 漏掉发布前安全检查
- 写着写着变成泛泛介绍，看不出具体做了什么

所以我把这个过程做成一个 Skill，让它先把材料和结构拉齐，再由我做最后判断和修改。

除了比赛投稿，它也适合这些场景：

- 做完一个小工具后，整理一篇介绍帖
- 完成一个版本更新后，整理 Release 说明
- 做完一次工程改造后，整理复盘
- 想把一次技术尝试写成社区分享

## 3、创作过程

我先看了比赛公告和投稿指南，确认帖子至少要讲清楚这些内容：

- Skill 简介
- 使用场景
- 创作过程
- 使用步骤
- 效果展示
- Skill 链接
- 总结与思考

然后我把 Skill 设计成五个步骤：

1. 界定范围：先确认目标目录、发帖渠道、读者和公开边界。
2. 检查材料：读取规划文档、Skill 草稿、参考链接和已有输出。
3. 整理证据：把截图、文件、链接、生成物和结论对应起来。
4. 起草帖子：按目标社区的结构生成草稿。
5. 发布前复查：检查敏感信息和缺口材料。

中间我还调整了公开仓库结构。最开始只是本地草稿，后来单独建了一个 GitHub 仓库：

```text
https://github.com/fengzhubao/agentarium
```

仓库里按工具和语言版本组织：

```text
skills/
  trae/
    solo-project-publisher/
      zh_CN/
      en_US/
```

这样后续不只可以放 TRAE 的 Skill，也可以继续放 Claude、Codex 或其他工具的版本；每个 Skill 也至少保留中文和英文两个版本。

## 4、使用步骤

我这次在 Windows 上用 TRAE SOLO 试跑，导入的是中文版本：

```text
skills/trae/solo-project-publisher/zh_CN
```

试跑时输入的大意是：

```text
请使用 SOLO Project Publisher，把 solo-skill-contest 目录下的比赛准备工作整理成一篇 SOLO 技能创作赛参赛帖。

发布分类：https://forum.trae.cn/c/37-category/37
标签：Skill创作

公开边界：
- 可以公开规划文档和 Skill 草稿。
- 不要读取或泄露敏感配置。
- 不要输出 auth.json、Token、私钥、账号、内部主机名。

输出要求：
- 使用官方 7 段结构。
- 标记缺少的截图、Skill 链接、源码链接。
- 最后给出发布前安全检查。
```

TRAE SOLO 实际执行时做了这些事：

- 识别并加载了 `solo-project-publisher` 技能。
- 读取了 `SKILL.md`、`post-template.md`、`evidence-checklist.md` 和部分规划文档。
- 按官方 7 段结构生成了 `forum-post-draft.md`。
- 在流程里执行了发布前安全检查。
- 标记了还需要补充的截图和链接。

试跑过程中有两个文件创建失败提示，但核心草稿生成成功了。这个问题后续我会继续看是路径、权限还是 TRAE 写文件策略导致的。

## 5、效果展示

这次试跑留下了几张截图，可以作为证据：

- `01-skill-import.png`：TRAE SOLO 已识别并加载 `solo-project-publisher`。
- `02-generation-process.png`：技能被调用，并按步骤检查目录、读取材料、整理证据。
- `03-generated-draft.png`：生成了 7 段式论坛草稿。
- `04-safety-check.png`：读取了安全检查相关材料，并执行发布前检查。
- `05-directory-structure.png`：Skill 已按 `zh_CN` / `en_US` 双语版本组织。

试跑前：

- 只有本地规划文档、Skill 草稿和参考帖子记录。
- 发布材料分散在不同文件里。
- 还没有外部可访问的 Skill 链接。

试跑后：

- 生成了参赛帖草稿。
- GitHub 仓库已经整理出可公开的 Skill 包。
- 截图和试跑输出已经放入示例目录。
- 发布前安全边界更清楚了。

当前公开仓库结构：

```text
agentarium/
  skills/
    trae/
      solo-project-publisher/
        zh_CN/
        en_US/
  examples/
    trae/
      solo-project-publisher/
        zh_CN/
        en_US/
```

## 6、Skill 链接

Skill 源码：

https://github.com/fengzhubao/agentarium/tree/main/skills/trae/solo-project-publisher

中文版本：

https://github.com/fengzhubao/agentarium/tree/main/skills/trae/solo-project-publisher/zh_CN

英文版本：

https://github.com/fengzhubao/agentarium/tree/main/skills/trae/solo-project-publisher/en_US

示例和截图：

https://github.com/fengzhubao/agentarium/tree/main/examples/trae/solo-project-publisher/zh_CN

Skill 市场链接：暂时没有，后续如果官方支持上传，我再补。

## 7、总结与思考

这次试下来，我觉得这个 Skill 的价值主要在三个地方。

第一，它能把“发帖”这件事变成一个稳定流程。不是上来就写正文，而是先确认范围、材料、证据和公开边界。

第二，它能提醒我补证据。比如截图、源码链接、使用前后对比，这些如果不提前列出来，最后很容易漏。

第三，它能把安全检查放到发布前。对我这种本地目录里有配置备份、脚本和各种实验材料的人来说，这一步很重要。

目前还不完美。比如这次试跑里出现了文件创建失败提示，生成的第一版草稿也还需要人工调整，不可能直接原样发布。但它已经把最耗时间的结构整理和缺口检查做出来了。

后续我想继续补几个方向：

- Release 说明模式
- 工程复盘模式
- Skill 测评帖模式
- 多语言发帖版本
- 更严格的发布前脱敏检查

如果你也经常做完一个东西之后卡在“怎么把过程讲清楚”，这个 Skill 应该会有点用。
