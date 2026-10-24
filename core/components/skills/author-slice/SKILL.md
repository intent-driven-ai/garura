---
name: author-slice
description: Choose the one slice that shows a business intent is served, for /shape-slice — the one surface and the persona who tests it there (the tester), the features from any capability in build order with why_this_order, what is left out, and the needs list of the model (fills.json — the new parts, the updates to parts that exist, the thin parts). Writes slice.json and fills.json, or no-slice.json with its reason when no surface can be tested end to end. Reuse mode writes reuse.json (pull_in, push_out, why) for a kept slice and keeps it testable end to end; it never changes a slice in progress. Fix mode fixes the problems the model check finds in slice.json or fills.json. Each choice names the lines it rests on, so its agent can record the trace. Reads only what its agent put in short-term memory; never writes the model, the spine or a page. Generative artifact production for /shape-slice (ontology v11). Use when /shape-slice needs the slice chosen, a kept slice compared, or a slice record fixed.
user-invocable: false
model: opus
allowed-tools: Read, Write
---

# author-slice

A slice is an ordered group of features that one person can test end to end, on one surface,
to show a business intent is served. This skill makes every choice of the slice: the surface,
the tester, the features and their build order, what is left out, and what the model must get
so the slice can be built. The agent only gathers the context and passes this skill's output
on; the play's scripts write the spine, the slice record and the pages' marks.

## Input

