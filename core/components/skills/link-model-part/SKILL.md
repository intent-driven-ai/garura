---
name: link-model-part
description: Put a domain, capability or feature into the product model's spine — the model's index of every part — after its page is written, for a part found during other work (#979). A new part gets its spine entry (its parent, intents, one-line, page, issue, status proposed, marked to be deepened); an existing one gets its one-line replaced or its intents added; a thin capability or feature gets the thin mark in both places that must agree, metadata.thin on its entry and one Thin line on its page just before its ICE (a domain carries no ICE, so it is never thin). Its script does all of it mechanically and all or nothing — an id already there, a parent not in the spine, a page not on disk or outside its folder, an intent with no page, or a path that leaves the model refuses the whole request and writes nothing; the spine keeps its comments and layout. It never writes a page's words; the page skill (enrich-grounding) writes those first. Used through product-os-keeper by any play or run that finds a part the model lacks, without running a discovery play.
user-invocable: false
model: sonnet
allowed-tools: Read, Bash
---

# link-model-part

The page skill writes a part's page. This skill puts the part into the spine, so the model
knows the page is there, and sets the thin mark when the part is thin. It is mechanical: what
the part is, and its words, were decided before it runs. It works the same way for a domain, a
capability and a feature; an intent has no spine entry of its own (the parts name it in their
`intents`), so an intent page needs only the page skill.

## Input

| Field | Required | Meaning |
|-------|----------|---------|
| `request` | yes | `link-request.json`: `by` (the play or run that asks) and `parts`, each `{id, kind: domain|capability|feature, mode: new|update, ...}` — see the script's header for the fields of each mode. |
| `product_base` | yes | The project's product base; the model is under `<product_base>product-os/`. |
| `out` | yes | Where to write `link-report.json`. |

## Process

1. **Check the pages are there.** Each part's page must already be written, in its folder: a
   domain at `<folder>/domain.md`; a capability in `capabilities/<id>/` or under its domain's
   folder; a feature in `features/<id>/` or under its capability's folder. A thin part's page
   must have its ICE section. When a page is missing, stop and say so — this skill never
   writes one.
2. **Link the parts.** Run the script:

   ```bash
   python3 scripts/link_part.py --request <working>/link-request.json \
       --product-base <product_base> --out <working>/link-report.json
   ```

   Exit 0: every part is in the spine, and each thin one carries its mark. Exit 2: nothing
   was written; the error says which part and why.
3. **Return the report's path.**

## Output

`link-report.json`, at `out`: `written` (each new part's id), `updated` (each existing part
changed), `thin` (each part now marked thin), `changed` (every file it touched, relative to the
product base) and `layout_kept` (false only when the spine had to be written whole). Nothing is
written when the script exits 2; its error names the part and why.

## Rules

- **Only inside the product model.** Every path is checked first; one that leaves
  `<product_base>product-os/` refuses the request.
- **All or nothing.** Every check runs before the first write. One bad part refuses the whole
  request.
- **No page words.** It adds only the Thin line to a page; every other word is the page
  skill's.
- **The thin mark is two marks that agree.** `metadata.thin: true` on the spine entry and
  exactly one Thin line on the page, just before its ICE. The play that deepens the part
  removes both. A domain is never thin.
- **Never re-parent.** A part's parent is set when it is new; moving it later is
  `link-model-gaps`'s work.
