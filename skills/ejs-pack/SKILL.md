---
name: ejs-pack
description: Build a bounded ContextPack from a Executive Job Search root concept (default 2 hops, 20 nodes).
---

# ejs-pack

## Process

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ejs_common.py" pack \
  --bundle knowledge \
  --root "/job-leads/example.md" \
  --hops 2 \
  --max-nodes 20
```

Use `--hops 1` for a tiny pack. Outbound edges only. Do not dump the whole tree.
