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
  Each ICE is written as a proposed capability in the one product model: its ICE in the
  capability page's `## Agent intent (ICE)` section, its spine entry naming the business
  intent it is built from. When the play can tell which domain the capability belongs to —
  from the source, the person's words, or a domain already in the model — the capability
  goes under that domain, and a domain not yet in the model is added as a light
  (directional) domain page; when it cannot tell, the capability waits in the holding
  folder with no domain.

All three are kinds of the product ontology (`standards/schemas/product-os/ontology.md`), and
the ontology is the hand-off: every play after this one reads the intents and their ICE from
the product model. One model, written at the depth that is known: no play owns a kind and
nothing waits for another play — `/vision` places what is still in the holding folder, raises
light domain pages and adds to the capabilities, and drift is fixed by alignment. Each part an
intent touches is linked both ways: the part's spine entry names the intent, and the intent
page's Touches list names the part, marked adds or changes.

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
- C4 — Only a person confirms: each Business Intent is written as `proposed` and becomes
  `confirmed` only on the person's typed confirmation of that intent, recorded with who and
  when; the person may drop any intent instead, and a dropped intent is not saved. An agent
  never confirms or drops one. Run by hand, the play asks the person to confirm or drop each
  intent before saving — a pinned gate (class: standard, pinned). Inside a drive there is no approval stop: the drive may still ask its
  questions, but the intents are saved as `proposed`, and the person confirms or drops them at
  the drive's final review (the review and the pull request at its end). Until then their ICE
  is not workable.
- C5 — Nothing invented: every outcome, reason, proof and limit traces either to what the
  source shows or to the person's own answers; where the source cannot say (who asked, why,
  how we will know), the play asks the person and never fills the gap itself.
- C6 — The Source is kept as it was when read: a snapshot (screenshots and images for a
  deployed solution; a copy of the file for a file or a document; the exact text for a
  statement), with when it was read, what it shows in
  plain words, and who gave it (the git user running the play) — saved through Garura's
  evidence method so it outlives the link or the file.
- C7 — Every confirmed Business Intent and every Source of the run are linked: each Source
  records every intent it shows, and each intent names every Source. Every part an intent
  touches is linked both ways: each ICE's capability — and the domain it is placed under —
  names the intent in its spine `intents`, and the intent page's Touches list names each of
  them, marked `adds` (written by this run) or `changes` (already in the model), with a link
  to its page. The Touches list is written by the save script, never by hand.
- C8 — Additive and contained: the run writes only the new Business Intents, their ICE (as
  new proposed capability entries added to the spine, each with its grounding doc), the light
  domain entry and page for a domain not yet in the model, and their Sources. On a domain
  already in the model it only adds the intent to the domain's spine `intents`; no existing
  doc is changed, and no other part of the product model changes.
- C9 — Stands alone, or runs inside a drive: run by hand it needs no other play first, and it
  opens and lands its own change; handed a drive's JSON contract, it opens no issue or branch
  of its own, works on the drive's branch, and does not stop for approval.
- C10 — The model is the hand-off: each confirmed Business Intent and its ICE are saved in the
  product model in the ontology's shapes — the ICE in the `## Agent intent (ICE)` section of a
  proposed, directional capability page, the capability's spine entry naming its intent, under
  its domain at `<domain>/<capability>/capability.md` when the domain is known (a new domain
  as a light, directional page: `# Theme:` and `## Intent`), else in the holding folder
  `capabilities/<capability>/capability.md` with its domain left for `/vision` — so any later
  play reads them there. A domain is never invented to avoid the holding folder: it is named
  only when the source, the person, or the model shows it. No separate hand-off file is
  written.
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
  by an agent; or, inside a drive, the play stopped to wait for an approval.
- F5 — A property was filled with something neither the source shows nor the person said.
- F6 — A Source has no snapshot, or the snapshot is not saved through the evidence method, or
  it is missing when it was read, what it shows, or who gave it.
