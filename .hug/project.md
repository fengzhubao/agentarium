# Hug Project

This file lets `hug_scripts` understand this repository without becoming the
source of truth for the repository itself. Project-owned documents remain
authoritative; this file only points to them and defines scan boundaries.

## Repo

- name: agentarium
- status: active
- updated: 2026-05-18
- vcs: git
- default_branch: main

## Workspace Profiles

The fenced YAML block is the machine-readable source for local checkout
resolution. Keep paths user-neutral.

```yaml
workspace:
  schema: "hug.workspace.v1"
  workspace_paths:
    - "fengzhubao/agentarium"
  root_selection:
    - "Match the profile to the current OS/runtime."
    - "Use an existing root from roots."
    - "Prefer the current worktree when multiple roots match."
  profiles:
    - id: "wsl-debian"
      os: "linux"
      runtime: "wsl2"
      distro: "debian"
      observed_versions:
        - "13"
      roots:
        - path: "~/workspace/lup"
          style: "posix"
    - id: "windows"
      os: "windows"
      runtime: "native"
      roots:
        - path: "/d/Projects/LuppiterProjects"
          style: "msys"
        - path: "D:/Projects/LuppiterProjects"
          style: "win32"
```

## Source Of Truth

- repository_overview: README.md
- solo_project_publisher_status: skills/trae/solo-project-publisher/STATUS.md
- worktree_conductor_status: skills/trae/worktree-conductor/STATUS.md

## Subprojects

| path | name | status source |
| --- | --- | --- |
| skills/trae/solo-project-publisher | SOLO Project Publisher | skills/trae/solo-project-publisher/STATUS.md |
| skills/trae/worktree-conductor | Worktree Conductor | skills/trae/worktree-conductor/STATUS.md |
| skills/codex | Codex skills | README.md |
| skills/claude | Claude skills | README.md |
| examples/trae | TRAE examples | README.md |
| examples/codex | Codex examples | README.md |
| examples/claude | Claude examples | README.md |
| docs | Repository docs | README.md |

## Entrypoints

- repository_overview: `README.md`
- solo_project_publisher_status: `skills/trae/solo-project-publisher/STATUS.md`
- worktree_conductor_status: `skills/trae/worktree-conductor/STATUS.md`

## Hug Scan

- include:
  - README.md
  - .hug/project.md
  - skills/
  - examples/
  - docs/
- exclude:
  - .hug/local/
  - .git/
  - dist/
  - build/
  - __pycache__/
  - .pytest_cache/

## Maintenance

Update this file when canonical document paths, important subprojects,
entrypoints, or scan boundaries change.

Do not update this file for ordinary bug fixes, small copy edits, or internal
implementation details that do not affect repository navigation.

## Local Rules

- Use `<workspace-root>/...` for shared local paths unless a
  profile-specific example is required.
- Do not record concrete user-home paths such as `/home/<user>/...` or
  `C:/Users/<user>/...`.
- Add new machine roots under `workspace.profiles[].roots`; keep them
  user-neutral.
- `.hug/project.md` is intended to be committed.
- `.hug/local/` is private local state and must stay ignored.