| Field | Required | Meaning |
|-------|----------|---------|
| `mode` | no | `shape` (the default), `reuse` or `fix` |
| `intent_page` | yes | The business intent's page in the model: title, outcome, why, asked by, proof it is met, must not |
| `gather` | yes | `gather.json`: each model page and memory line the agent read (tier, path, lines, fingerprint), with the short-term copies |
| `placement` | yes, to shape | The `find-work-placement` routing result: where each part of the intent's outcome sits (domain, capability, feature) |
| `record` | yes | The question record (`grounding-questions.md`): the person's answers are facts |
| `split` | yes, to shape | `split.json`: the questions asked and the assumptions (each gap not asked, with its `assume` text) |
| `spine` | yes | The spine, read only: the domains, capabilities, features, ICE and slices that exist, with their folders |
| `change` | no | The person's `change: <what>` at the checkpoint, on a re-run |
| `serving` | for `reuse` | `serving.json` from `find_serving_slice.py`: the matched slice, its reason, and the slices in progress |
| `slice` | for `reuse` and `fix` | The shaped `slice.json` |
| `fills` | for `fix` | The `fills.json` to fix |
| `problems` | for `fix` | `slice-check.json` (or a script's refusal message): each problem with the page or field it names |
| `out` | yes | The folder to write to: `slice.json`, `fills.json` and `no-slice.json` (shape and fix), `reuse.json` (reuse) |

## Process

### Shape mode

1. **Read the intent as the goal.** The outcome says what the person must see when the intent
   is served. The proof says how that is measured. The person's answers in `record` are facts;
   each assumption in `split` is used as it is written.
2. **Choose the one surface and its tester.** The surface is one place where a person does
   the thing the outcome names: a screen, a command line command or an endpoint. The tester is
   a persona: a role the domain knows, who uses that surface to do it. Take both from the
   intent page (asked by, outcome), the personas and journeys in the model, and the placement.
   Never ask the person for them: they see the surface and the tester in the brief and say yes
   or change them. Exactly one surface. Write `user_action`: what the tester does there, in
   one plain sentence.
3. **When nothing names a surface a person can test end to end**, write `no-slice.json`
   `{reason, looked_at: [the pages and lines read]}`, and write no `slice.json` and no
   `fills.json`. A reason says what is missing in plain words ("no screen, command or endpoint
   lets a patient do the booking the outcome names").
4. **Choose the features, in build order.** Take every feature the outcome needs from any
   capability, one per thing the tester must do or see on the surface. Use the placement for
   each part of the outcome; a part the model does not hold yet is a new feature. The build
   order is the order in which the tester can test them: a feature that another one needs
   comes first. Write `why_this_order` in one or two plain sentences.
5. **List what is left out.** Each thing the intent or the model holds that the slice does
   not take, with why (`left_out: [{what, why}]`). When nothing is left out, write an empty
   list.
6. **Write the needs list (`fills.json`).** For each domain, capability, feature or ICE that
   the slice needs:
   - the model has it and it serves the intent already: list nothing;
   - the model has it, and it lacks the intent, or its domain (a capability) or its
     capability (a feature): write one entry in `updates` —
     `{id, kind: domain|capability|feature, add_intents: [<intent>], domain | capability: <id>, page: true}`.
     Give the domain or capability only when the part has none. Set `page: true` for each
     part whose page the slice moves or uses (each feature of the slice, its capability and
     their domains), so that `enrich-grounding` brings that page up to the current rules;
   - the model lacks it: write it in `domains`, `capabilities`, `features` or `ices`, with
     its id, slug, one_line, parent and `doc` in its folder — a domain at `<domain>/domain.md`,
     a capability at `<folder of its domain's page>/<capability>/capability.md`, a feature at
     `<folder of its capability's page>/<feature>/feature.md` (the parent's page where it will
     be after this run's moves), a part with no parent in its holding folder
     `capabilities/<id>/capability.md` or `features/<id>/feature.md`;
   - the part has no ICE: list its id in `thin`. `enrich-grounding` writes the thin ICE, and
     the play's script writes the two thin marks.
   Nothing the slice needs is skipped.
7. **Name the basis of each choice.** For the surface, the tester, the features and their
   order, write one `decisions` entry: `{question, answer, sources: [{tier, path, start, end}]}`,
   with the lines from `gather` that the choice rests on, or `from_record: <question id>` when
   it rests on a person's answer. The agent records each one with the memory tool.

### Reuse mode

1. Compare the kept slice's features (the spine entry that `serving` names) with the shaped
   slice's features.
2. For each feature the intent needs and the kept slice lacks, add it to `pull_in`. For each
   feature the kept slice holds that serves none of its intents now, add it to `push_out`.
3. The slice must stay testable end to end: its one surface, its tester, and one feature or
   more after the push-outs. When a push-out would leave no feature, do not push it out, and
   say why in `why`.
4. A slice in progress (its id is in `serving` `in_progress`) is never changed: write
   `{pull_in: [], push_out: [], why}` that says a new slice is shaped.
5. Write one `decisions` entry for the reuse, with the spine lines of the kept slice.

### Fix mode

Read each problem. Fix only the field or entry of `slice.json` or `fills.json` that the
problem names: a page outside its folder gets the right `doc`; a part that lacks the intent
gets its update; a thin part that has no Thin mark is listed in `thin`; a slice with two
surfaces keeps one. A problem in a page's text is not this skill's: list it in `not_mine`,
so the agent sends it to `enrich-grounding`. Keep every other field as it is.

## Output

`slice.json` (shape and fix):

```json
{"id": "sl-self-booking", "slug": "self-booking", "name": "Self booking",
 "outcome": "A patient books a free slot with no phone call.",
 "feature_refs": ["ft-pick-a-free-slot", "ft-confirm-a-booking"],
 "vertical": "the booking screen", "intents": ["bi-340"],
 "surface": {"id": "sf-booking-screen", "name": "the booking screen", "persona_ref": "patient",
             "user_action": "picks a free slot and confirms it"},
 "why_this_order": "A patient must pick a slot before the booking can be confirmed.",
 "left_out": [{"what": "Paying for the visit", "why": "The intent is met before any payment."}],
 "decisions": [{"question": "Which surface does the tester use?", "answer": "the booking screen",
                "sources": [{"tier": "garura", "path": "product/product-os/care/booking/capability.md",
                             "start": 12, "end": 14}]}]}
```

`fills.json` (shape and fix): `{domains, capabilities, features, ices, updates, thin}`, the
shape `persist_fills.py` reads; each list may be empty.

`no-slice.json` (shape, only when no surface can be tested end to end): `{reason, looked_at}`.

`reuse.json` (reuse): `{pull_in: [feature ids], push_out: [feature ids], why, decisions}`.

Examples from different fields:
- A clinic: the surface is the booking screen, the tester a patient; the features are pick a
  free slot, then confirm the booking.
- A shop: the surface is the checkout page, the tester a returning shopper; the features are
  keep the cart, then pay with a saved card.
- A build tool: the surface is the `release` command, the tester a release engineer; the
  features are tag the version, then publish the notes.

## Rules

- One surface and one tester (a persona) for each slice. Never a question to the person: the
  brief shows them for the person's yes.
- Every feature the outcome needs is in `feature_refs` or in `fills.json`; nothing the slice
  needs is skipped, and every part has its folder.
- A choice with no source in `gather` or `record` is not made up: when the model and memory
  do not name a surface a person can test end to end, write `no-slice.json`.
- Never change a slice in progress; a reused slice stays testable end to end.
- Never write the spine, a slice record, a model page or the hidden file. The play's scripts
  write them from this skill's files.
- Plain words (ASD-STE100), personas only, no real names.
