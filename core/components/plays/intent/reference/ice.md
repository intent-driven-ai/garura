# intent — ICE source

The clean ICE triple this play is compiled from. Update this and recompile via
play-editor; never hand-edit the compiled SKILL.md.

## Intent

Turn whatever a person shares to explain what they want — a prototype, a deployed site, a
document, or a plain statement — into the person's **Business Intents**, and keep what they
shared as the **Source**, exactly as it was when read:

- **Business Intents** — the person's level: each need the product meets for its user, at the
  level of the product and in its users' words, with why the business needs it, who asks for
  it and how we will know it is met, each confirmed by them. The play drafts all of it from
  what the source shows and what it is for; the person confirms or corrects.

This play writes business intents only (ADR 043). It writes no ICE, no capability and no
domain: `/vision` writes the domains, and `/understand` writes the capabilities and
functionalities with their ICE. Each kind is written on its own and linked later — by the
play that links a part to an intent, or, inside a loop, by the loop's gap skills. Run on its
own, this play leaves the rest of the model to those plays, and the person runs them when they
want it.

The Business Intent and the Source are kinds of the product ontology
(`standards/schemas/product-os/ontology.md`), and the ontology is the hand-off: every play
after this one reads the intents from the product model.

The source is the input, never the intent: an intent must allow more than one way to build
it (IDD Principle 1), and a prototype or a document describing a solution is one way. This
play pulls out what the person wants; it never copies how the source does it.

### Constraints

- C1 — Source accepted: the source is anything that explains the intent — a prototype (a file,
  a project folder, or a deployed solution), a document, or a plain statement. It must be readable at the time of
  the run; a runnable source is also run through, so what it does is seen, not only what it says.
  A prototype is run through **view by view**: the play itself finds every view it offers — each
  tab, button or link that changes what is shown, up to two clicks deep — and keeps each one; a
  view it could not reach is recorded with why. Reading only the first screen of a prototype
  that offers more is not reading it (#613: the Argus mockup's first run saw one screen of six
  sections and drafted intents that missed what Argus does).
- C2 — Each Business Intent carries every required property of its ontology kind — title,
  outcome, why, asked by, proof it is met, stage — and may carry "must not". "Asked by" is a
  persona: a role the product's domain knows and what it does there, the same role across
  the intents one person asks for — never a task or a step in a process. "Proof it is met" is a result
  someone can measure, with a number or a clear yes/no. It is written for a business reader,
  in plain words, readable with no other document open.
- C3 — Outcome, not build: the Business Intent states what should be true for the person, not
  how the source achieves it; no screen-by-screen description, no copied content, no
  implementation detail from the source.
- C4 — Only a person confirms: each Business Intent is written as `proposed` and becomes
  `confirmed` only on the person's typed confirmation of that intent, recorded with who and
  when; the person may drop any intent instead, and a dropped intent is not saved. An agent
  never confirms or drops one. Run by hand, the play asks the person to confirm or drop each
  intent before saving — a pinned gate (class: standard, pinned). Inside a loop there is no approval stop: the loop may still ask its
  questions, but the intents are saved as `proposed`, and the person confirms or drops them at
  the loop's final review (the review and the pull request at its end). Until then no ICE
  built for them is workable.
- C5 — Nothing without a basis: every title, outcome and limit traces to what the source shows,
  to the journeys walked through it, to memory (found through the memory tool, with its
  trace), to what the loop's other plays wrote in the product model, or to the person's own
  answers. Why, asked by and proof are the play's own draft, each with its basis (C17). Where
  nothing can say anything else, the play never fills the gap itself: run by hand it asks the
  person; inside a loop the gap is the loop's question (C16).
- C6 — The Source is kept as it was when read: a snapshot (screenshots and images for a
  deployed solution; a copy of the file for a file or a document; the exact text for a
  statement), with when it was read, what it shows in
  plain words, and who gave it (the git user running the play) — saved through Garura's
  evidence method so it outlives the link or the file.
- C7 — Every confirmed Business Intent and every Source of the run are linked both ways: each
  Source records every intent it shows, and each intent names every Source. The intent page's
  Touches list is written later, by the play that links a part to the intent; this play
  writes none, and on a later round of a loop it keeps a Touches list already on the page.