- F7 — A confirmed Business Intent and a Source of the run are not linked both ways, or a part
  the intent touches is not linked both ways (spine `intents` and the intent page's Touches
  list).
- F8 — A model file other than the new Business Intents, their capabilities, the light pages of
  new domains, the spine, and their Sources changed during the run, or an existing doc was
  changed.
- F9 — Run by hand, the change was not opened and landed; or, handed a drive's contract, the
  play opened an issue or a branch of its own.
- F10 — A confirmed Business Intent or its ICE is missing from the product model, or not in
  the ontology's shape (the ICE outside its named section, a capability under a domain that
  is not in the spine), so a later play cannot read it there; or a domain was named that
  neither the source, the person, nor the model shows.
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
owns a kind (ontology v3–v4): this play writes capabilities under the domain it can tell, or
without one when it cannot, and `/vision` places them, raises the light domain pages and adds
to them; drift is fixed by alignment, not by holding work back.
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
  reads `decided: true` and `stage: confirmed`, each saved intent has `confirmed_by` set
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
  the run record shows `in_drive: true`, no start-change or end-sequence step ran, the current
  branch equals the contract's branch, no confirmation step ran, every saved intent reads
  `proposed`, and the workable check reads every capability it wrote as not workable.
- S6 — (product strategist, hand-over through the model) Given a confirmed Business Intent with
  ICE under it, when the run ends, then a later play finds both in the product model. Measure:
  each ICE is a spine capability entry — status proposed, detail directional, `intents` naming
  its business intent, and either `domain` naming a domain in the spine (its page under that
  domain's folder) or empty (its page in the holding folder) — with a capability page whose
  last section is `## Agent intent (ICE)`; a domain this run added is a spine entry with
  `detail: directional` and a light page; the grounding linter passes with the spine (no
  error; "no domain yet" is the only warning); each intent page's Touches list names every
  capability and domain built from or linked to it, each with its mark, and each of those
  names the intent in its spine `intents`; run by hand, the workable check reads every
  capability as workable (inside a drive, none until the person confirms at the drive's final
  review); no hand-off file is written.
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
- D2 — says: "run by hand, a person confirmed at least one and decided every one drafted; inside a
  drive, every drafted intent was saved as proposed for the drive's final review"
  check: { type: field_equals, file: "intent-manifest.json", field: "decided", equals: true }
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
  agent, or the play waited for approval inside a drive. direction: reset the stage to
  proposed; by hand, present it to the person and record only their own confirmation; inside a
  drive, save it as proposed and move on — the drive's final review confirms it. handoff: human.
- REC5 (F5) — trigger: a property has no provenance in the source or the person's answers.
  direction: remove it and ask the person for it. handoff: human.
- REC6 (F6) — trigger: the Source has no snapshot, is not saved through the evidence method, or
  is missing when it was read, what it shows, or who gave it. direction: take the snapshot again
  and re-save it through the evidence method with every field before the close. handoff: autonomous.
- REC7 (F7) — trigger: an intent and a Source, or an intent and a part it touches, are not
  linked both ways. direction: write the missing link on whichever side lacks it — through the
  save script for the Touches list and the spine `intents`. handoff: autonomous.
- REC8 (F8) — trigger: a model path outside the run's scope changed, or an existing doc was
  changed. direction: the guard's restore reverts the offending paths; re-write only the
  run's own records, after a human confirms the restore. handoff: human.
- REC9 (F9) — trigger: run by hand without opening or landing its change, or opened its own
  issue or branch inside a drive. direction: by hand, run the missing opening or end-sequence
  step; inside a drive, close the stray issue and branch and continue on the drive's branch.
  handoff: human.
- REC10 (F10) — trigger: an intent or its ICE is not in the product model in the ontology's
  shape, or a domain was named with nothing to show it. direction: re-write the missing or
  misshapen record from the confirmed draft; drop a domain nothing shows and put its
  capabilities in the holding folder. handoff: autonomous.
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
