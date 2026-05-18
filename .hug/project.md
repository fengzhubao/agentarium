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

Use `workspace_path` with any selected `roots` entry to reconstruct a local
checkout path. `roots` is intentionally a list so one platform can carry several
candidate workspace roots.

- workspace_path: `fengzhubao/agentarium`
- root_selection: choose the profile matching the current OS/runtime, then use
  an existing root from `roots`; prefer the current working tree when multiple
  roots match.
- profiles:
  - id: wsl-debian-13
    os: linux
    runtime: wsl2
    distro: debian-13
    roots:
      - `~/workspace/lup`
  - id: windows
    os: windows
    runtime: native
    path_style: msys
    roots:
      - `/d/Projects/LuppiterProjects`

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
- Add new machine roots under `Workspace Profiles` as `roots` list entries;
  keep them user-neutral.
- `.hug/project.md` is intended to be committed.
- `.hug/local/` is private local state and must stay ignored.
