# Typed edges — Executive Job Search

Direction matters. Packs follow outbound edges by default.

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

Unknown `rel` values are treated as `info` by validation. Do not invent new names in this plugin.
