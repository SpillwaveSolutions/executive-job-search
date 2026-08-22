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

<!-- worklog:policy:start -->
## WikiTicket SDD (worklog)

This plugin tracks implementation with [WikiTicket SDD](https://github.com/SpillwaveSolutions/wiki_ticket_sdd).

- Install the `worklog` plugin from `SpillwaveSolutions/wiki_ticket_sdd` (Claude Code, Grok Build, Codex, Cursor).
- Config lives in `.work/config.yml`. Event log is `.work/todo.jsonl`.
- Every plan MUST end by running `worklog plan-capture`.
- Work discovered mid-flight: `worklog add --unplanned --discovered-during <item>` BEFORE doing the work.
- Never hand-edit `.work/*.jsonl` (use `worklog`) or `docs/roadmap.md` (generated).
- After changing work items, run `worklog roadmap-render` and commit the log and roadmap together.
- CLI: `worklog` on PATH, or `python3 <wiki_ticket_sdd>/bin/worklog`.
<!-- worklog:policy:end -->

