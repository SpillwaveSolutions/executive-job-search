---
name: ejs-init
description: Scaffold the Executive Job Search catalogs in a shared second-brain bundle.
---

# ejs-init

Create the catalogs this plugin owns inside a shared knowledge root.

## Process

1. Confirm target (default `knowledge/`).
2. Run:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/ejs_common.py" init-bundle \
  --bundle knowledge \
  --title "Executive Job Search" \
  --catalogs "job-leads,roles,companies,interviews,offers,applications,criteria"
```

3. Point the user at `sample-knowledge/` for a fictional demo.

## Done when

- `knowledge/index.md` exists
- Each owned catalog has `index.md`