- C8 — One kind, additive and contained (ADR 043): the run writes only the new Business
  Intents and their Sources. It writes no ICE, no capability, no domain and no spine entry; a
  draft that carries any of them is refused. No existing doc is changed, and no other part of
  the product model changes.
- C9 — Stands alone, or runs inside a loop: run by hand it needs no other play first, and it
  opens and lands its own change; handed a loop's JSON contract — checked by the shared loop-contract checker
  (`check_loop_contract.py`, `standards/rules/loop-contract.md`) — it opens no issue or branch
  of its own, works on the loop's branch, and does not stop for approval. Handed the loop's
  capture (`inputs.intent.capture`, ADR 043), it neither captures nor walks the source again:
  its Sources are the capture's prototype and the person's write-up (each with its source
  manifest), and its journeys are the capture's.
- C10 — The model is the hand-off: each saved Business Intent is a page under
  `<product_base>product-os/intents/<id>.md`, in the ontology's shape, so any later play reads
  it there. No separate hand-off file is written.
- C11 — The play ends by proving its Done means at close: at least one Business Intent and
  every Source exist, every saved intent is confirmed by a person, every intent drafted was
  confirmed or dropped by the person, and the intents and Sources are linked. The close never reads
  COMPLETED with the stop condition unmet.
- C12 — Nothing merged, nothing lost: the play proposes one business intent per need the
  product meets for its user, at the level of the product (C17), never merging two needs and
  never leaving out a part the source shows; every part of the source is mapped to the
  business intent it serves (the coverage map). Asking "why?" once gives the intent's why, not
  a higher intent. The person may add business intents the source does not show (no part maps
  to them). Qualities every intent must keep — fresh, trusted, private — are limits, not
  intents. The person sees the intents and the map before confirming.
- C13 — Questions help the person answer: a question goes to the person only for what nothing
  can draft — never why, asked by or proof (C17) — and comes with up to three example answers
  drawn from the source and the person's words so far; the person's reply is recorded exactly,
  and a reply that picks an example is recorded as picked, so it stays clear who wrote it.
- C14 — The run's short-term memory lives in the issue it works on (ADR 036 §1, ADR 039 §1;
  Kapil, 2026-10-19: "the issue that we are working on is where the short-term memory is going
  to get created. Doesn't matter whether it is drive play or whatnot"). Inside a loop that is
  the contract's `issue`; run by hand it is the issue `start-change` opens or resolves (Step 0).
  The run's working folder is `{stm_base}<issue>/context/intent/<run-ts>/` (inside the issue's
  `context/` key, ADR 017), so the person's answers (`answers.yaml`) are in the issue's
  short-term memory, where the memory tool finds them. Its status and session-stamp markers
  sit at `{stm_base}<issue>/status/`, its sub-play results under
  `{stm_base}<issue>/context/intent/start/` and `…/end/`, and its evidence — the Sources'
  snapshots included — under `{stm_base}<issue>/evidence/intent/`. Run by hand, nothing is
  written to short-term memory before `start-change` gives the issue: what the pre-flight
  records is held in a scratch folder outside `.garura/` and moved into the issue right after
  Step 0, so a pre-flight halt leaves no issue, no branch and no file behind.
