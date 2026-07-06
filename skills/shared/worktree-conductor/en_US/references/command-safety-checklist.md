# Command Safety Checklist

Use this checklist before recommending or running any Git/worktree command.

## Preflight Checks

- Check the current branch with `git branch --show-current`.
- Check the worktree state with `git status --short`.
- List existing worktrees with `git worktree list`.
- Check whether planned branches already exist with `git branch --list <branch>`.
- Confirm each target worktree path does not already exist.
- Confirm the base branch is correct and current enough for planning.

## Command Rules

- Do not run Git commands by default; output commands as a plan unless the user explicitly asks you to execute them.
- Prefer `git pull --ff-only` over a merge-producing `git pull`.
- Do not recommend `git reset --hard`, `git clean -fd`, force push, or destructive cleanup unless the user explicitly asks for that operation and the risk is stated.
- If the repository is dirty, ask the user or assign an owner before creating worktrees.
- If generated outputs or lockfiles must change, assign one integration owner.

## Public Output

- Replace private repository names, customer names, machine paths, and account identifiers with examples.
- Use example worktree paths such as `../repo-runtime`, not real local absolute paths.
