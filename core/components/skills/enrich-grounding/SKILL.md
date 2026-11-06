---
name: enrich-grounding
description: Write on the pages of the product-model parts a slice needs, for /shape-slice, from the person's answers and the assumptions, keeping every section and line a page had — bring each domain, capability or feature page the slice moves or uses up to the current grounding rules, in place; write one new feature page under a capability that exists, without re-detailing the capability; thin-ICE mode writes the minimum ICE (Goal, Limit, Fails if, Context, Checked by) for a part that has none; fix mode fixes the problems the model check finds in those pages; on any page — domain, capability, feature or intent — update and fix mode can instead change only the lines a request names, to the words it gives (for example a capability's ICE to an approved design, or a real name to a persona), through its change_lines.py script, all or nothing; approved mode writes a domain, capability, feature or ICE page (ice.md, beside its part's page, with Intent, Context and Expectation) from text a person approved, word for word, through its write_approved.py script, all or nothing. Writes per-node pages only; it never writes _spine.yaml, the Thin line or any shared file. Generative artifact production for /shape-slice, and for a part found during other work (#979), through product-os-keeper, before link-model-part. Use when the pages of the model's parts need to be written, raised to the current rules, given a thin ICE, or fixed, or when named lines of a page must change, or when a page a person approved must be written as it is.
user-invocable: false
model: opus
allowed-tools: Read, Write, Bash
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
| `mode` | no | `update` (the default), `new-feature`, `thin`, `fix` or `approved`; an intent page takes `update` or `fix` only; a named-lines request (step 5) takes `update` or `fix`; an approved-text request (step 6) takes `approved` |
| `pages` | yes | The pages to work on, each `{id, kind: domain|capability|feature|intent, doc}` — in a slice run, from `fills.json` `updates` with `page: true`, its new features under a capability that exists, and its `thin` list; for found work, from the request |
| `product_base` | yes | The live model root. The pages are read and written in place under `{product_base}product-os/` |
| `schemas_dir` | yes | The grounding templates (`domain.md`, `capability.md`, `feature.md`) and the content standard, copied into short-term memory by the agent through the memory tool |
| `intent_page` | in a slice run | The business intent the slice serves |
| `record` | in a slice run | The question record: the person's answers are facts |
| `split` | in a slice run | `split.json`: each assumption is used as it is written |
| `fills` | in a slice run | `fills.json`: the parent of each new feature, and the thin parts |
| `request` | for found work | What the person asked for, and the sources to write from (the design, the issue texts). In place of `record`, `split` and `fills` |
| `lines_request` | for named lines | `lines-request.json` (step 5), written by the agent that dispatches this skill, never by the skill: `by`, `source` (an approved design, or the person's own words) and `pages`, each `{page, changes}` — a change is `{old, new}` (`new: null` removes the line) or `{after, add}`; see the script's header |
| `approved_request` | for `approved` | `approved-request.json` (step 6), written by the agent that dispatches this skill, never by the skill: `by`, `approved_by` (the person), `source` (where the approval is recorded) and `pages`, each `{page, from}` — `from` is the file holding the approved text; see the script's header |
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
5. **Named lines, on any page (update or fix mode).** When the request names lines to change —
   on a domain, capability, feature or intent page — change only those lines, to the words it
   gives: for example a capability's ICE to an approved design, or a real person's name to a
   persona (`the product owner`). The agent wrote each line to change, whole and as it is on the
   page, in `lines-request.json` with the request's source, and handed you its path
   (`lines_request`); you do not write or change it. Run the script on it:

   ```bash
   python3 scripts/change_lines.py --request <lines_request> \
       --product-base <product_base> --out <working>/lines-report.json
   ```

   Exit 0: every named line changed and every other line kept, word for word, with its own line
   ending. Exit 2: nothing was written, or every page already written was put back; the error
   names the page and the line (not on the page, on it twice, named twice, a Thin line, a path
   outside the model, a line that cannot be written, or no source). Return the error to the
   agent, which corrects the request; never work around it. The meaning comes from the
   request's source, never from this skill: a new intent page is /discover-intent's, and a
   change of meaning is the person's or an approved design's.
6. **Approved mode — write a page a person approved, word for word.** When a person reviewed a
   page's text before it reaches the model, the page is copied as it is: nothing is composed.
   This covers a domain, capability or feature page, and an ICE page. An ICE has its own page,
   `ice.md`, in the folder of its part's page, with `## Intent`, `## Context` and
   `## Expectation`, in that order (ontology v15); a part's page holds no ICE section. The agent
   wrote `approved-request.json` and handed you its path (`approved_request`); you do not write
   or change it. Run the script on it:

   ```bash
   python3 scripts/write_approved.py --request <approved_request> \
       --product-base <product_base> --out <working>/approved-report.json
   ```

   Exit 0: every page holds its approved text, word for word, new or replacing the page that
   was there. Exit 2: nothing was written, or every page already written was put back; the
   error names the page and why (a Thin line in the text, an ICE section on a part's page, an
   ICE page without its three parts or with no part beside it, a wrong title, an intent page,
   a path outside the model, a thin page on disk, or no one who approved). Return the error to
   the agent; never work around it. The ICE page's entry in the spine and its thin mark are
   `link-model-part`'s, run after this.
7. **Fix mode.** Fix each problem that names one of the pages: a missing section, an old
   heading, a broken link, a thin ICE that lacks a line. Change only what the problem names.
   A problem in `slice.json` or `fills.json` is not this skill's: list it in `not_mine`.
8. **Check the page against what it had.** Every section and line from step 1 is still on
   the page, except the lines a named-lines request (step 5) replaced or removed — its
   `lines-report.json` names each one — and a page approved mode (step 6) wrote, which holds
   its approved text. When any other line is lost, put it back before you write the report.

## Output

The pages, written in place under `{product_base}product-os/`, and `grounding-report.json`:

```json
{"updated": [{"id": "cap-booking", "doc": "care/booking/capability.md",
              "added_sections": ["Guiding rules"], "renamed": [], "kept_lines": 41}],
 "new_features": [{"id": "ft-confirm-a-booking", "doc": "care/booking/confirm/feature.md"}],
 "thin": [{"id": "ft-confirm-a-booking", "lines": ["Goal", "Limit", "Fails if", "Context", "Checked by"]}],
 "fixed": [], "not_mine": []}
```

A named-lines request (step 5) writes `lines-report.json` instead: `source`, and for each page
each change (old and new, or after and add), its line counts before and after and the lines
kept, and `changed` (every page written). An approved-text request (step 6) writes
`approved-report.json`: `written` (each page, `created` or `replaced`), `approved_by` and
`source`.

Examples from different fields:
- A clinic: the Booking capability's page had no Guiding rules section; the run adds it, with
  the person's rule that a slot is held for ten minutes, and keeps its old Scope text.
- A shop: a new feature "Pay with a saved card" goes under the Checkout capability that
  exists; Checkout gets one new line in its Features list and nothing else.
- A school: "Send a note home" has no ICE; the thin ICE says Goal: each family gets its own
  child's note; Fails if: a parent sees a note for another child.

## Rules

- In place: keep every section and line a page had, except the lines a named-lines request
  names (step 5) and a page a person approved whole (step 6); never remove or move a page.
- Write per-node pages only. Never write `_spine.yaml`, the profile, a decision, the Thin
  line or `metadata.thin`; a play's scripts or `link-model-part` write them. On an intent
  page, change only the lines the request names (step 5); never write a new intent page. A
  named-lines request goes through `change_lines.py`, and an approved-text request through
  `write_approved.py`, each all or nothing.
- A thin ICE has a Goal, a Limit, one Fails if line or more, a Context line and a Checked by
  line, each from the person's answers or the assumptions; nothing made up.
- One new feature under a capability that exists never re-details the capability.
- Plain words (ASD-STE100), personas only, no real names.