- C15 — A prototype is understood by using it (Kapil, 2026-10-20: "it should try to run, create
  journey steps, and understand it, even deeply"). Before drafting, the play walks the prototype
  as the people it serves would: journeys of **who**, what they **set out to do**, each **step**
  and what it showed, and what they **end with** — kept with the Source as evidence. The intents
  are drafted from the main areas and the journeys: each business intent from the need a main
  area of the product meets for a journey's person, and its outcome from the steps that get it. Every
  main section is the goal of a journey of its own (`main_sections`, each journey's `section`). A business intent says what a
  person or the business gets, never a rule the system enforces. Every view the capture kept is
  on a journey, or named as not walked with why. On a deployed site, a step that changes data
  (pay, delete, submit, accept …) is taken only when the person said the site is safe for it;
  on a file or a local prototype nothing real changes, so any step may be taken.
- C16 — Inside a loop, a question `/intent` cannot answer is the **loop's**, not a stop (Kapil,
  2026-10-20: "the question belongs to the whole drive"). First it looks in memory for what
  the product is and who uses it — and drafts a memory update when research can answer
  (ADR 035: used only once a person approves it). What is still open — never why, asked by or
  proof, which it drafts (C17) — it saves as a proposed intent with each gap named as open, writes its open questions for the loop (each with what
  it is about, whether a person must answer it, and example answers), and finishes. On a later
  round of the loop it reads what `/vision` and `/understand` wrote in the product model,
  fills what it can, and updates its own proposed intents — only those this loop saved. It
  never stops the loop to ask; the loop asks the person what no play could answer.
  On a later round the contract's `inputs.intent.targets` names the loop's work for it (a
  screen whose need no intent names, ADR 043): it drafts intents for exactly those.
- C17— The product, at the product's level (Kapil, 2026-10-20, after Kickoff run 7: "you took
  the tool and confused it with the drive work … i gave you the prototype and you still could
  not translate that into intents"). A business intent names a need the product meets for its
  user — one per thing the product offers, following its own main areas, each main section with
  a business intent of its own, never folded into another section's — in the words its
  users would use. The source's sample data is an example of what the product handles: an
  intent holds for any such content and never names the sample's specifics (its company, its
  items, its counts). Any process or tool the screens talk about is content the product shows:
  an intent says what the user gets from the product, never how that process works behind it,
  and never uses the words of the tools that run this play. Why, asked by and proof are drafted by the play, each with its
  basis (provenance `proposed`, or where the source or memory states it, that provenance):
  asked by a persona, why the business reason, proof a measurable result. They are never left
  open and never asked. The test of the result is whether another builder, given only the
  intents and the model, rebuilds what the prototype does (the rebuild eval,
  `core/tools/rebuild-eval`).

### Failure conditions

- F1 — The source could not be read — or, for a runnable source, could not be run through —
  and the play went on anyway; or a prototype was kept from fewer views than it offers: a view
  the play could reach was not kept, or a view it could not reach is not recorded.
- F2 — A Business Intent is missing a required property, or is not readable by a business
  reader (labels, jargon, or a section that does not explain itself).
- F3 — A Business Intent describes the source — screens, fields, copied text, how it
  works — instead of the outcome the person wants.
- F4 — A Business Intent was marked `confirmed` without the person's typed confirmation, or
  by an agent; or, inside a loop, the play stopped to wait for an approval.
- F5 — A title, outcome or limit was filled with something neither the source shows nor the
  person said; or a drafted why, asked by or proof names no basis.
- F6 — A Source has no snapshot, or the snapshot is not saved through the evidence method, or
  it is missing when it was read, what it shows, or who gave it.
- F7 — A confirmed Business Intent and a Source of the run are not linked both ways, or a
  later round dropped a Touches list another play wrote.
- F8 — The run wrote another kind — an ICE, a capability, a domain or a spine entry — or a
  model file other than the new Business Intents and their Sources changed, or an existing doc
  was changed.
- F9 — Run by hand, the change was not opened and landed; or, handed a loop's contract, the
  play opened an issue or a branch of its own.
- F10 — A confirmed Business Intent is missing from the product model, or not in the
  ontology's shape, so a later play cannot read it there.
- F11 — The run closed COMPLETED without the Done means held.
- F12 — Two needs were merged into one business intent, a part of what the source shows is
  mapped to no business intent, or a business intent restates what the source shows instead of
  the need it meets for its user.
- F13 — A question for why or proof was asked with no example answers, or a picked example was
  recorded as the person's own words.
- F14 — The run wrote short-term memory outside its issue's folder: a working file, a person's
  answer, a status marker, a sub-play result or a Source's snapshot under any other folder, or,
  run by hand, anything written to short-term memory before `start-change` gave the issue.
- F15 — A prototype's intents were drafted without walking it in journeys; a journey lacks who,
  what they set out to do, its steps or what they end with; a captured view is neither on a
  journey nor named as not walked; a business intent is a rule the system enforces rather than
  what a person gets; or a step that changes data ran on a deployed site the person had not
  cleared.
