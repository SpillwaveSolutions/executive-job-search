# CLAUDE.md — Executive Job Search

You are operating the **Executive Job Search** ContentPack plugin.

## When to use

Use this plugin when the user is working on any type listed in README.md / `schemas/okf-concepts/registry.json`. Read `docs/ONBOARDING.md` first.

## Write path

1. Identify the noun type.
2. Check `schemas/okf-concepts/` for required fields.
3. Call `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/ejs_common.py write ...`
4. Link with typed `rel` values from `docs/typed-edges.md`.
5. Offer `/ejs-pack` if the user needs a session-sized subgraph.

## Do not

- Dump the whole knowledge tree into context. Use packs.
- Write types owned by another plugin.
- Publish, send email, or apply to jobs unless the user explicitly confirms.

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

