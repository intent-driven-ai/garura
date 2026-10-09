# intent — ICE source

The clean ICE triple this play is compiled from. Update this and recompile via
play-editor; never hand-edit the compiled SKILL.md.

## Intent

Turn whatever a person shares to explain what they want — a prototype, a deployed site, a
document, or a plain statement — into two levels of intent, and keep what they shared as the
**Source**, exactly as it was when read:

- **Business Intents** — the person's level: what they want for the business, in their own
  words, with why it matters and how we will know it is met, each confirmed by them. A source
  rarely shows these directly; they sit above what it shows and mostly come from the person.
- **ICE** — the agents' level, under each business intent: the separate things a person must
  be able to see, decide or do to meet it, as ICE goals. This is what a source shows best.
  Each ICE is written as a proposed capability: its ICE inline in the capability's grounding
  doc, its spine entry naming the business intent it is built from, and no domain yet.

All three are kinds of the product ontology (`standards/schemas/product-os/ontology.md`), and
the ontology is the hand-off: every play after this one reads the intents and their ICE from
the product model. No play owns a kind and nothing waits for another play — `/vision`
attaches the capabilities to domains and adds to them, and drift is fixed by alignment.

The source is the input, never the intent: an intent must allow more than one way to build
it (IDD Principle 1), and a prototype or a document describing a solution is one way. This
play pulls out what the person wants; it never copies how the source does it.

### Constraints

- C1 — Source accepted: the source is anything that explains the intent — a prototype (a file,
  a project folder, or a deployed solution), a document, or a plain statement. It must be readable at the time of
  the run; a runnable source is also run through, so what it does is seen, not only what it says.
- C2 — Each Business Intent carries every required property of its ontology kind — title,
  outcome, why, asked by, proof it is met, stage — and may carry "must not". It is written for
  a business reader, in plain words, readable with no other document open.
- C3 — Outcome, not build: the Business Intent states what should be true for the person, not
  how the source achieves it; no screen-by-screen description, no copied content, no
  implementation detail from the source.
- C4 — Only a person confirms: each Business Intent is written as `proposed`, shown to the
  person, and becomes `confirmed` only on their typed confirmation of that intent, recorded
  with who and when. The person may drop any intent instead; a dropped intent is not saved.
  An agent never confirms or drops one.
- C5 — Nothing invented: every outcome, reason, proof and limit traces either to what the
  source shows or to the person's own answers; where the source cannot say (who asked, why,
  how we will know), the play asks the person and never fills the gap itself.
- C6 — The Source is kept as it was when read: a snapshot (screenshots and images for a
  deployed solution; a copy of the file for a file or a document; the exact text for a
  statement), with when it was read, what it shows in
  plain words, and who gave it (the git user running the play) — saved through Garura's
  evidence method so it outlives the link or the file.
- C7 — Every confirmed Business Intent and every Source of the run are linked: each Source
  records every intent it shows, and each intent names every Source. Every ICE's capability
  names, in the spine, the business intent it is built from, and each intent names its
  capabilities.
- C8 — Additive and contained: the run writes only the new Business Intents, their ICE (as
  new proposed capability entries added to the spine, each with its grounding doc) and their
  Sources; no existing entry or doc is changed, and no other part of the product model
  changes.
- C9 — Stands alone, or runs inside a drive: run by hand it needs no other play first, and it
  opens and lands its own change; handed a drive's JSON contract, it opens no issue or branch
  of its own and works on the drive's branch.
- C10 — The model is the hand-off: each confirmed Business Intent and its ICE are saved in the
  product model in the ontology's shapes — the ICE inline in a proposed capability's grounding
  doc, the capability's spine entry naming its intent and leaving its domain for `/vision` —
  so any later play reads them there. No separate hand-off file is written.
- C11 — The play ends by proving its Done means at close: at least one Business Intent and
  every Source exist, every saved intent is confirmed by a person, every intent drafted was
  confirmed or dropped by the person, and the intents and Sources are linked. The close never reads
  COMPLETED with the stop condition unmet.
- C12 — Two levels, nothing merged, nothing lost: the play drafts each separate thing the
  source lets the person see, decide or do as its own ICE, never merging separate things and
  never leaving out a part the source shows; every part is mapped to its ICE. Above them it
  proposes the business intents they serve, found by asking "why?" one level at a time and
  stopping when the answer no longer names the product; each ICE is built from one of them.
  The person may add business intents the source does not show (they start with no ICE).
  Qualities every intent must keep — fresh, trusted, private — are limits, not intents. The
  person sees both levels and the map before confirming.
