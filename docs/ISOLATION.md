# Write isolation

This pack uses the same protocol as second-brain-core.

Read `docs/ISOLATION.md` in [second-brain-core](https://github.com/SpillwaveSolutions/second-brain-core/blob/main/docs/ISOLATION.md).

```
read  → origin/main + optional session overlay
write → brain/<actor>/<session-id> worktree only
close → commit, push to the checkout's existing remote, open PR
```

```bash
python3 scripts/brain_session.py open \
  --repo . \
  --bundle knowledge \
  --actor "$SECOND_BRAIN_IDENTITY" \
  --plugin <this-pack> \
  --host <claude-code|grok-bot|deep-agents|codex|grok-build>
```

This document never names a private remote. `SECOND_BRAIN_ROOT` is a local path the human already has.
