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