- C13 — Questions help the person answer: each question for why or proof comes with up to
  three example answers drawn from the source and the person's words so far; the person's
  reply is recorded exactly, and a reply that picks an example is recorded as picked, so it
  stays clear who wrote it.

### Failure conditions

- F1 — The source could not be read — or, for a runnable source, could not be run through —
  and the play went on anyway.
- F2 — A Business Intent is missing a required property, or is not readable by a business
  reader (labels, jargon, or a section that does not explain itself).
- F3 — A Business Intent describes the source — screens, fields, copied text, how it
  works — instead of the outcome the person wants.
- F4 — A Business Intent was marked `confirmed` without the person's typed confirmation, or
  by an agent.
- F5 — A property was filled with something neither the source shows nor the person said.
- F6 — A Source has no snapshot, or the snapshot is not saved through the evidence method, or
  it is missing when it was read, what it shows, or who gave it.
- F7 — A confirmed Business Intent and a Source of the run are not linked both ways.
- F8 — A model file other than the new Business Intents and their Sources changed during the run.
- F9 — Run by hand, the change was not opened and landed; or, handed a drive's contract, the
  play opened an issue or a branch of its own.
- F10 — A confirmed Business Intent or its ICE is missing from the product model, or not in
  the ontology's shape, so a later play cannot read it there.
- F11 — The run closed COMPLETED without the Done means held.
- F12 — Separate things the person must see or decide were merged into one ICE, a part of
  what the source shows is mapped to no ICE, an ICE is built from no business intent, or a
  business intent restates what the source shows instead of what the person wants for the
  business.
- F13 — A question for why or proof was asked with no example answers, or a picked example was
  recorded as the person's own words.

## Context

The Business Intent is the person's interface to the product; the product model and the ICE
built from it are the agents' interface (`docs/philosophy/idsd.md`, two interfaces). This play
is where the two meet: it drafts both levels from one reading of the source, so the link from
each ICE to the intent it serves is made at the moment both are known. The drafting judgment
sits with the agent for the person's side, because the person confirms the result. No play
owns a kind (ontology v3): this play writes capabilities without a domain, and `/vision`
attaches the domain and adds to them; drift is fixed by alignment, not by holding work back.
An ICE is workable only when built from a confirmed business intent, which this play's
confirmation step provides. A project folder is two Sources (its written
docs and the running app), and the draft reads both.

The first trial on a real prototype shaped this: a prototype shows what the person must see
and decide; the business intents sit one "why?" above, and the person supplied them,
including one no source showed. Example answers helped the person answer why and proof.

## Expectation

### Success scenarios

- S1 — (business owner, from a deployed prototype) Given a deployed site that shows what they
  want, when `/intent` runs and the person confirms, then each confirmed Business Intent and
  the Source exist, linked both ways, and the change is landed. Measure: the intent manifest
  reads `any_confirmed: true` and `all_decided: true`, each saved intent has `confirmed_by` set
  and every required property present; the Source manifest lists at least one screenshot under
  the evidence folder; the intent manifest reads `linked: true`; the scoped guard reads ok;
  merge-change reports the PR merged.
- S2 — (founder, from a plain statement) Given only a written statement of what they want,
  when `/intent` runs and the person confirms, then the Source's snapshot is the exact text of
  the statement and each Business Intent states its outcome without repeating the statement
  word for word. Measure: the Source manifest reads `kind: statement` and its snapshot file
  matches the statement byte for byte; the outcome-not-build check passes on the intent.
- S3 — (business owner, nothing invented) Given a source that does not say who asked, why, or
  how we will know, when `/intent` runs, then the play asks the person for each, and every
  property records where it came from. Measure: every saved intent gives every property a
  provenance of `source` or `person`, and none is empty or `agent`.
- S4 — (business owner, does not confirm) Given the person drops every drafted intent or
  stops, when the run reaches confirmation, then nothing is saved as confirmed and no model
  change is committed. Measure: no Business Intent file is committed; the working tree's model
  paths are clean; the run closes HALTED with the reason recorded.
- S5 — (Kickoff drive, inside a drive) Given a drive hands `/intent` its JSON contract, when it
  runs, then it opens no issue or branch of its own and writes on the drive's branch. Measure:
  the run record shows `in_drive: true`, no start-change or end-sequence step ran, and the
  current branch equals the contract's branch.
- S6 — (product strategist, hand-over through the model) Given a confirmed Business Intent with
  ICE under it, when the run ends, then a later play finds both in the product model. Measure:
  each ICE is a spine capability entry — status proposed, detail directional, domain empty,
  `intents` naming its business intent — with a capability grounding doc that passes the
  grounding linter (no error; "no domain yet" is the only warning); each intent page names its
  capabilities; the workable check reads every one of them as workable; no hand-off file is
  written.
