---
name: enrich-grounding
description: Write on the pages of the product-model parts a slice needs, for /shape-slice, from the person's answers and the assumptions, keeping every section and line a page had — bring each domain, capability or feature page the slice moves or uses up to the current grounding rules, in place; write one new feature page under a capability that exists, without re-detailing the capability; thin-ICE mode writes the minimum ICE (Goal, Limit, Fails if, Context, Checked by) for a part that has none; fix mode fixes the problems the model check finds in those pages. Writes per-node pages only; it never writes _spine.yaml, the Thin line or any shared file. Generative artifact production for /shape-slice. Use when /shape-slice needs the pages of its parts written, raised to the current rules, given a thin ICE, or fixed.
user-invocable: false
model: opus
allowed-tools: Read, Write
---

# enrich-grounding

A slice uses pages that other plays wrote, at other times, under older rules. /shape-slice
brings each page it moves or uses up to the current rules in the same run, and adds what the
slice needs and the page lacks. This skill writes that page content. It works on one page at
a time and keeps everything the page had. The play's scripts write the spine, the thin marks
and every move of a page.

## Input

| Field | Required | Meaning |
|-------|----------|---------|
| `mode` | no | `update` (the default), `new-feature`, `thin` or `fix` |
| `pages` | yes | The pages to work on, each `{id, kind: domain|capability|feature, doc}` — from `fills.json` `updates` with `page: true`, its new features under a capability that exists, and its `thin` list |
| `product_base` | yes | The live model root. The pages are read and written in place under `{product_base}product-os/` |
| `schemas_dir` | yes | The grounding templates (`domain.md`, `capability.md`, `feature.md`) and the content standard, copied into short-term memory by the agent through the memory tool |
| `intent_page` | yes | The business intent the slice serves |
| `record` | yes | The question record: the person's answers are facts |
| `split` | yes | `split.json`: each assumption is used as it is written |
| `fills` | yes | `fills.json`: the parent of each new feature, and the thin parts |
| `problems` | for `fix` | `slice-check.json` (or a script's refusal): each problem with the page it names |
| `out` | yes | Where to write `grounding-report.json` |

## Process

1. **Read the page and its template.** Read the page as it is now, and the template of its
   kind in `schemas_dir`. Make a list of every section and every line the page has.
2. **Update mode — bring the page up to the current rules, in place.** Add each section the
   template asks for and the page lacks, at the page's own stage. Rename an old heading to
   the template's name and keep its text. Add what the slice needs from the person's answers
   and the assumptions (for example the intent it now serves, a rule the person gave). Never
   remove a section or a line; never move the page (the play's script moves pages).
3. **New-feature mode — one new feature under a capability that exists.** Write the new
   feature's page at its `doc` path, from the feature template, at the depth the run knows:
   what it does, its inputs and outputs, its rules, its acceptance criteria and what is out
   of scope, from the intent, the answers and the capability's page. Do not re-detail the
   capability and do not write its other features. Add one line for the new feature to the
   capability's Features list, in place.
4. **Thin mode — the minimum ICE for a part with none.** In the page's
   `## Agent intent (ICE)` section (or in its `ice.md` when the spine has an `ices` list),
   write from the person's answers and the assumptions:
   - `- Goal:` what must be true;
   - `- Limit:` a line that must not be crossed;
   - `- Fails if:` one line at least, that an eval can see from the outside;
   - `- Context:` who it serves and what it touches;
   - `- Checked by:` how a goal is checked.
   In an `ice.md`, Goal, Limit and Fails if go under `## Intent`, the Context line under
   `## Context`, and the Checked by line under `## Expectation`. Do not write the Thin line
   and do not set `metadata.thin`: the play's script writes the two thin marks.
5. **Fix mode.** Fix each problem that names one of the pages: a missing section, an old
   heading, a broken link, a thin ICE that lacks a line. Change only what the problem names.
   A problem in `slice.json` or `fills.json` is not this skill's: list it in `not_mine`.
6. **Check the page against what it had.** Every section and line from step 1 is still on
   the page. When one is lost, put it back before you write the report.

## Output

The pages, written in place under `{product_base}product-os/`, and `grounding-report.json`:

```json
{"updated": [{"id": "cap-booking", "doc": "care/booking/capability.md",
              "added_sections": ["Guiding rules"], "renamed": [], "kept_lines": 41}],
 "new_features": [{"id": "ft-confirm-a-booking", "doc": "care/booking/confirm/feature.md"}],
 "thin": [{"id": "ft-confirm-a-booking", "lines": ["Goal", "Limit", "Fails if", "Context", "Checked by"]}],
 "fixed": [], "not_mine": []}
```

Examples from different fields:
- A clinic: the Booking capability's page had no Guiding rules section; the run adds it, with
  the person's rule that a slot is held for ten minutes, and keeps its old Scope text.
- A shop: a new feature "Pay with a saved card" goes under the Checkout capability that
  exists; Checkout gets one new line in its Features list and nothing else.
- A school: "Send a note home" has no ICE; the thin ICE says Goal: each family gets its own
  child's note; Fails if: a parent sees a note for another child.

## Rules

- In place: keep every section and line a page had; never remove or move a page.
- Write per-node pages only. Never write `_spine.yaml`, the profile, a decision, an intent
  page, the Thin line or `metadata.thin`; the play's scripts write them.
- A thin ICE has a Goal, a Limit, one Fails if line or more, a Context line and a Checked by
  line, each from the person's answers or the assumptions; nothing made up.
- One new feature under a capability that exists never re-details the capability.
- Plain words (ASD-STE100), personas only, no real names.
