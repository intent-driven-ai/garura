---
name: link-model-part
description: Put a domain, capability or feature into the product model's spine — the model's index of every part — after its page is written, for a part found during other work (#979). A new part gets its spine entry (its parent, intents, one-line, page, issue, marked to be deepened; a new feature gets its state, status Unplanned, and a domain or capability gets no status, because only a feature has a state — ontology v18, ADR 070); an existing one gets its one-line replaced, its intents added or its issue named; a feature's state is set on request to one of Unplanned, Planned, In progress, Completed or Dropped, any of them after any other, and a status on any other kind or any other value is refused; a one-time migration request takes the old status (proposed, active, deprecated) off every domain and capability and sets Unplanned on every feature that holds none of the five, keeping the rest; a slice that exists gets features added to it, at its end or after a named feature (#931 — a slice itself is shaped only by /design-slice; an /reshape-plan session the person approves may add a feature to a slice in progress, ADR 062); a thin capability or feature gets the thin mark in both places that must agree, metadata.thin on its entry and one Thin line on its page just before its ICE (a domain carries no ICE, so it is never thin); an ICE, which has its own page ice.md beside its part's page, gets its entry in the spine's ices list (the part it is for, its kind and its page), and a thin ICE gets the thin mark on its entry and as one Thin line at the top of its page — a part that has an ICE is never marked thin itself (ontology v15, #1031); and, to take in an old part a person approved (#1037), an existing capability's or feature's thin mark comes off both places (`thin: false`), a feature is filed under another capability (`capability`), and a page moves with the ice.md beside it to a new folder (`doc`), refused while a page names its old path or its old folder holds any other file. Its script does all of it mechanically and all or nothing — an id already there, a parent not in the spine, a page not on disk or outside its folder, an intent with no page, or a path that leaves the model refuses the whole request and writes nothing; the spine keeps its comments and layout. It never writes a page's words; the page skill (enrich-grounding) writes those first. Used through product-os-keeper by any play or run that finds a part the model lacks, without running a discovery play.
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
| `request` | yes | `link-request.json`: `by` (the play or run that asks) and `parts`, each `{id, kind: domain|capability|feature|slice|ice, mode: new|update, ...}` (a slice: `update` only, with `add_features` and an optional `after`; an ICE: `new` with `for` and `doc`, or `update` to mark it thin; a capability or feature on `update` may also take `thin: false`, `doc` and, a feature only, `capability` and `status`) — see the script's header for the fields of each mode. Or, once for a model, the migration request `{"by": ..., "migrate_status": true}`, with no `parts`. |
| `product_base` | yes | The project's product base; the model is under `<product_base>product-os/`. |
| `out` | yes | Where to write `link-report.json`. |

## Process

1. **Check the pages are there.** Each part's page must already be written, in its folder: a
   domain at `<folder>/domain.md`; a capability in `capabilities/<id>/` or under its domain's
   folder; a feature in `features/<id>/` or under its capability's folder; an ICE's page
   `ice.md` in the folder of its part's page, with Intent, Context and Expectation. A thin
   part's page must have its ICE section. When a page is missing, stop and say so — this skill
   never writes one.
2. **Link the parts.** Run the script:

   ```bash
   python3 scripts/link_part.py --request <working>/link-request.json \
       --product-base <product_base> --out <working>/link-report.json
   ```

   Exit 0: every part is in the spine, and each thin one carries its mark. Exit 2: nothing
   was written; the error says which part and why.

   To set a feature's state, give it on `update`, for example
   `{"id": "fn-12", "kind": "feature", "mode": "update", "status": "Planned"}`. To move a model
   off the old status, run the script once with `{"by": "<caller>", "migrate_status": true}`.
3. **Return the report's path.**

## Output

`link-report.json`, at `out`: `written` (each new part's id, an ICE's too), `updated` (each
existing part or ICE changed), `thin` (each part or ICE now marked thin), `unthin` (each part whose
thin mark came off), `moved` (each page moved, from and to), `changed` (every file it touched, relative to the
product base) and `layout_kept` (false only when the spine had to be written whole). A migration
also gives `migrated`: `domains_cleared`, `capabilities_cleared`, `features_set_unplanned` and
`features_kept`. Nothing is written when the script exits 2; its error names the part and why.
A request that changes nothing writes nothing, and its `changed` is empty.

## Rules

- **Only inside the product model.** Every path is checked first; one that leaves
  `<product_base>product-os/` refuses the request.
- **All or nothing.** Every check runs before the first write. One bad part refuses the whole
  request.
- **No page words.** It adds only the Thin line to a page; every other word is the page
  skill's.
- **Only a feature has a state.** Its `status` is one of Unplanned, Planned, In progress,
  Completed or Dropped (ontology v18, ADR 070). A new feature is Unplanned; a `status` on a new
  part is refused. On `update`, any of the five may follow any other: the caller decides the
  move, and this skill keeps no workflow. A domain, a capability, a slice or an ICE takes no
  status. The state names no plan, no issue and no decision record.
- **The migration runs once and is all or nothing.** It removes `status` from every domain and
  capability, whatever it holds, and sets Unplanned on every feature whose status is not one of
  the five (in place, or after its intents when it has none); a feature that holds one of the
  five keeps it. Run again, it finds nothing to change and writes nothing. Marking features
  built before the state existed as Completed is a separate `update` the person confirms.
- **The thin mark is two marks that agree.** `metadata.thin: true` on the spine entry and
  exactly one Thin line on the page, just before its ICE. The play that deepens the part
  removes both. A domain is never thin.
- **An ICE is its own node.** Its entry in `ices` names the one capability or feature it is
  for, never a business intent; each part has at most one. A thin ICE carries the mark on its
  own entry and page, at the top, before Intent; the part it is for is not marked. The `ices`
  list is made only when an ICE is added, because a spine with that list is checked as one
  whose ICE are nodes.
- **Re-file only what a person approved.** A part's parent is set when it is new, and a loose
  part gets its parent from `link-model-gaps`. A feature that already has a capability moves to
  another only through `capability` on `update`, when a person approved taking in an old part
  (#1037); `link-model-gaps` leaves that move as alignment work. The request's `by` names the
  play or run that asks; that caller records the person's approval before it calls, as the
  `/design-slice` brief and a reviewed take-in do. This skill does not check a name.
- **A re-file moves the page too.** A feature lives under its capability's folder, so give
  `capability` with `doc` naming the new folder under that capability. `capability` alone files
  the entry and leaves the page where it is, which suits only a page in the holding folder
  `features/<id>/`.
- **A move breaks no link.** `doc` moves a page and the ice.md beside it, and the ICE's entry
  follows. It is refused while any page or record in the model names an old path, from the
  model root or as a link relative to the page, and while the old folder holds any other file;
  the page skill changes those lines first. The old folder is removed once empty.
- **The thin mark comes off as it went on.** `thin: false` takes `metadata.thin` off the entry
  and every Thin line off the page, together. Give it before the part's ICE in the same request.
