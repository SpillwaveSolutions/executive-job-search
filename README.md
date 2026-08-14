# Executive Job Search

Executive job-search ContentPack: job leads, roles, compensation bands, interview stages, offers, and target criteria.

MIT. Dual-host: **Claude Code**, **Grok Build**, and **Codex** (Agent Skill Standard). Writes OKF Markdown + YAML into a shared second-brain bundle so other agents and local jobs can read the same graph.

## Install

```bash
# Claude Code
/plugin marketplace add SpillwaveSolutions/executive-job-search
/plugin install executive-job-search@SpillwaveSolutions

# Skilz CLI
skilz install SpillwaveSolutions/executive-job-search
```

Point the plugin at a shared knowledge root (default `knowledge/`). All sibling ContentPack plugins write into the same tree.

## Skills

| Skill | What it does |
|-------|----------------|
| `/ejs-init` | Scaffold the catalogs this plugin owns |
| `/ejs-capture` | Capture a noun into the shared second brain (deterministic write) |
| `/ejs-pack` | Build a bounded ContextPack from a root concept |
| `/ejs-validate` | Validate frontmatter, types, and links |
| `/ejs-doctor` | Health check of the bundle this plugin owns |

## Nouns this plugin may write

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

## Relationships

| `rel` | Meaning |
|-------|---------|
| `owned_by` | Job-search agent identity |
| `at_company` | Role or lead at company |
| `matches` | Lead matches target criteria |
| `referred_by` | Came from referral or recruiter |
| `in_stage` | Current interview stage |
| `originates_from` | Scan or intro source |
| `related_to` | Similar roles |
| `resulted_in` | Application became offer or rejection |

## Catalogs

- `job-leads/`
- `roles/`
- `companies/`
- `interviews/`
- `offers/`
- `applications/`
- `criteria/`

## Deterministic write boundary

The model proposes. Schema-enforced scripts commit:

```bash
python3 scripts/ejs_common.py write \
  --bundle knowledge \
  --type JobLead \
  --folder job-leads \
  --title "Example" \
  --author "Grok Bot: Executive Job Search"
```

Never invent `rel` values. Never write types owned by another plugin.



## Related plugins

- [second-brain-core](https://github.com/SpillwaveSolutions/second-brain-core) — shared pack engine and typed-edge conventions
- [project-knowledge-capture](https://github.com/SpillwaveSolutions/project-knowledge-capture) — the “why” second brain
- [system-architecture-capture](https://github.com/SpillwaveSolutions/system-architecture-capture) — the “what is running” second brain
- [wiki_ticket_sdd](https://github.com/SpillwaveSolutions/wiki_ticket_sdd) — visible work log

## License

MIT. Copyright 2026 Rick Hightower / contributors.
