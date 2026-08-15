# Changelog

## 0.3.0 — 2026-08-15

- Grok Bot onboarding: `docs/ONBOARDING.md` (LLM-wiki history, destination state, public repo list)
- Full type ownership in `docs/GROK_BOT.md` (every registry noun, not a subset)
- Registry folders filled so writes land in the right catalog
- Linked Northstar sample graph (typed edges, packable in 2 hops)
- Version stamps aligned across plugin.json, marketplace, and package.json
- README related-plugins list now covers the whole suite plus foundations

## 0.2.0 — 2026-08-15

- Write isolation: `scripts/brain_session.py` (worktree + branch + PR)
- Required `--author` / `SECOND_BRAIN_IDENTITY`; emit `WriteEvent` on write
- Session overlay on pack (`--overlay`)
- Agent Plugins 1.0 root `plugin.json`
- `docs/GROK_BOT.md`, `docs/LANG_CHAIN_DEEP_AGENTS.md`, `docs/ISOLATION.md`
- Codex hooks (`.codex-plugin` + `hooks/hooks.json`)
- Host skills for Grok Bot and LangChain Deep Agents

## 0.1.0 — 2026-08-14

- Initial public release
- Nouns: JobLead, Role, CompanyTarget, CompensationBand, LocationPreference, RecruiterContact, HiringManager, InterviewStage, InterviewNote, Offer, CounterOffer, RejectionReason, Application, Referral, TargetCriteria, MarketSignal, CompanyResearch, CultureNote, DecisionRationale
- Skills: ejs-init, ejs-capture, ejs-pack, ejs-validate, ejs-doctor
- Dual-host plugin manifests (Claude Code + Grok Build)
