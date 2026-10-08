# Issue Output Template

Structured output for `manage-issue` skill.

## Format

```yaml
issue:
  number: {int}
  title: "{title}"
  labels: [{label_names}]
  state: "{open|closed}"
  body_summary: "{first 200 chars of body}"
  body: "{full body}"            # action read only
  url: "{html_url}"
  created: {true|false}
  closed: {true|false}
  parent_issue: {parent_number or null}
  type: "{issue type name or null}"          # e.g. Feature, Story, Business Intent
  parent:                                    # action read only; null when none
    number: {int}
    title: "{title}"
    state: "{open|closed}"
  sub_issues:                                # action read only; [] when none
    - number: {int}
      title: "{title}"
      state: "{open|closed}"
  tree_available: {true|false}               # false when the platform or gh version cannot report type/parent/sub-issues
```

## Field Descriptions

| Field | Description |
|-------|-------------|
| `number` | GitHub issue number |
| `title` | Issue title |
| `labels` | List of label name strings |
| `state` | Current issue state (`open` or `closed`) |
| `body_summary` | First 200 characters of the issue body |
| `url` | Full HTML URL to the issue |
| `created` | `true` if this skill created the issue, `false` if it already existed |
| `closed` | `true` if this skill closed the issue, `false` otherwise |
| `parent_issue` | Parent issue number — from the tracker on `read`, or the parent just attached on `create` / `resolve_or_create`; `null` when none |
| `body` | Full issue body. `read` only — callers that build context (e.g. the plan context) need all of it, not the summary |
| `type` | The tracker's issue type name (`issueType.name`), or `null` when the issue has none or the tracker cannot say |
| `parent` | `read` only: the parent issue's number, title and state, from the tracker's parent/child link; `null` when none |
| `sub_issues` | `read` only: each child issue's number, title and state, from the tracker's parent/child link; `[]` when none. A mention in the body is never a child |
| `tree_available` | `true` when the platform reported type, parent and sub-issues. `false` on GitLab, or on GitHub with gh older than 2.94.0 — then `type`, `parent` and `sub_issues` are unknown, not empty, and callers must say so |
