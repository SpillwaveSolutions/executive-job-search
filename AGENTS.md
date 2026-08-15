# AGENTS.md — Executive Job Search

This repository is a dual-host agent plugin (Claude Code + Grok Build + Codex).

## Rules

- Read `docs/ONBOARDING.md` before writing. Grok Bot agents start there.
- Write only the noun types listed in README.md.
- Use absolute in-bundle paths for links (`/clients/acme.md`).
- Deterministic writes go through `scripts/ejs_common.py`.
- Do not invent relationship names.
- Do not hard-code real client or company names in samples. Use fictional examples.
- Identity of the writer belongs in `author` frontmatter.

## Layout

- `skills/` — progressive-disclosure skills
- `commands/` — slash-command shims
- `schemas/okf-concepts/` — JSON Schema for each noun
- `templates/` — Markdown templates
- `sample-knowledge/` — fictional demo bundle
- `scripts/ejs_common.py` — init / write / pack / validate
