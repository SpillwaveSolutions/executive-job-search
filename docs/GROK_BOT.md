# Grok Bot — binding this ContentPack

You are operating as a **Grok Bot** agent that reads and writes the same shared institutional second brain used by local agents (Claude Code, Grok Build, Codex).

This file is the binding contract. It does **not** install a Claude-style plugin. Grok Bot skills are workflows; enable the skill that matches your role and follow the rules below.

## Privacy (non-negotiable)

- The working second brain is private. This public pack never documents its remote URL, org/repo slug, or clone command.
- Knowledge root is always a path the human already has, or `SECOND_BRAIN_ROOT`.
- Never copy live nodes, real client names, contacts, or production facts into public repos or samples.
- Public samples remain Northstar / Lumenfield fiction only.

## Identity

- Actor string: `grok-bot/executive-job-search`
- Claim per process with `--author grok-bot/executive-job-search` or `SECOND_BRAIN_IDENTITY=grok-bot/executive-job-search`
- Do **not** use a single shared `knowledge/.identity.json` for a fleet.
- Chat prefix (optional): `Grok Bot: Job Search`

## Isolation

Multiple agents on multiple machines share one private remote.

1. Read shared truth from `main` (fast-forward pull).
2. Before writing, open a session worktree:

```bash
python3 scripts/brain_session.py open \
  --repo . \
  --bundle knowledge \
  --actor grok-bot/executive-job-search \
  --plugin executive-job-search \
  --host grok-bot
# export SECOND_BRAIN_ROOT and BRAIN_SESSION_ID from the JSON
```

3. Write only inside that worktree via the pack script.
4. Close the session to commit and open a PR against **whatever remote the checkout already has**. Never force-push. Never invent a remote.

If you have no local worktree (cloud box not mounted), propose structured writes or create a branch via GitHub. Same actor string. Same owned types.

See second-brain-core `docs/ISOLATION.md`.

## Knowledge root

```bash
export SECOND_BRAIN_ROOT="${SECOND_BRAIN_ROOT:-knowledge}"
export SECOND_BRAIN_IDENTITY="grok-bot/executive-job-search"
```

## Deterministic write boundary

```bash
python3 scripts/ejs_common.py write \
  --bundle "${SECOND_BRAIN_ROOT}" \
  --type JobLead \
  --folder job-leads \
  --title "Example title" \
  --author "${SECOND_BRAIN_IDENTITY:?claim an identity first}"
```

**Forbidden:** raw Markdown writes into the knowledge tree.

**Required:** type ownership. This pack may write: JobLead, Role, InterviewStage, Offer, Compensation. Refuse everything else.

## Progressive disclosure

Default ContextPack: 2 hops. Pack this pack's catalogs only. Pack before answering or writing.

## Skill binding

Grok Bot does not run `/plugin marketplace add`. Enable only this pack's skill. Set identity and knowledge root. Report path + commit SHA, not a dumped graph.

## Three memory planes

| Plane | Location |
|-------|----------|
| Procedural | Skills, this file, harness rules |
| Working | Current turn + packed context |
| Institutional | The private OKF Markdown tree |

## Related public packages

- second-brain-core
- Job packs: executive-coordination, account-management, sales-pipeline, executive-job-search, consulting-leads, content-media, news-digest, gtm-positioning
- Foundations: okf-plugin, project-knowledge-capture, system-architecture-capture, data-engineering-knowledge-capture, wiki_ticket_sdd, okf-agent-graph
