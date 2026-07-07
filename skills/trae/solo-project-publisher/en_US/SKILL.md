---
name: solo-project-publisher
description: Use when a developer wants to turn a local repository task, project workflow, contest entry, release, or technical case into an evidence-backed community post or project report. This Skill guides scope definition, repository inspection, evidence collection, public-safety review, and forum-ready drafting.
---

# SOLO Project Publisher

Use this Skill to help developers publish real project workflows as credible community posts or project reports.

The output must be grounded in evidence such as files, commands, screenshots, diffs, or generated artifacts. Do not invent promotional claims that are not backed by visible evidence.

## Good Fit

- A feature, tool, script, or project phase is complete and needs a community post.
- A contest or event submission needs a clear creation process, usage steps, and result display.
- Local repository evidence needs to become a project report, release note, or technical case.
- A public-safety check is needed before publishing.

## Not A Fit

- The user only wants a marketing article without project evidence.
- The user asks you to invent screenshots, test results, user feedback, or source links.
- The material mainly contains personal information, private data, customer data, or internal incident details without a clear redaction boundary.
- The user asks you to read or expose credentials, keys, cookies, tokens, private keys, or auth files.

## Recommended Input

Ask for or infer these fields:

```text
Target directory: <project directory or repository path>
Publishing channel: <forum, community, release, internal report, etc.>
Public boundary: <what can be public, what must stay private>
Demo goal: <what the reader should understand after reading>
Existing evidence: <screenshots, commands, files, links, generated artifacts>
```

If the input is incomplete, infer from the current directory, repository state, and local documentation. Ask only when the public boundary or publishing goal is unclear.

## Workflow

1. Scope
   - Identify the target project, repository, or directory.
   - Identify the target audience and publishing channel.
   - Ask only if the public boundary is unclear; otherwise infer conservatively.
   - Record what must not be exposed.

2. Inspect
   - Read the most relevant local docs and changed files first.
   - Check repository state if available.
   - Look for commands, scripts, generated artifacts, screenshots, and validation outputs.
   - Avoid reading or quoting tokens, auth files, private keys, or credential backups.

3. Package Evidence
   - Summarize the real scenario in one short paragraph.
   - Extract the process as concrete steps.
   - Collect evidence for each important claim.
   - Separate completed results from planned follow-ups.

4. Draft
   - Use the target channel's required structure.
   - For the TRAE SOLO Skill contest, include:
     - Skill introduction
     - Use scenario
     - Creation process
     - Usage steps
     - Result display
     - Skill link
     - Summary and reflection
   - Use English by default.
   - Use concise Chinese only when the target channel is a Chinese community post, such as the TRAE SOLO Skill contest.

5. Pre-Publish Review
   - Check for keys, private hostnames, private repository links, personal names, accounts, emails, avatars, tokens, or unnecessary local absolute paths.
   - Check whether each key claim has evidence.
   - Mark missing screenshots, public links, or marketplace links.
   - Provide a short next-step checklist.

## Evidence Requirements

Each output should try to include at least three evidence types:

- Process evidence: steps, prompt snippets, creation screenshots, or conversation summary.
- Result evidence: generated files, Skill package path, output draft, command results, or directory changes.
- Credibility evidence: public links, verification commands, before/after comparison, or manual review notes.

If evidence is missing, do not invent it. Mark it clearly as `[TODO]`.

## Public-Safety Rules

- Do not read `auth.json`, `.env`, private keys, tokens, cookies, or password files.
- Do not expose internal hostnames, private repository URLs, customer names, personal names, real accounts, emails, avatars, user labels, or machine fingerprints.
- For public output, use relative paths or redacted placeholders by default. Keep local absolute paths only for non-public internal reports with a clear reason.
- For public community output, always include a pre-publish safety check.

## Output Shape

For a default English community post, output:

```markdown
# <Skill Name>: <One-Line Result>

## Skill Introduction

## Use Scenario

## Creation Process

## Usage Steps

## Results

## Skill Link

## Summary And Reflection
```

For the TRAE Chinese community contest, use the Chinese 7-section structure in `references/post-template.md`.

For an internal report, adapt to:

```markdown
# Project Case

## Background

## What Changed

## Evidence

## Validation

## Risks

## Next Steps
```

## References

- For the reusable post skeleton, read `references/post-template.md`.
- For evidence and public-safety checks, read `references/evidence-checklist.md`.

## Minimal Trial Output

For the first trial, output at least:

- One contest post draft using the 7-section structure.
- A missing-materials list.
- A pre-publish safety checklist.
- A list of suggested Skill improvements.
