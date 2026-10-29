# Design — #993 The page skill changes named lines on any model page

Plan 717, story of #720 (manage a plan). Waiting for the product owner's approval.

## What changes for a person

A play or a person asks the model sub-agent to change some lines on a model page — a domain,
capability, feature or intent page — and gives the new words. Exactly those lines change; every
other line stays word for word. Today that works only on an intent page.

## Surface

The request the model sub-agent hands the page skill (`enrich-grounding`, update or fix mode):

```json
{"page": "capabilities/cap-720/capability.md",
 "source": "the approved design of #720, .garura/project/issues/720/specs/design.md",
 "changes": [{"old": "- Goal: After any change, the plan file and the tracker agree.",
              "new": "- Goal: After the person approves, the plan file, GitHub and the product model agree, and nothing beyond the approved list has changed."}]}
```

- `old` is a whole line as it is on the page; `new` is the line that replaces it. A change may add
  a line after another (`"after": "<line>"`) or remove one (`"new": null`).
- `source` names where the change comes from: an approved design, or the person's own words. The
  skill does not decide what the part means; the request does.

## Tech

- A new script in the skill, `scripts/change_lines.py`, does the change mechanically:
  - checks every path stays inside the product model;
  - checks every `old` line is on its page exactly once — else it refuses the whole request, names
    the line, and writes nothing;
  - writes every page through the model's `safe_write.py` (a page is whole or unchanged);
  - writes `lines-report.json`: each page, each change old and new, and the count of lines kept.
- The skill's step 5 (today: intent pages only) becomes "any page, update or fix mode", and calls
  the script. Its rules keep: never write `_spine.yaml`, the Thin line or `metadata.thin`; never
  write a new intent page.
- `product-os-keeper` routes "change these lines" on any page to the skill (today its route names
  intent pages only).
- Tests for the script: change one line, several lines on two pages, add after, remove; refuse a
  line not on the page, a line on it twice, a path outside the model; nothing written on a refusal.
- `enrich-grounding` is a skill, not a play: a direct edit to its SKILL.md, no ICE recompile.

## Then, in this change

Through `product-os-keeper` and the skill (never by hand): cap-720's directional intent and its
four ICE lines, and fn-730's "What it does" and its four ICE lines, to the approved #720 design.

## Not in this change

- Titles of GitHub issues (no skill can edit a title today; the #775 rename has the same gap).
- `/update-plan` itself (#730).
