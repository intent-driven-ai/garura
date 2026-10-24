# Input Contract — check-pr-quality

## Required fields

| Field | Type | Description |
|---|---|---|
| `diff_path` | string | Absolute or repo-relative path to a unified diff file |
| `changed_paths` | string[] | Repo-relative paths of files touched by the diff |
| `standards_order` | string[] | From `.garura/core/config.yaml` `review-pr.standards_order` (for example `[kb, ltm, stm]`) |
| `severity_taxonomy_path` | string | The short-term copy of the memory rule `standards/rules/pr.md`, which `quality-auditor` fetched through the memory tool (`<issue folder>/context/memory/standards/rules/pr.md`) |
| `intent_summary` | string | 1–3 sentences from `spec/intent.yaml` or PR body |
| `output_path` | string | Where to write `findings.yaml` |

## Resolution

The caller (check-change Step 3 via `quality-auditor`) reads memory only through the memory tool: it copies `standards/rules/pr.md` into the issue's short-term memory and passes that copy. No path in this contract points into memory or into Garura's source. Pre-flight validates that `severity_taxonomy_path` exists before the scan runs.

## Optional fields

None. Any extra fields are ignored.

## Example

```yaml
diff_path: .garura/project/issues/208/evidence/review-pr/diff.patch
changed_paths:
  - src/api/users.ts
  - src/db/migrations/0042_add_email.sql
  - .env.example
standards_order: [kb, ltm, stm]
severity_taxonomy_path: .garura/project/issues/208/context/memory/standards/rules/pr.md
intent_summary: "Add email verification flow with token expiry."
output_path: .garura/project/issues/208/evidence/review-pr/findings.yaml
```
