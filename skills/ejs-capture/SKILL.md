---
name: ejs-capture
description: Capture a Executive Job Search noun into the shared second brain via the deterministic write helper.
---

# ejs-capture

## Process

0. If more than one agent writes the shared brain, open an isolation session (`ejs-session`) and export `SECOND_BRAIN_ROOT`.
   Claim identity `grok-bot/executive-job-search` (or `deep-agents/executive-job-search` on Deep Agents).
1. Identify the noun type from the allowed list (see README).
2. Collect title, status, author identity, and optional typed links.
3. Write with the helper — do not hand-author frontmatter unless the user insists:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ejs_common.py" write \
  --bundle knowledge \
  --type JobLead \
  --folder job-leads \
  --title "Example JobLead" \
  --author "Grok Bot: Executive Job Search" \
  --tags "ejs"
```

4. Add typed links in a follow-up edit if needed (`rel` values from `docs/typed-edges.md`).
5. Validate.

Allowed types: JobLead, Role, CompanyTarget, CompensationBand, LocationPreference, RecruiterContact, HiringManager, InterviewStage, InterviewNote, Offer, CounterOffer, RejectionReason, Application, Referral, TargetCriteria, MarketSignal, CompanyResearch, CultureNote, DecisionRationale.