- F16 — Inside a loop, `/intent` stopped to ask the person instead of handing its open
  questions to the loop; saved an intent with a gap not named as open; wrote an open question
  without what it is about or example answers; on a later round left open a gap that the
  product model or memory now answers; or changed an intent this loop did not save.
- F17 — A business intent names the process or tools behind the screens instead of a need the
  product meets for its user, or a main section has no business intent of its own (folded into
  another section's), or an intent sits above the product's level, or uses words its users would
  not; "asked by" is not a persona; or why, asked by or proof was left open, asked, or is not
  measurable (proof).

## Context

The Business Intent is the person's interface to the product; the product model and the ICE
built for its parts are the agents' interface (`docs/philosophy/idsd.md`, two interfaces). This
play writes the person's side only. ADR 043 (21 October, after Kickoff run 7) made each Discovery
play write one kind: when `/intent` also drafted the ICE and capabilities, its reading of the
screens flowed into every play after it, and one wrong intent spread to the whole model. Now
`/vision` and `/understand` read the screens for their own kinds, and the links between the
kinds are made later. The drafting judgment sits with the agent for the person's side, because
the person confirms the result. A project folder is two Sources (its written docs and the
running app), and the draft reads both.

The first trial on a real prototype shaped this: a prototype shows what the person must see
and decide, and the person supplied business intents, including one no source showed. Discovery
run 7 (20 October) showed the limit of asking "why?" until the answer leaves the product: the
intents rose into the process behind the screens ("…so waiting work can go on"), left every
proof open, and named the people by their step in a process. Kapil's own version stays at the
product's level — "Able to see the product intents as business needs", asked by "a product
owner defining the intents for a product", proof "business intents are well captured; 90% and
above approved" — so the play drafts at that level (C17).

Short-term memory is created in the issue being worked on, whether the play runs by hand or
inside a loop (C14).

The play reads no memory itself (ADR 039 §2). It hands `business-intent-keeper` the issue and
the ontology by its name in memory — the config's `product.ontology` — and the agent reads the
ontology through the memory tool, copies it into the run's short-term memory for
`author-business-intent`, and records what it read with `cite`. The close gets its templates
from the `template-manager` agent (the shared close, `_shared/play-close.md`), never by a path
in memory.

## Expectation

### Success scenarios

- S1 — (business owner, from a deployed prototype) Given a deployed site that shows what they
  want, when `/intent` runs and the person confirms, then each confirmed Business Intent and
  the Source exist, linked both ways, and the change is landed. Measure: the intent manifest
  reads `decided: true` and `stage: confirmed`, each saved intent has `confirmed_by` set
  and every required property present; the Source manifest lists a screenshot and the text of
  every view the prototype offers (`views.kept` equals `views.found`, or each one missed is in
  `views.unreached` with why) under
  the evidence folder; the intent manifest reads `linked: true`; the scoped guard reads ok;
  merge-change reports the PR merged.
- S2 — (founder, from a plain statement) Given only a written statement of what they want,
  when `/intent` runs and the person confirms, then the Source's snapshot is the exact text of
  the statement and each Business Intent states its outcome without repeating the statement
  word for word. Measure: the Source manifest reads `kind: statement` and its snapshot file
  matches the statement byte for byte; the outcome-not-build check passes on the intent.
- S3 — (business owner, nothing without a basis) Given a source that does not say who asked,
  why, or how we will know, when `/intent` runs, then the play drafts each with its basis and
  asks no question for them, and every property records where it came from. Measure: every
  saved intent gives every property a provenance of `source`, `journey`, `memory`, `model`,
  `person` or `proposed`; each `proposed` one has its basis; none is empty, `open` or `agent`;
  the intent check reads no question for why, asked by or proof.
- S4 — (business owner, does not confirm) Given the person drops every drafted intent or
  stops, when the run reaches confirmation, then nothing is saved as confirmed and no model
  change is committed. Measure: no Business Intent file is committed; the working tree's model
  paths are clean; the run closes HALTED with the reason recorded.
- S5 — (Discovery loop, inside a loop) Given a loop hands `/intent` its JSON contract, when it
  runs, then it opens no issue or branch of its own and writes on the loop's branch. Measure:
  the run record shows `in_loop: true`, no start-change or end-sequence step ran, the current
  branch equals the contract's branch, no confirmation step ran, every saved intent reads
  `proposed`, and it wrote no capability, domain or spine entry.
- S6 — (product strategist, hand-over through the model) Given a confirmed Business Intent,
  when the run ends, then a later play finds it in the product model. Measure: each saved
  intent is a page under `product-os/intents/` in the ontology's shape; the run wrote no spine,
  no capability page and no domain page; no hand-off file is written.
- S7 — (business owner, a prototype that does several things) Given a prototype that meets
  several separate needs, when `/intent` runs, then the draft holds one business intent per
  need, every part of the source maps to one, and the person confirms or drops each. Measure:
  the coverage map names every part and an existing intent for each; every intent no part maps
  to was stated by the person; the confirmation holds a decision per intent.
- S8 — (business owner, answering a question) Given open questions — about anything but why,
  asked by and proof — when the play asks them, then each comes with example answers, and the record shows which replies picked an
  example. Measure: every answer in the answers record lists the examples offered, and every
  reply that matches an offered example is marked picked.
- S9 — (product owner, a prototype with many views) Given a working prototype that offers many
  views and flows, when `/intent` runs, then it walks the prototype in journeys before drafting,
  every view the capture kept is on a journey or named as not walked, and each business intent
  traces to what a journey's person sets out to get. Measure: `journeys-check.json` reads
  `ok: true`; every business intent in the draft names the journey it came from.
- S10 — (Discovery loop, a gap only the loop can fill) Given a prototype that shows who uses it but
  not the product's domain, when `/intent` runs inside a loop, then it saves
  its intents as proposed with the gaps named, writes its open questions for the loop, and
  does not stop; on the next round it fills what `/vision` and `/understand` made known.
  Measure: round 1's `open-intent.json` lists every gap; no question was put to a person by
  `/intent`; round 2's intent pages fill at least one gap round 1 left open, and every filled
  property's provenance is `source`, `journey`, `memory`, `model`, `person` or `proposed`.
- S11 — (product owner, a prototype rebuilt from its intents) Given a working prototype, when
  `/intent` runs, then each business intent names a need the product meets for its user, in its
  users' words, with a persona, a business why and a measurable proof. Measure: the rebuild
  eval's static check reads no `intent-field` or `intent-proof-open` finding, and its review
  reads every intent test passed (`need_the_product_offers`, `outcome`, `asked_by_persona`,
  `why_business`, `proof_measurable`, `product_words`).

### Done means

Paths are relative to the run's working folder (`<working>`, under
`{stm_base}<issue>/context/intent/<run-ts>/`, inside the issue being worked on). `intent-manifest.json` is written when the confirmed
Business Intents are saved, and rolls up every Source of the run; `guard-report.json` is the
captured scoped-write guard output.

