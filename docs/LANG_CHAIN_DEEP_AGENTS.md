# LangChain Deep Agents / Deep Agents Code

How to use this Spillwave ContentPack with LangChain Deep Agents and Deep Agents Code (`dcode`).

This package already follows the open **Agent Skills** layout (`skills/*/SKILL.md`). Deep Agents loads the same format.

## Privacy and knowledge root

The institutional second brain is a local or private OKF tree the human already owns.

- Point Deep Agents at that tree with `SECOND_BRAIN_ROOT`.
- Never hard-code a remote URL or clone command.
- Public samples use only fictional Northstar / Lumenfield data.

## Install / discovery

### Filesystem skills source

```python
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend

agent = create_deep_agent(
    model="...",
    backend=FilesystemBackend(root_dir=".", virtual_mode=True),
    skills=["./path/to/executive-job-search/skills/"],
)
```

Or with SkillsMiddleware:

```python
from deepagents.middleware import SkillsMiddleware

SkillsMiddleware(
    backend=backend,
    sources=["/skills/", "/path/to/executive-job-search/skills/"],
)
```

```bash
npx skills add SpillwaveSolutions/executive-job-search --skill '*' --yes
```

This repo ships a root `plugin.json` conforming to https://agent-plugins.org.

## Isolation

Deep Agents on one project worktree must not write main of the shared brain directly.

```bash
python3 path/to/second-brain-core/scripts/brain_session.py open \
  --repo "$BRAIN_REPO" \
  --bundle knowledge \
  --actor deep-agents/executive-job-search \
  --plugin executive-job-search \
  --host deep-agents
```

Then set `SECOND_BRAIN_ROOT` to the session bundle from the JSON. Close the session to PR.

## Deterministic write boundary

```bash
export SECOND_BRAIN_IDENTITY="deep-agents/executive-job-search"
python3 scripts/ejs_common.py write \
  --bundle "${SECOND_BRAIN_ROOT:-knowledge}" \
  --type JobLead \
  --folder job-leads \
  --title "..." \
  --author "${SECOND_BRAIN_IDENTITY}"
```

Wrap the scripts as tools or shell. The model proposes. The scripts commit.

## Progressive disclosure

Startup sees skill frontmatter only. Pack (2 hops) before answering or writing.

## Related

- Agent Skills spec
- Agent Plugins 1.0
- second-brain-core docs/ISOLATION.md, docs/GROK_BOT.md
