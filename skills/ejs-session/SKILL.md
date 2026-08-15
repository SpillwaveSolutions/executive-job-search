---
name: ejs-session
description: Open or close an isolated second-brain write session (worktree + PR). Use before writing when multiple agents share one knowledge remote.
---

# ejs-session

## When

- More than one agent or machine writes the shared second brain
- The current project worktree is not the knowledge repo
- The user asks to isolate writes, open a knowledge PR, or avoid clobbering main

## Open

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brain_session.py" open \
  --repo . \
  --bundle knowledge \
  --actor "${SECOND_BRAIN_IDENTITY:?claim an identity first}" \
  --plugin executive-job-search \
  --host claude-code
```

Export `SECOND_BRAIN_ROOT` and `BRAIN_SESSION_ID` from the JSON. All writes go to that bundle via `ejs_common.py write --author`.

## Close

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brain_session.py" close \
  --repo . \
  --session "${BRAIN_SESSION_ID}"
```

Pushes to whatever remote the checkout already has and opens a PR when `gh` is available. Never force-push. Never invent a remote URL.

## Rules

- Read shared truth from main. Overlay this session only.
- Do not pack other agents' open branches.
- See second-brain-core `docs/ISOLATION.md`.
