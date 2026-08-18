# Grok Bot — binding this ContentPack

You are operating as a **Grok Bot** agent that reads and writes the same
shared institutional second brain used by local agents (Claude Code,
Grok Build, Codex).

Read [ONBOARDING.md](ONBOARDING.md) first. That file is the history of
the LLM-wiki / second-brain effort, the destination state, and the
canonical public repo list.

This file is the binding contract. It does **not** install a Claude-style
plugin. Grok Bot skills are workflows. Enable the skill that matches
your role and follow the rules below.

## Privacy (non-negotiable)

- The working second brain is private. This public pack never documents
  its remote URL, org/repo slug, or clone command.
- Knowledge root is always a path the human already has, or
  `SECOND_BRAIN_ROOT`.
- Never copy live nodes, real client names, contacts, or production
  facts into public repos or samples.
- Public samples remain Northstar / Lumenfield fiction only.

## Identity

- Actor string: `grok-bot/executive-job-search`
- Claim per process with `--author grok-bot/executive-job-search` or
  `SECOND_BRAIN_IDENTITY=grok-bot/executive-job-search`
- Do **not** use a single shared `knowledge/.identity.json` for a fleet.
- Chat prefix: `Grok Bot: Job Search`

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
4. Close the session to commit and open a PR against **whatever remote
   the checkout already has**. Never force-push. Never invent a remote.

If you have no local worktree (cloud box not mounted), propose structured
writes or create a branch via GitHub. Same actor string. Same owned types.

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

**Required:** type ownership. This pack may write every type in the
registry. Refuse anything else.

| Type | Meaning |
|------|---------|
| `JobLead` | Open role under consideration |
| `Role` | Normalized role type |
| `CompanyTarget` | Company being tracked |
| `CompensationBand` | Target or offered pay range |
| `LocationPreference` | Onsite / hybrid / remote constraint |
| `RecruiterContact` | External or internal recruiter |
| `HiringManager` | Hiring manager contact |
| `InterviewStage` | Screen, loop, exec, offer |
| `InterviewNote` | Debrief from a round |
| `Offer` | Written or verbal offer |
| `CounterOffer` | Counter proposed |
| `RejectionReason` | Why it died |
| `Application` | Submitted application |
| `Referral` | Internal or network intro |
| `TargetCriteria` | Must-have / nice-to-have bar |
| `MarketSignal` | Comp or demand note |
| `CompanyResearch` | Diligence notes |
| `CultureNote` | Culture observation |
| `DecisionRationale` | Why pursue or decline |

Owned types: JobLead, Role, CompanyTarget, CompensationBand, LocationPreference, RecruiterContact, HiringManager, InterviewStage, InterviewNote, Offer, CounterOffer, RejectionReason, Application, Referral, TargetCriteria, MarketSignal, CompanyResearch, CultureNote, DecisionRationale.

## Progressive disclosure

Default ContextPack: 2 hops. Pack this pack's catalogs only. Pack before
answering or writing.

## Skill binding

Grok Bot does not run `/plugin marketplace add`. Enable only this pack's
skill. Set identity and knowledge root. Report path + commit SHA, not a
dumped graph.

## Three memory planes

| Plane | Location |
|-------|----------|
| Procedural | Skills, this file, [ONBOARDING.md](ONBOARDING.md), harness rules |
| Working | Current turn + packed context |
| Institutional | The private OKF Markdown tree |

## Cursor (Grok Bot coding host)

Grok Bot often opens a **Cursor cloud agent** against the knowledge tree.
That session does **not** automatically have this plugin installed.

- Local Cursor: add the marketplace, then install this plugin. See [CURSOR.md](CURSOR.md).
- Cloud Cursor on the brain: follow this file plus `AGENTS.md` in the knowledge tree. Plugin install is optional. The write protocol is not.
- This pack ships `.cursor-plugin/plugin.json` (Cursor Plugins) and a root `plugin.json` (Agent Plugins 1.0). Cursor loads both. Skills stay in `skills/`.
- Never name a private remote. Pack roots are packing hints, not access control.

## Related public packages

- [second-brain-core](https://github.com/SpillwaveSolutions/second-brain-core)
- [executive-coordination](https://github.com/SpillwaveSolutions/executive-coordination)
- [account-management](https://github.com/SpillwaveSolutions/account-management)
- [sales-pipeline](https://github.com/SpillwaveSolutions/sales-pipeline)
- [executive-job-search](https://github.com/SpillwaveSolutions/executive-job-search)
- [consulting-leads](https://github.com/SpillwaveSolutions/consulting-leads)
- [content-media](https://github.com/SpillwaveSolutions/content-media)
- [news-digest](https://github.com/SpillwaveSolutions/news-digest)
- [gtm-positioning](https://github.com/SpillwaveSolutions/gtm-positioning)

- [second-brain-marketplace](https://github.com/SpillwaveSolutions/second-brain-marketplace)
- [second-brain-starter](https://github.com/SpillwaveSolutions/second-brain-starter)

Foundation:

- [okf-plugin](https://github.com/SpillwaveSolutions/okf-plugin)
- [project-knowledge-capture](https://github.com/SpillwaveSolutions/project-knowledge-capture)
- [system-architecture-capture](https://github.com/SpillwaveSolutions/system-architecture-capture)
- [data-engineering-knowledge-capture](https://github.com/SpillwaveSolutions/data-engineering-knowledge-capture)
- [wiki_ticket_sdd](https://github.com/SpillwaveSolutions/wiki_ticket_sdd)
- [okf-agent-graph](https://github.com/SpillwaveSolutions/okf-agent-graph)