- D1 — says: "the Business Intents were saved"
  check: { type: artifact_exists, path: "intent-manifest.json" }
- D2 — says: "run by hand, a person confirmed at least one and decided every one drafted; inside a
  loop, every drafted intent was saved as proposed for the loop's final review"
  check: { type: field_equals, file: "intent-manifest.json", field: "decided", equals: true }
- D3 — says: "every Source was saved with a snapshot"
  check: { type: field_equals, file: "intent-manifest.json", field: "sources_saved", equals: true }
- D4 — says: "the intents and their Sources are linked both ways"
  check: { type: field_equals, file: "intent-manifest.json", field: "linked", equals: true }
- D5 — says: "nothing else in the product model changed"
  check: { type: field_equals, file: "guard-report.json", field: "ok", equals: true }

### Recovery (one per failure condition)

- REC1 (F1) — trigger: the source could not be read or run through, or a prototype was kept
  from fewer views than it offers. direction: halt and tell the person exactly what could not be
  opened, and ask for a readable copy or a working link; for missing views, capture again with
  every view found, and name to the person each view that still cannot be reached. handoff:
  human.
- REC2 (F2) — trigger: a required property is missing, or a section does not read for a
  business reader. direction: ask the person for the missing property; rewrite the unclear
  section in plain words; re-check before confirmation. handoff: autonomous.
