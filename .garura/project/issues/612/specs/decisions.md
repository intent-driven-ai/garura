# #612 — decisions

Kapil answered plan item 1 on 2026-10-08 (taken as approval of the plan):

**D1 — The confirmed intent lives in the product model.** It is a new kind of record there, and it is the **first piece of the product ontology** (#597) — built together with Kapil now, as the start of that ontology.

**D2 — A prototype is anything you can run through:** a single file on disk, or a deployed solution (a link). `/intent` runs through it to read how it behaves.

**D3 — Handoff is a JSON contract.** Garura's rule: components pass a JSON contract to each other. A drive dispatches `/intent` with a JSON contract (as plays already dispatch sub-plays with `parent_run_id`); with that contract, `/intent` skips opening its own issue and branch. Run by hand, with no contract, it opens and lands its own change.

**D4 — What `/intent` creates is a Business Intent, and it is human-facing.** It is the person's outcome, written to be read by a person — not an ICE-shaped list of goal / constraints / failures. It is one kind of thing in the product ontology, which Kapil and Claude build together from here, step by step (Kapil has not built an ontology before). Kapil, 2026-10-08.

**D5 — A source is anything that explains the intent** (widens D2). A prototype (a file or a deployed solution), a document, or a plain statement. A runnable source is also run through. Kapil, 2026-10-08, approving `/intent`'s intent source.

## D6 — Two levels: business intents above, ICE below (2026-10-09)

**Decided by:** Kapil, after the trial.
A source shows what the person must see and decide; that is ICE, the agents' level, already
in the ontology. The business intents sit one "why?" above and mostly come from the person.
`/intent` drafts both and saves both. The ontology is the hand-off: no separate file for
`/vision`.

## D7 — No play owns a kind; alignment fixes drift (2026-10-09)

**Decided by:** Kapil: "nothing is waiting.. we can find an intent and ICE while implementation
and later we will align the drift.. there is no rule who writes ICE or any part of ontology.
anyone can write.. that will be its own drive."
Ontology rules say what holds once aligned and never block a write. ICE may exist before it is
placed under a capability. Only a person confirms or drops a business intent. The Alignment
drive is its own drive (not yet filed).

## D8 — ICE is placed at once, on a proposed capability; the domain comes later (2026-10-09)

**Decided by:** Kapil, on review of PR #631 — "why would we have ICE that is not placed?";
"intent doesn't need domain... domain can be added / attached later. isn't vision responsible
for attaching domain?"
`/intent` writes each ICE as a proposed capability: a spine entry (status proposed, detail
directional, no domain yet, `intents` naming its business intent) and a capability grounding
doc with the ICE inline — no separate ICE file (spine v2 retired them). `/vision` attaches the
domain. A missing domain is a linter warning, not an error; a named domain that does not exist
stays an error.

## D9 — ICE is workable only with a confirmed business intent; writes are never blocked (2026-10-09)

**Decided by:** Kapil — "without a bint, there is no need to work on ICE"; "our principle is also
to not introduce blocks.. even if ice is written, it need to be captured, and marked in a way
where it cant be processed."
Any play may write an ICE. It is workable only when its node's spine `intents` names a
confirmed business intent; otherwise it is kept but no play plans, breaks down or builds from
it. Worked out from the link (`check_ice_workable.py`), not a separate status field.


## D10 — No approval stop inside a drive; the drive's end is the review (2026-10-09)

**Decided by:** Kapil — "no stop... drive can ask questions, but no need to approve. the last
steps of a drive is where validation final review happens - that is the review, pr etc."
Inside a drive `/intent` asks its questions but does not wait for approval: every drafted intent
is saved as `proposed`, and the person confirms or drops it at the drive's final review. Until
then its ICE is not workable (D9). Run by hand, `/intent` still asks for confirmation first.

Note on D9 (2026-10-09, review round 2): an intent whose proof now holds (`met`) was confirmed
first, so its ICE stays workable — work that keeps it met is still wanted. Only proposed,
dropped or missing intents leave an ICE not workable.