- S7 — (business owner, a prototype that does several things) Given a prototype that lets the
  person see and decide several separate things, when `/intent` runs, then the draft holds one
  ICE per separate thing, each built from a business intent above it, every part of the source
  maps to an ICE, and the person confirms or drops each business intent. Measure: the coverage
  map names every part and an existing ICE for each; every ICE names an existing intent; every
  intent with no ICE was stated by the person; the confirmation holds a decision per intent.
- S8 — (business owner, answering why and proof) Given open questions, when the play asks
  them, then each comes with example answers, and the record shows which replies picked an
  example. Measure: every answer in the answers record lists the examples offered, and every
  reply that matches an offered example is marked picked.

### Done means

Paths are relative to the run's working folder (`<working>`, under
`{stm_base}_kickoff/intent/<run-ts>/`). `intent-manifest.json` is written when the confirmed
Business Intents are saved, and rolls up every Source of the run; `guard-report.json` is the
captured scoped-write guard output.

- D1 — says: "the Business Intents were saved"
  check: { type: artifact_exists, path: "intent-manifest.json" }
- D2 — says: "a person confirmed at least one, and decided every one drafted"
  check: { type: field_equals, file: "intent-manifest.json", field: "confirmed_and_decided", equals: true }
- D3 — says: "every Source was saved with a snapshot"
  check: { type: field_equals, file: "intent-manifest.json", field: "sources_saved", equals: true }
- D4 — says: "the intents, their ICE and their Sources are linked"
  check: { type: field_equals, file: "intent-manifest.json", field: "linked", equals: true }
- D5 — says: "nothing else in the product model changed"
  check: { type: field_equals, file: "guard-report.json", field: "ok", equals: true }

### Recovery (one per failure condition)

- REC1 (F1) — trigger: the source could not be read or run through. direction: halt and tell
  the person exactly what could not be opened; ask for a readable copy or a working link.
  handoff: human.
- REC2 (F2) — trigger: a required property is missing, or a section does not read for a
  business reader. direction: ask the person for the missing property; rewrite the unclear
  section in plain words; re-check before confirmation. handoff: autonomous.
- REC3 (F3) — trigger: the intent describes the source instead of the outcome. direction:
  strip the description and restate the outcome the person wants; re-check. handoff: autonomous.
- REC4 (F4) — trigger: the intent was marked confirmed without the person's typed yes, or by an
  agent. direction: reset the stage to proposed, present it to the person, and record only their
  own confirmation. handoff: human.
- REC5 (F5) — trigger: a property has no provenance in the source or the person's answers.
  direction: remove it and ask the person for it. handoff: human.
- REC6 (F6) — trigger: the Source has no snapshot, is not saved through the evidence method, or
  is missing when it was read, what it shows, or who gave it. direction: take the snapshot again
  and re-save it through the evidence method with every field before the close. handoff: autonomous.
- REC7 (F7) — trigger: an intent and a Source are not linked both ways. direction: write the
  missing link on whichever side lacks it. handoff: autonomous.
- REC8 (F8) — trigger: a model path outside the new intent and source changed. direction: the
  guard's restore reverts the offending paths; re-write only the intent and source, after a
  human confirms the restore. handoff: human.
- REC9 (F9) — trigger: run by hand without opening or landing its change, or opened its own
  issue or branch inside a drive. direction: by hand, run the missing opening or end-sequence
  step; inside a drive, close the stray issue and branch and continue on the drive's branch.
  handoff: human.
- REC10 (F10) — trigger: an intent or its ICE is not in the product model in the ontology's
  shape. direction: re-write the missing or misshapen record from the confirmed draft.
  handoff: autonomous.
- REC11 (F11) — trigger: the close would read COMPLETED with the Done means unmet. direction:
  close HALTED with the unmet clauses named; fix the state and re-evaluate. handoff: autonomous.
- REC12 (F12) — trigger: two separate things share one ICE, a part maps to no ICE, an ICE has no
  business intent, or a business intent restates the source. direction: re-draft with the
  problem named — one ICE per separate thing, each built from an intent; ask "why?" again for
  an intent that restates the source; at confirmation the person can name a missing or merged
  item and the play re-drafts. handoff: autonomous.
- REC13 (F13) — trigger: a question went out with no examples, or a picked example was recorded
  as the person's words. direction: ask again with examples; mark the picked reply as picked.
  handoff: autonomous.
