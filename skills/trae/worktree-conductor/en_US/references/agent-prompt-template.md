# Agent Task Prompt Template

Copy this template for each agent and replace the angle-bracket placeholders.

```text
You are responsible for <task name>. You are not alone in this repository; other agents are working in separate worktrees.

Repository: <repo>
Branch: <branch>
Worktree: <worktree-path>
Goal: <goal>

Allowed paths:
- <path 1>
- <path 2>

Forbidden paths:
- <path 1>
- <path 2>

Shared dependencies:
- <dependency 1>

Validation commands:
- <command 1>
- <command 2>

Requirements:
- Only modify files in the allowed scope.
- Do not revert changes made by others.
- If you discover that a shared file must change, stop and explain why first.
- Finish with a change summary, validation results, risks, and follow-ups.
```