- REC3 (F3) — trigger: the intent describes the source instead of the outcome. direction:
  strip the description and restate the outcome the person wants; re-check. handoff: autonomous.
- REC4 (F4) — trigger: the intent was marked confirmed without the person's typed yes, or by an
  agent, or the play waited for approval inside a loop. direction: reset the stage to
  proposed; by hand, present it to the person and record only their own confirmation; inside a
  loop, save it as proposed and move on — the loop's final review confirms it. handoff: human.
- REC5 (F5) — trigger: a title, outcome or limit has no provenance in the source or the
  person's answers, or a drafted property names no basis. direction: remove the title,
  outcome or limit and ask the person for it; give the drafted property its basis or redraft
  it from one. handoff: human.
- REC6 (F6) — trigger: the Source has no snapshot, is not saved through the evidence method, or
  is missing when it was read, what it shows, or who gave it. direction: take the snapshot again
  and re-save it through the evidence method with every field before the close. handoff: autonomous.
- REC7 (F7) — trigger: an intent and a Source are not linked both ways, or a later round
  dropped a Touches list. direction: write the missing link on whichever side lacks it, and
  restore the Touches list from the page as it was — through the save script. handoff:
  autonomous.
- REC8 (F8) — trigger: the run wrote another kind, a model path outside the run's scope
  changed, or an existing doc was changed. direction: drop the other kind from the draft (the
  play that owns it writes it); the guard's restore reverts the offending paths; re-write only
  the run's own records, after a human confirms the restore. handoff: human.
- REC9 (F9) — trigger: run by hand without opening or landing its change, or opened its own
  issue or branch inside a loop. direction: by hand, run the missing opening or end-sequence
  step; inside a loop, close the stray issue and branch and continue on the loop's branch.
  handoff: human.
- REC10 (F10) — trigger: an intent is not in the product model in the ontology's shape.
  direction: re-write the missing or misshapen page from the confirmed draft. handoff:
  autonomous.
- REC11 (F11) — trigger: the close would read COMPLETED with the Done means unmet. direction:
  close HALTED with the unmet clauses named; fix the state and re-evaluate. handoff: autonomous.
- REC12 (F12) — trigger: two needs share one intent, a part maps to no intent, or an intent
  restates the source. direction: re-draft with the problem named — one intent per need, every
  part mapped; ask "why?" once for an intent that restates the source; at confirmation the
  person can name a missing or merged intent and the play re-drafts. handoff: autonomous.
- REC13 (F13) — trigger: a question went out with no examples, or a picked example was recorded
  as the person's words. direction: ask again with examples; mark the picked reply as picked.
  handoff: autonomous.
- REC14 (F14) — trigger: a working file, an answer, a marker, a sub-play result or a snapshot
  sits outside `{stm_base}<issue>/`, or something was written to short-term memory before Step 0
  gave the issue. direction: move it into the issue's working folder (or status or evidence
  folder), delete the stray copy, and continue; when the issue is not known yet, hold it in the
  scratch folder until Step 0. handoff: autonomous.

- REC15 (F15) — trigger: the intents were drafted without journeys, a journey is incomplete, a
  view is on no journey and not named, a business intent is a rule rather than what a person
  gets, or a data-changing step ran on a deployed site not cleared. direction: walk the missing
  journeys (or name each view not walked, with why), redraft the business intents from the
  journeys' goals; for a deployed site, ask the person whether a data-changing step is safe
  before taking it. handoff: autonomous.

- REC16 (F16) — trigger: inside a loop `/intent` stopped to ask, saved an unnamed gap, wrote an
  open question without its context, left a gap the model or memory now answers, or changed an
  intent this loop did not save. direction: hand the questions to the loop instead; name
  every gap as open with its question; on the next round re-read the model and memory and fill
  what they answer; restore any intent this loop did not save. handoff: autonomous.

- REC17 (F17) — trigger: an intent names the process or tools behind the screens, sits above
  the product's level, or uses words its users would not; asked by is not a persona; or why,
  asked by or proof is open, asked or not measurable. direction: redraft the intent from the
  product's main area and the journey it serves, in its users' words; draft asked by, why and
  proof with their basis; drop the question. handoff: autonomous.
