---
name: remove-model-part
description: Take parts out of the product model once a person has approved it. It repoints what named an old business intent to a new one, or drops it, part by part; removes a business intent's page once nothing names it; merges a capability into another (its features, links, intents and decisions move, and its needs are listed for review, never copied); and removes a slice and its record. Its script does all of it mechanically and all or nothing, on a copy, with every check run before the first write — no name of the person who approved, a part still named by the spine, a page that still names a part being removed (each path and line is named), a capability folder with any other file, or a path that leaves the model refuses the whole request and writes nothing; when a write fails, every file is put back. The spine keeps its comments and layout. It never writes a page's words; the page skill fixes those first, and a survivor's page is the page skill's work. Used through product-os-keeper by any play or run carrying out a removal a person approved.
user-invocable: false
model: sonnet
allowed-tools: Read, Bash
---

# remove-model-part

A part leaves the product model only when a person said so and when nothing is left that still
names it. This skill does the removal: the spine and the files. It is mechanical: what goes, what
replaces it and who approved were decided before it runs.

## Input

| Field | Required | Meaning |
|-------|----------|---------|
| `request` | yes | `remove-request.json`: `by` (the play or run that asks), `approved_by` (the person who approved it), and at least one item in `repoint` or `remove` — see below. |
| `product_base` | yes | The project's product base; the model is under `<product_base>product-os/`. |
| `out` | yes | Where to write `remove-report.json`. |

```json
{"by": "<the play or run that asks>",
 "approved_by": "<the person who approved it>",
 "repoint": [{"id": "cap-2", "kind": "capability", "intents": {"bi-1": "bi-3"}},
             {"id": "cap-3", "kind": "capability", "intents": {"bi-2": null}}],
 "remove": [{"kind": "intent", "id": "bi-1"},
            {"kind": "capability", "id": "cap-4", "into": "cap-3"},
            {"kind": "slice", "id": "sl-old"}]}
```

A part to repoint is a domain, a capability, a feature or a slice. In `intents`, each old business
intent maps to its new one, or to `null` to drop it. Two parts that shared an intent can go to
different new ones. A capability is never simply removed: it merges `into` another.

## Process

1. **Have the words fixed first.** Every id being removed must be gone from the pages. Ask the page
   skill (`enrich-grounding`) to change the lines that name it. When the script refuses, it names
   each path and line still to fix.
2. **Run the script:**

   ```bash
   python3 scripts/remove_part.py --request <working>/remove-request.json \
       --product-base <product_base> --out <working>/remove-report.json
   ```

   It works on a copy, in this order: repoints, capability merges, slice removals, intent
   removals. Every check runs, and only then is the first file changed. Exit 0: done. Exit 2:
   nothing was written; the error names the part or the line and why.
3. **Return the report's path.** Pass on `needs_to_review` as it is: a merged capability's needs
   are for a person to look at.

What a merge does: the capability's features move to the survivor. Whatever was identified by it,
or depended on it, now names the survivor, never twice and never the survivor itself. The survivor
gains the intents it lacks, in order, and the decisions. The capability's page goes, and its folder
when that is then empty.

A merge is a one-time change, so the spine keeps no record of it. The report's `merged` list is the
run's record. The merged capability's issue number is gone from the model; the tracker keeps the
issue.

## Output

`remove-report.json`, at `out`: `by`, `approved_by`, `repointed` (ids), `removed` (ids), `merged`
(`[{id, into}]`), `moved_features`, `needs_to_review` (a merged capability's non-empty `nfr_needs` or
`compliance_needs`, with its id), `changed` and `deleted` (paths relative to the product base) and
`layout_kept` (false only when the spine had to be written whole). No report is written when the
script exits 2.

## Rules

- **Never without the person's name.** A request with no `approved_by` is refused.
- **No page words.** It writes only the spine and deletes files. A mention left on a page refuses
  the request, so the page skill fixes those words first. The page of a survivor is the page skill's
  work too.
- **All or nothing.** One bad item refuses the whole request, every check runs before the first
  write, and when a write or a delete fails every file is put back as it was.
- **Only inside the product model.** An id or a page path that leaves `<product_base>product-os/`
  refuses the request. Nothing under the plans folder is touched, even for a slice.
- **The removed id stays nowhere.** Anywhere in the changed spine's data it refuses the request,
  naming the part. Comments in the spine do not count.
- **A capability with more than its page does not go.** A folder that holds any other file, or an
  entry in the spine's `ices` list, refuses the merge and is named.
