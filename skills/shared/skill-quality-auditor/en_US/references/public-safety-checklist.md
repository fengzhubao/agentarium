# Public-Safety Checklist

Agentarium is a public repository. Audit Skill instructions, references, and examples for information that should not be public.

## Blockers

Mark these as BLOCKER:

- API keys, tokens, cookies, passwords, or private keys.
- `.env` content or authentication file content.
- Private repository URLs.
- Internal hosts, private IP-only services, customer names, or customer data.
- Unredacted screenshot descriptions.
- Personal names, accounts, email addresses, phone numbers, avatars, user labels, machine names, or absolute paths unless they are clear placeholders.

## High-Risk Items

Usually mark these as HIGH:

- Large raw logs with environment details.
- Real project paths or organization names.
- Identifiable business data.
- Claims of public publication without a public link or placeholder note.

## Recommended Patterns

- Use placeholders such as `<redacted>`, `<public-repo-url>`, and `<project-root>`.
- Prefer relative paths in examples.
- Use screenshot placeholders until redaction has been reviewed.
- Do not treat local machine state, user directories, or command history as public evidence.
