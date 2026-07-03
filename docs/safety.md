# Public Safety

This repository is public. Treat every committed file as externally visible.

## Do Not Commit

- `auth.json`
- `.env`
- API keys, tokens, cookies, passwords, private keys
- Internal hostnames or private IP-only service details
- Private repository URLs unless intentionally public
- Customer data, internal incident data, or project secrets
- Large raw logs with machine, account, or environment details
- Unnecessary local absolute paths

For public examples, posts, screenshots, and reports, use relative paths or redacted placeholders by default. Keep absolute local paths only for non-public internal reports when there is a clear reason.

## Allowed Content

- Skill instructions
- Workflow templates
- Public examples
- Redacted sample inputs and outputs
- Public-safe screenshots
- Safety checklists
- Links to public documentation

## Screenshot Rule

Screenshots must be reviewed before commit. Do not publish raw tool screenshots if they show account labels, user avatars, local paths, task names, private project names, repository paths, terminal output, or workspace context that is not meant to be public.

If a screenshot is useful but not yet reviewed, keep a placeholder in the example and add the redacted screenshot later.

## Review Checklist

Before publishing a Skill:

- [ ] The Skill can be understood without private context.
- [ ] Examples are redacted and reproducible enough for readers.
- [ ] No credential or secret-like strings are present.
- [ ] No private repo, host, customer, or account details are present.
- [ ] Public links are accessible to readers.
- [ ] Claims in examples are backed by visible evidence or clearly marked as placeholders.
