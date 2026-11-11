# BI-6 (Run → Product): what Garura has for learning from use, and what is pending

Research only, 2026-11-10, for #1021 (the chore that reorganises Garura's business intents around the phases and their
transitions). Nothing under `.garura/product/`, on GitHub or in git was changed.

Scope: BI-6 only. By the product owner's rule of 2026-11-08 ("the work we are doing are based on where the phase
ends"), BI-6 holds what ends in the product: its intents, its model and its memory, kept true to what happened in use.

## In one paragraph

Nothing live in Garura learns from use. No part takes in what happened once a product runs, sets it against an
intent's proof, marks an intent met, or moves a learning up into Garura memory or Phoenix memory. Garura never touches
production and reads nothing from it, and BI-5, which would carry work to pre-production and record people's
acceptance, is parked with nothing built. So today "what happens in use" can reach Garura only as people's own words
(an issue, a comment, an answer in a session) and as the records Garura's own runs leave in short-term memory, and
nothing reads either as a signal on an intent. The one play built for this, /learn-outcomes, is stale: every input it
reads is gone or stale, and the model updates it made are now claimed by BI-1's approved Keep the spec matched, which
also finds drift between the spec and what agents built, the substance of BI-6's first proof. Memory has a working
front half (an agent raises a memory update, a person approves it, the tool writes it into the issue's short-term
memory), but nothing promotes it, and every promotion to Phoenix memory so far was a hand copy outside the change
plays. What only BI-6 can hold is comparing what happened in use with what was intended, judging when an intent is
met, and choosing which learnings to promote.

## Words used here

- **Play**: a slash command that runs a fixed workflow, with a person's yes at its checkpoint. **Agent** (sub-agent):
  gathers context and calls skills. **Skill**: does one piece of work and writes a file. **Tool**: a script Garura
  installs under `.garura/core/tools/` (for example the memory tool).
- **Business intent**: what a person wants, in their words, with its **Outcome**, **Why**, **Proof it is met** and
  **Must not**. Its **stage** is proposed, confirmed, met or dropped; "met" means its proof holds. Its **What was done**
  block records what was delivered for it and the value each piece brought.
- **Product model**: the shared map of the product that people and agents read, under `.garura/product/product-os/`.
  **Spec**: BI-1's word for the intents, domains, capabilities and features in it. **Spine**: the model's index,
  `_spine.yaml`. **ICE**: the agent's intent for one capability or feature.
- **Drift**: a difference between what the model says and what is true elsewhere (the work, the tracker, memory).
- **Short-term memory**: one issue's own folder, `.garura/project/issues/<issue>/`. **Garura memory**: the project's own
  memory; in this repo only the product model, since `.garura/core/memory/` was removed (#942, item 1). **Phoenix
  memory**: the shared memory on the machine that every project reads. **Memory update**: a draft answer an agent
  raises when no memory answers; a person approves or rejects it, and an approved one is written into short-term
  memory. **Promotion**: moving memory up, from short-term memory to Garura memory or to Phoenix memory; a person makes
  it on purpose, outside the work. **Decision trace**: the record of a decision and the memory lines it rested on.
- **Signal**: in the ADLC note (`docs/philosophy/intent-and-adlc.md`, "designed, not in force"), what is received from
  outside: "Signals land on intents. Only on intents." (line 335).
- **Source**: a saved copy of what a person gave (a file, a document, their own words).
- **Production**: the live product that people use. **Pre-production**: the last environment of Garura's path.
- **Stale**: a part marked `stale: true` in its front matter. It waits for a rebuild, and no install lays it (#855, the
  task that marked the old-chain parts stale and kept them out of every install).
- **Pinned gate**: a checkpoint that always waits for a person. **Loop**: a play that runs other plays in rounds until
  its goal is met. **Change plays**: /start-change, /commit-change, /propose-change, /check-change and /merge-change.

States: **Live and in use** · **Live, full install only** (built and not stale, but Garura's own repo installs the
harness scope, so it is not laid here) · **Built, unused** (not stale, but no play runs it) · **Stale** (with its
stale note) · **Planned only** · **Dropped**.

"Ends in" names the business intent whose output the item ends in, by his rule: Spec (BI-1), Design (BI-2), Code
(BI-3), Validation (BI-4), Run (BI-5), Product (BI-6), or "none" for parts that only run, track or support the work
(with the other intent named when it has one: Memory is BI-10, Standards, structure, settings and memory; Manage the
model is BI-11, Product model).

## 1. Where "what happens in use" can come from today

- **Production**: closed by approved rules. "Never: declare, build or touch production. No environment here is
  production, and nothing here reads from it or writes to it, which includes copying its data into an environment"
  (`environment-setup/capability.md` line 59); "Never: touch production" (`deployment-design/capability.md` line 66);
  "Never read: ... anything in production, such as its data or its traffic" (`test-performance/ice.md` line 14). The
  product owner: "We are never touching production." *State:* Dropped as a source. *Ends in:* none; binds BI-6.
- **The end of Garura's path** (a release accepted in pre-production, with its record): BI-5 parked on 2026-11-10,
  nothing in the model (`capabilities.md` line 59); the acceptance and release records are planned only (BI-5
  inventory, sections 4 and 5). *State:* Planned only, parked. *Ends in:* Run (BI-5).
- **People's own words**: the product owner or a team member says what happened, today as an issue, a comment or an
  answer in a session; it never reaches an intent page. The ADLC note expects this: "Until the system is connected,
  those signals come from humans — someone reports where the intent is heading. That signal history is itself a
  graph." (lines 401-403). Specify the product keeps what a person gives as a Source (`specify-product/capability.md`
  line 44), and Specify against what exists sorts it: "a new intent, an enhancement, a new feature under one, or a
  clash" (`specify-product/fn-specify-against-existing/feature.md` line 4, "to build"). *State:* by hand; the sorting
  is Planned only. *Ends in:* Spec (BI-1) for sorting what is given; Product (BI-6) for the signal on an intent.
- **Defects found in use**: "A defect can be reported anywhere: in a person's own words, as a finding in the review of
  a change, by the eval after the work was accepted, or as a bug in a plan" (`fix-defects-test-first/capability.md`
  line 6); "A defect that no feature covers is not fixed here; it is named as a new need for Specify the product"
  (line 7). /fix-bug: Live, full install only. *Ends in:* Code (BI-3).
- **Garura's own run records**: in this repo there are 183 issue folders; 85 of them hold an evidence folder, 9 hold
  decision traces (`context/citations.jsonl`), and every play run writes a session stamp (`status/session-stamp-*.json`,
  section 6). *State:* Live and in use as records; nothing reads them as signals. *Ends in:* none (Orchestration, BI-9,
  and #969, every run's records kept in the evidence folder of its issue, under BI-10).
- **A listener outside Garura**: the ADLC note's Griffin "**Listens** — to the product, to signals, to quality — and
  **reports**. It can also **spawn its own agents** to act on what it hears." (line 144); Griffin is a Phoenix tool
  built beside Garura (`.garura/user-provided/managing-work.md`, "Phoenix tools and the Phoenix project"). *State:*
  Planned only (a design note). *Ends in:* none (a tool beside Garura).
- **Phoenix memory's analytics shelf**: `knowledge/domains/analytics.md`, "Measure product analytics, not just web.
  Feature usage, adoption, retention" (line 20, read through the memory tool). It is knowledge for building analytics
  into a product, not a reader Garura runs. *State:* Live in memory. *Ends in:* none (memory).

## 2. Learning plays: built, stale, dropped and planned

- **/learn-outcomes** with **author-learnings** (and its scripts `persist_learn.py`, `check_ready_unit.py`): after a
  unit of work ships, reads its "outcome signals" (the slice's measurement design from /shape-measure-lens with
  baseline, target and realized value; the validate verdicts and fix reports; the slice's run design from
  /shape-run-lens, "production actuals"; the delivered epic and slice status) and updates the model's meaning (one-line,
  quality levels that may only rise, earned status, page sections), with one append-only decision per material
  learning; every change cites its outcome; one checkpoint; never the tree's skeleton
  (`core/components/plays/learn-outcomes/reference/ice.md` lines 8-29, C1-C14). *State:* Stale: "waits for the rebuild
  of the learn loop on the current product model (#855)". Every input is gone or stale: /shape-measure-lens is dropped
  (ADR 066 §7) and with it the `realized` stamp ("Whoever rebuilds /build-epic and /learn-outcomes needs to know the
  stamp is gone", ADR 066 line 37); the epic's `delivered` stamp is gone (ADR 048 line 61); /validate-epic and
  /shape-run-lens are stale. Its model writes are now BI-1's: "An older play that was written to bring the model up to
  match what shipped waits for a rebuild" (`keep-spec-matched/fn-update-spec-to-match-built/feature.md` line 40;
  `fn-find-spec-drift/feature.md` line 21). Its name stays: "/learn-outcomes (stays)" under the Specifier role
  (`.garura/project/issues/1021/context/names.md` line 6); ADR 053 line 40 keeps it stale, not dropped. *Ends in:*
  Product (BI-6) by its name and Phoenix memory's naming files; Spec (BI-1) by what it writes. See disagreement 4.
- **The retired learning pipeline**: capture, codify, distill, enrich, reap and the knowledge-extractor agent. "It
  replaces the retired capture/codify/distill/enrich/reap pipeline and the `knowledge-extractor` agent's
  ANALYZE/ENRICH/FAST modes — those concepts are gone." (`core/grounding/glossary.md` line 114). Enrich was its
  promotion step (#319, enrich: promote approved learning proposals into the old product memory, closed 2026-04-30).
  *State:* Dropped. *Ends in:* Product (BI-6), had it lived.
- **check-drift** and **/reconcile**: "An earlier skill, `check-drift`, compared the code with locked specs. Its play
  was never built; the stub was deleted on 2026-06-09 ... A later name for the play was `/reconcile`." (#977, History).
  `TODO.md` line 111 still records a defect in it (DEF-004). *State:* Dropped. *Ends in:* Spec (BI-1), now
  fn-find-spec-drift.
- **/report-bug**: background capture of a defect found inside other work, with where it was found; "Logs without
  approval to act ... Triage is the control, not the write gate" (#538). *State:* Dropped: #538 closed as not planned
  on 2026-10-29; nothing built. *Ends in:* none (its defects go to Code, BI-3). Listed as a pattern: capture cheaply,
  and a person triages.
- **The `measure` play idea**: "Close the intent→outcome loop. Wires telemetry, monitors the success criteria declared
  in intent.yaml against production signal ... nothing measures *product* learning (did it work)."
  (`docs/design/playbook-catalog.md` line 117; the note is a 2026-04-23 "Discovery draft. Not scoped, not
  implemented."). *State:* Dropped (never built; production is now out of reach). *Ends in:* Product (BI-6).
- **/shape-measure-lens** with **author-measure-lens**: each slice's delivery measures, a baseline, a target and a proof
  on speed, tokens and the person's effort; it measured delivery, not use. *State:* Dropped by ADR 066 §7 ("They didn't
  have good reasons to exist. They'll be added if needed, and for now they go."), still in the source and stale. *Ends
  in:* Design (BI-2), had it lived.
- **/learn, /promote and /drift** (the Learn loop's plays): "`/learn` (short-term memory to Garura memory), `/promote`
  (Garura memory to Phoenix memory) and `/drift` (find drift)" (ADR 045 line 62); "Build `/promote` and `/drift` for the
  Learn loop (#611). They are not built yet." (line 98). The memory tool calls them "the /learn-memory and
  /promote-memory plays" (`core/tools/memory/updates.py` lines 7-8); the glossary's Promotion row names
  "`/promote-memory` (not built yet)" (line 41). *State:* Planned only. *Ends in:* Product (BI-6) or Memory (BI-10) for
  /learn and /promote (disagreement 3); Spec (BI-1) for /drift, now fn-find-spec-drift.
- **find-architecture-learnings**: reads Phoenix memory's architecture and technology learnings, "the
  condition-matched, 'what works for us' engine". Nothing writes a new learning into those shelves except a hand
  promotion. *State:* Stale ("waits for the rebuild of the design plays (#855)"). *Ends in:* Design (BI-2), as a reader.

## 3. Comparing what happened with what was intended

- **An intent's proof, its stage "met" and its What was done**: "It is met by its proof, never because its work is
  finished." (ontology, Phoenix memory, line 219); "proposed → confirmed ... → met (its proof holds)" (line 229); What
  was done holds "What was delivered for it and the value each piece brought, with links to the finished work items —
  updated as work finishes" (line 195). In the model there are 16 intent pages: all 16 are confirmed and none is met;
  12 read "What was done: (nothing yet)" and the 4 older ones (bi-717, bi-722, bi-734, bi-756) have no such block, so
  12 + 4 = 16. author-intent-page writes "(nothing yet)" on a new page and keeps the block on a rewrite
  (`core/components/skills/author-intent-page/scripts/write_page.py` lines 28 and 208); the ready check already accepts
  `met` (`core/components/plays/shape-plan/scripts/check_ice_workable.py` lines 26 and 54). *State:* Planned only. BI-1
  lists both as its own not built ("Nothing records what was done for an intent as work finishes, and nothing marks an
  intent met when its proof holds", `keep-spec-matched/capability.md` line 29; `fn-update-spec-to-match-built/
  feature.md` line 42). *Ends in:* Spec (BI-1) as approved; Product (BI-6) by its outcome. See disagreement 5.
- **The rebuild eval** (`core/tools/rebuild-eval/`): a fresh agent builds the product from the intents and the model
  alone, and what the prototype does that the rebuild misses is named as drift (BI-5 inventory, section 6). It compares
  the model with what a person gave, not with use. *State:* Built, run by hand. *Ends in:* Spec (BI-1), where Specify
  the product already uses it.
- **A slice's eval** (/shape-eval, Write the evals that check the work): "Write the eval that checks, from the outside,
  that a business intent is met on its slice's surface" (spine, `cap-shape-eval`). It checks the built work in the
  testing environment, before release, not use. *State:* /shape-eval Live and in use; the runner is not built. *Ends
  in:* Code (BI-3) for writing it, Validation (BI-4) for running it. The nearest built thing to an intent's proof.
- **result-checker** with **judge-loop-result**: checks a finished loop's result against what the loop promised, from
  outside, on another model. *State:* Live, full install only. *Ends in:* none (Orchestration, BI-9).
- **/update-plan's agreement check**: "after the landing, the plan file, the tracker and the model agree", for the
  items its session changed (`core/components/plays/update-plan/scripts/check_agreement.py`). *State:* Live and in use.
  *Ends in:* none (Orchestration, BI-9).
- **#545** (Measure intents — outcome on business, speed and autonomy on agent): open, filed under BI-6's tracker
  issue; "Not approved to build"; parked by the product owner: "we are not at the measurement and connected state yet…
  you can keep it in the backlog — we will come back to it some day." Business intent: "Did the org get what it
  wanted"; agent intent: "How fast it moved, how much was autonomous, how much needed a human" (also ADLC note lines
  387-388). *State:* Planned only, parked. *Ends in:* Product (BI-6) by the tracker; the ADLC note places the step change
  in measurement in a governance harness, "(third, later)" (lines 145 and 394). See disagreement 8.
- **#541** (Build the Product Graph — intents, shape, ADLC and measurements as one graph): open, under BI-11, "Not
  approved to build"; "Measurements do not exist at all." *State:* Planned only. *Ends in:* Product model (BI-11).

## 4. Finding drift and keeping the model true

- **Keep the spec matched to what's built** (BI-1, approved 2026-11-07), with its five features: Find where the spec
  and what's built no longer match (not built); Update the spec to match what's built (built in part: approved words
  can go on any page, all or nothing); Keep an intent's links current (built in part); Replace or retire an intent
  (built in part); Keep the tracker's words matched to the model (not built). "This is about the inside of the work:
  what the agents build and plan is brought back into the spec. What users say once the product runs is not part of
  it. Run → Product handles that." (`keep-spec-matched/capability.md` line 5). *Ends in:* Spec (BI-1). Section 12.
- **#977** (The Learn loop finds where the product model has drifted from what was built, and fixes the model): open,
  filed under BI-1's tracker issue; the source of fn-find-spec-drift. *Ends in:* Spec (BI-1).
- **#990** (The product model moves with the work: a design approval updates it, and /propose-change lets the person
  update it now or leave it for Learn): open, under BI-11; a "leave it" writes the change "to one list of changes not
  yet learned ... so Learn processes exactly that list later". *State:* Planned only. *Ends in:* Product model (BI-11)
  as filed; the "Learn" that reads the list is the step BI-1's Update the spec lists as not built (line 40).
- **find-model-gaps** and **link-model-gaps**: find and close gaps inside the model (one-sided links, duplicates, loose
  parts) in the Discovery loop. *State:* Live, full install only. *Ends in:* Product model (BI-11): "drift inside the
  model with no work in it ... Manage the model owns them" (`keep-spec-matched/capability.md` line 51).
- **The Alignment loop**: the ontology (lines 144, 510, 522, 524, 735) and ADRs 031, 049 and 052 send drift inside the
  model to it; "the Alignment loop is unapproved and unnamed: the product owner names it later, it does not move into
  `/loop-run-product`" (ADR 066 line 79). *State:* Planned only, unnamed. *Ends in:* Product model (BI-11).
- **lint_grounding.py, judge-grounding, check_ice_workable.py**: the model's checks inside the plays that write it.
  *State:* Live and in use. *Ends in:* Product model (BI-11).
- **Decisions against memory**: `memory.py citations --check` names every decision whose memory source changed or is
  gone (`core/tools/memory/README.md` line 128); /shape-slice runs it (`shape-slice/scripts/trace_check.py`). *State:*
  Live and in use. *Ends in:* none (Memory, BI-10).
- **A project's memory against Phoenix memory**: "On each run, `initialize` compares those parts with Phoenix memory
  and names in the brief each block whose parts changed" (`initialize/fn-883/feature.md` line 15). *State:* Planned only
  (no initialize play in the source; its capability serves no intent in the spine). *Ends in:* none (Memory, BI-10).
- **Phoenix memory against Garura's source**: #949 (Phoenix memory has fallen behind Garura's source in 60 places),
  #921 (Phoenix memory stays up to date as Garura is built, and is versioned per release) and #966 (Phoenix memory stays
  in step with Garura's source, and is versioned per release, under BI-10). Open. *Ends in:* none (Memory, BI-10, with
  Install and distribute, BI-7).

## 5. Memory updates and promotion

- **propose, decide, apply** (the memory tool): an agent raises a memory update in its issue's short-term memory; a
  person approves or rejects it ("Only a person decides, one update at a time", README line 136); `apply` writes an
  approved one, and only into short-term memory, and refuses one that is not approved or whose target changed
  (`core/tools/memory/updates.py` lines 122-142). *State:* Live and in use. In this repo there are 6 memory updates
  (in #844, #846 and #1021): 5 waiting and 1 rejected, so 0 applied (7 more are test records in #662's evidence). *Ends
  in:* none (Memory, BI-10).
- **Promotion**: "Moving memory up is not this tool's job. It is a promotion a person makes on purpose, outside the
  work: from short-term memory to Garura memory, or to Phoenix memory." (README lines 152-153); "Moving an answer from
  short-term memory up to Garura or Phoenix memory is a **promotion**. It happens outside the piece of work, as its own
  memory update that a person approves." (ADR 036 lines 54-56); "Promotion is not built ... the play for it
  (`/promote-memory`) does not exist yet." (#942, item 6). *State:* Planned only. *Ends in:* Product (BI-6) by its proof,
  or Memory (BI-10). See disagreement 3.
- **Promotion as done today**: "Promotion today is a manual copy, commit and push into another repository, outside the
  change plays, with no record of which Garura change needed it." (#921). Example: #929 (Send the pages the #920 change
  corrected to Phoenix memory), closed 2026-10-28. *State:* Live, by hand. *Ends in:* none (Memory, BI-10).
- **The review tool's Memory and ADRs section**: #664 ("A person approves a memory update on a card, and it is written
  to its tier: the issue's short-term memory for a researched answer, Garura or Phoenix memory for a promotion"), under
  #653 (agents work only from memory, BI-10). *State:* Planned only. *Ends in:* none (Developer tooling, BI-8, for the
  tool).
- **#942** (A project's memory can be managed, so agents decide only from memory people trust): open, under BI-10; "what
  goes into a project's memory, what changes in it, what is learned into it and what leaves it is checked and reviewed
  by a person". *Ends in:* none (Memory, BI-10).
- **knowledge-builder** with **author-knowledge-page**: in the Discovery loop's knowledge step, researches what memory
  lacks and raises it through `propose` for a person to approve. *State:* Live, full install only. *Ends in:* Spec
  (BI-1), inside the Discovery loop.
- **The learned checkpoint policy** (`distill_gate_policy.py`, #467): learns from how a person answers each checkpoint,
  run at the close of /discover-domains and /discover-capabilities; "learned checkpoint answers are not memory (ADR 036
  §5) — it is the project's gate setting" (Phoenix memory `standards/rules/gate-config.md` lines 57-58). No policy file
  exists in this repo. *State:* Built, wired in two plays; nothing learned here yet. *Ends in:* none (Settings, BI-10).
- **#839** (Review every Claude memory for this project, and set a guardrail on what it may learn): open chore about
  Claude Code's own memory, kept outside the repo. *Ends in:* none (Standards, BI-10).

## 6. Measures and records of Garura's own use

- **Session stamps** (#463, a token spend meter and hard budget caps on every play run, closed): each play binds its
  run to its session record "so spend and behavior are computable OFFLINE ... with zero in-run cost"
  (`core/components/plays/learn-outcomes/scripts/session_stamp.py` lines 5-7); 31 play folders carry the script.
  Reading the stamps is done outside Garura. *State:* Live and in use as records; nothing in Garura reads them. *Ends
  in:* none; raw data for #545's agent-intent measures.
- **Run evidence**: #969 (Every run's records are kept in the evidence folder of its issue), under BI-10. *Ends in:*
  none (BI-10).
- **The ADLC note's measurement design**: "**You cannot measure the Product Graph.**"; measurement sits on intents, not
  on the model (lines 374-389); "Live measurement feeding the Product Graph ... Not yet built (backlog)" (lines 399-403).
  *State:* designed, not in force. *Ends in:* Product (BI-6) or a governance harness outside Garura.

## 7. Loops, names, gates and the tracker

- **/loop-run-product**: the loop for this move (ADR 066 line 77; `names.md` line 23). *State:* Planned only, a name.
  *Ends in:* none (Orchestration, "Run plays as loops"), running BI-6's plays.
- **The Learn loop**: ADR 028 §5 ("Learn — know what to do next, and correct the intent", line 54) and a future loop
  "around **learning from everything**" (line 70); ADR 045 §3 (its plays, line 62); `docs/components/loops.md` line 79
  ("To build (#611)"). ADR 066 §3 drops the plain loop names. *State:* Planned only.
- **#611** (Decide the Learn loop's recipe — learn into Garura memory, promote to Phoenix memory, find drift): open
  spike, filed under BI-6's tracker issue; its old parents #594 (loop recipes) and #606 (the five loops) were closed as
  not planned. *Ends in:* Product (BI-6) by the tracker.
- **The `learn` verb**: ADR 066 gives it to the Specifier role beside `specify` (line 65). Phoenix memory's naming files
  still read "learn: Run -> Product. Read what happened and correct the intent." (`standards/rules/naming.yaml` line 11)
  and list `learn-outcomes` for Run → Product (`naming.md` line 46). *State:* Live in memory; ADR 066 not landed there.
- **The pinned learn gate**: Phoenix memory pins "**learn** (a wrong model learning bends the product model)"
  (`standards/rules/gate-config.md` line 100). *State:* Live as a rule; its play is stale. *Ends in:* none (Standards,
  BI-10), binding BI-6. See disagreement 7.
- **Phoenix memory's routing**: "**Learn loop:** `/learn-outcomes`." (`standards/rules/pipeline-next.md` line 30).
  *State:* Live in memory, pointing at a stale play.
- **BI-6's tracker issue** (garura-intents #6, "Run → Product"): open, with the same words as the page and two
  sub-issues, #611 and #545 (read on 2026-11-10). In the same tracker, BI-1 holds #977, BI-10 holds #942, #653 and #966,
  and BI-11 holds #990 and #541.
- No open issue in this repo is about reading how a product is used: telemetry, usage, feedback, support or
  outcomes after release (searched on 2026-11-10 for learn, promote, drift, outcome, feedback, telemetry, usage,
  reconcile, memory update, run product, retro, lesson, measure, experiment and idea).

## 8. The model today for BI-6

- **BI-6's page** (`intents/bi-6.md`, confirmed 2026-11-02): no Touches list; "What was done: (nothing yet)".
- **The spine**: no domain, capability or feature names `bi-6`. None names `bi-10` or `bi-11` either.
- **The domain**: software delivery planning "does not release the work or run the product" (`domain.md` line 4). A
  BI-6 capability that learns from use sits outside that sentence.

## 9. ADRs that set or change these

- ADR 028 (the lifecycle as loops): Learn, "know what to do next, and correct the intent" (§5); a future loop around
  "learning from everything" (line 70).
- ADR 031 (business intent and ICE): drift goes to an Alignment drive, "(its own drive, not yet designed)"; only a
  person confirms or drops an intent.
- ADR 035, ADR 036 and ADR 039 (memory): every memory write goes to short-term memory; promotion is a person's act,
  outside the work (ADR 036 §3; ADR 039 line 38); learned checkpoint answers are not memory (ADR 036 §5).
- ADR 045 (a drive is now a loop): the Learn loop's plays /learn, /promote and /drift; build them (#611).
- ADR 048 (the model and the work are two layers): no epic record and no `delivered` stamp.
- ADR 053 §4: /learn-outcomes is not dropped; it is stale and rebuilt when its stage comes (line 40).
- ADR 066 (names say who does the work): `learn` is a Specifier verb (line 65); /loop-run-product (line 77); the
  Alignment loop does not move into it (line 79); /shape-measure-lens dropped and the `realized` stamp gone (§7).

## 10. What is built for BI-6

1. **Nothing live learns from use.** No part takes in what happened in use, compares it with an intent's proof, marks
   an intent met, records the value each piece brought, or promotes a learning.
2. **The front half of memory works**: propose, a person's decision, and apply into short-term memory, with decision
   traces and their check. Six updates have been raised here; none has been applied yet.
3. **Records of Garura's own use are written but never read as signals**: run evidence, decision traces, and a session
   stamp on every play run.
4. **A stale pattern**: /learn-outcomes with author-learnings, where every change cites the outcome behind it, levels
   only rise, decisions are only added, a script writes only the allowed fields, and one person approves the whole
   change. Every input it reads is gone or stale.
5. **Promotion by hand**: a copy, commit and push into Phoenix memory's own repository, outside the change plays (#929).
6. **Built in part elsewhere**: drift inside the work (BI-1's Keep the spec matched) and drift inside the model (BI-11's
   gap finder and checks), which BI-6's outcome words also reach.

## 11. What is pending for BI-6

1. **An intake for what happens in use**: what people report, and later what a listener outside Garura reports, taken
   in as given and placed on the intents it bears on, never read from production (disagreement 2).
2. **A comparison of what happened with each intent's outcome and proof**, with "met" and the value each piece brought
   proposed to a person (disagreement 5).
3. **A rebuild of /learn-outcomes on new inputs**, handing each change to the part that owns it (disagreement 4).
4. **Choosing and promoting learnings**: /learn and /promote (/promote-memory), with a record of which work needed each
   (disagreement 3).
5. **Measuring intents** (#545), parked by the product owner (disagreement 8).
6. **#611's recipe and /loop-run-product.**
7. **The model**: BI-6's page words (disagreements 1 and 5), no spine part for `bi-6`, the domain's last sentence, and
   only #611 and #545 under its tracker issue.

## 12. The boundary with BI-1's Keep the spec matched

What BI-1's approved pages give to BI-6 by name:
- "Out: learning from real users once the product runs, where what happens in use is compared with what was intended.
  The Run → Product business intent (BI-6) asks for it." (`keep-spec-matched/capability.md` line 50)
- "It looks at the inside of the work only ... What users say or do once the product runs is not part of it. The Run →
  Product business intent (BI-6) asks for that." (`fn-find-spec-drift/feature.md` line 7; also lines 32 and 50)
- "What users say once the product runs. The Run → Product business intent (BI-6) asks for it."
  (`fn-update-spec-to-match-built/feature.md` line 61)
- The product owner on 2026-11-07: "the internal element: how the agents are working and making sure what the agents
  are implementing gets updated back here, not what the user is telling." (`fn-find-spec-drift/feature.md` line 55)

What BI-1 holds that BI-6's words also reach: finding drift between the spec and the agents' work and naming it to a
person; updating pages from approved words; intent links; replacing and retiring intents; the tracker's words; and, as
"not built" on its own page, recording what was done for an intent and marking it met.

The line, as the approved pages draw it: BI-1 keeps the spec true to what agents built and planned; BI-6 keeps the
product true to what happened in use. Every page change BI-6 finds is made through BI-1's features ("Each fix is made
by the part that owns it", `keep-spec-matched/capability.md` line 62), so BI-6 names and proposes, and BI-1 writes.

## 13. The boundary with Memory (BI-10) and Manage the model (BI-11)

- **Memory** (agreed, no page): "Agents decide from three tiers of memory (Phoenix global, Garura project,
  short-term), and people control what enters them." (`capabilities.md` line 85). BI-10's proof: "Nothing an agent
  decides from sits outside memory." Its tracker holds #942 (a project's memory can be managed), #653 (one memory
  tool) and #966 (Phoenix memory in step with the source). Proposed line: BI-10 owns the tiers, the tool (including its
  promote path), the checks on memory and Phoenix memory's link to the source; BI-6 owns choosing which learnings from
  finished work and from use are worth promoting, and proposing them. See disagreement 3.
- **Manage the model** (agreed, no page): "A living map, added to and pruned as work is done, and the source of what to
  try next." (`capabilities.md` line 90). BI-11's proof: "The model proposes an idea with its evidence, a person
  confirms it, and an experiment records the result." Already its own by BI-1's page: drift inside the model with no
  work in it, the link rules, merging capabilities and removing slices (`keep-spec-matched/capability.md` line 51), and
  the unnamed Alignment loop. Proposed line: BI-6 lands what happened on intents as evidence; BI-11 turns evidence into
  ideas and experiments. See disagreement 6.
- **#990** sits under BI-11 but its "Learn" step is BI-1's update step; it is not BI-6's unless the product owner
  calls the not-yet-learned list a learning to promote.

## 14. The boundary with BI-5 (parked)

- BI-5 would end with a release accepted in pre-production and recorded, handed to whoever runs production (BI-5
  inventory, disagreement 1, lean A: "gives Product (BI-6) a defined hand-over to learn from"). It is parked, so BI-6
  cannot start from an accepted release today.
- BI-5's proposed "Record and hand over each release" would tell BI-6 which plan items and intents a release held. Until
  it exists, BI-6 can tie a report from use to an intent, but not to a release.
- What happens after pre-production is outside Garura. BI-6 can receive reports about it; it never reaches it.
- No approved page names a hand-over from BI-5 to BI-6.

## 15. Lines on approved pages that would overlap a BI-6 capability

1. `keep-spec-matched/capability.md` line 29 and `fn-update-spec-to-match-built/feature.md` line 42 (BI-1) list
   recording what was done for an intent and marking it met as BI-1's own not built. A BI-6 comparison against the
   proof would overlap. See disagreement 5.
2. `fn-find-spec-drift/feature.md` line 4 (BI-1) finds drift between the spec and the agents' work and names it, the
   substance of BI-6's first proof. See disagreement 1.
3. `fn-update-spec-to-match-built/feature.md` line 40 and `fn-find-spec-drift/feature.md` line 21 (BI-1) treat the stale
   /learn-outcomes as the older form of their own step. See disagreement 4.
4. `fn-find-spec-drift/feature.md` line 39: "Not decided: where and when it runs ... The product owner names the loop or
   the play that runs it." If /loop-run-product runs it, BI-6's loop calls a BI-1 capability.
5. `fn-replace-or-retire-intent/feature.md` line 34: "Not decided: the old intent's record of what was done." Whoever
   writes the value each piece brought has to keep it through a retirement.
6. `specify-product/fn-specify-against-existing/feature.md` line 4 and `fix-defects-test-first/capability.md` lines 6-7
   take what a person reports (a new need, a clash, a defect). They fit as written: BI-6 hands them what it learns and
   does not sort or fix it.
7. The line "Out: moving an approved memory update into Phoenix memory. A memory update goes to the project's
   short-term memory, and moving it up is a promotion a person makes on purpose, outside this work." on four BI-2
   capability pages (`design-technology-architecture/capability.md` line 43, `manage-surfaces/capability.md` line 53,
   `deployment-design/capability.md` line 65, `environment-setup/capability.md` line 58), their features, and the BI-3
   page `write-work-evals/fn-add-eval-steps/feature.md` lines 27 and 39. None names an owner. They fit as written; a
   promotion capability (BI-6 or BI-10) is that owner.
8. `environment-setup/capability.md` line 59, `deployment-design/capability.md` line 66 and `test-performance/ice.md`
   line 14 forbid reading from production. They bind BI-6's intake.

## 16. Where his rule and the approved model or BI-6's page disagree

His rule (2026-11-08): each business intent holds the plays whose output ends in its phase; BI-6 holds what ends in
the product (its intents, model and memory) kept true to what happened in use.

### Disagreement 1: BI-6's first proof is already BI-1's work

BI-6's proof reads "Drift between the model and the work gets named." BI-1's approved Find where the spec and what's
built no longer match "finds the places where the spec no longer matches what the agents built and planned, and names
each one to a person" (`fn-find-spec-drift/feature.md` line 4), and BI-1's own proof reads "An intent that drifts from
the product gets named." The approved BI-1 pages give BI-6 only what happens in use.

- **Option A, reword BI-6's proof at its close** to the drift only use shows, for example a gap between what an intent
  asked and what happened in use gets named. BI-1 keeps every check inside the work.
- **Option B, move Find where the spec and what's built no longer match to BI-6**, because "drift is found" is in
  BI-6's outcome. BI-1's approved pages and proof change.
- **Option C, keep both proofs**, with BI-6's loop running BI-1's check as one step and holding no capability for it.

**Lean: A.** The product owner drew this line himself on 2026-11-07 ("not what the user is telling"), and an approved
page already holds the check inside the work.

### Disagreement 2: "what happens in use" when nothing reaches production

BI-6's outcome starts "What happens in use flows back." Garura never touches production and reads nothing from it
(section 1), and BI-5, the only part that would reach pre-production and record acceptance, is parked.

- **Option A, use reaches Garura only as what people report.** The product owner, a team member or whoever runs
  production says what happened; it is kept as a Source, as given, and placed on the intents it bears on. Nothing reads
  production. This is what the ADLC note expects "until the system is connected" (line 402).
- **Option B, "use" means the end of Garura's own path**: pre-production acceptance (BI-5, parked), BI-4's verdicts,
  defects and Garura's own run records. BI-6 waits for BI-5, and until then reads only the path's records.
- **Option C, a listener outside Garura** (the ADLC note's Griffin, line 144), run by the team that owns production,
  reads use and hands Garura a report. Garura still never touches production.

**Lean: A now, with C as where it grows.** A needs nothing that reaches production and matches "those signals come
from humans"; C later feeds the same intake. B makes BI-6 wait on a parked intent and mostly repeats BI-4's and BI-5's
records.

### Disagreement 3: who owns promotion

BI-6's proof reads "Each learning is promoted on purpose", and its must-not names promotion. The agreed Memory line in
BI-10 says "people control what enters them", and #942 under BI-10 holds "what is learned into it" and the missing
/promote-memory. ADR 045's /learn and /promote, and #611, sit under BI-6.

- **Option A, split by output.** BI-6 chooses the learnings worth keeping, from finished work and from use, and
  proposes each one for Garura memory or Phoenix memory. BI-10's Memory owns the mechanism: the tiers, the tool and its
  promote path, the checks and the review of what enters memory.
- **Option B, BI-10 owns all of promotion.** BI-6 only leaves learnings as memory updates in short-term memory.
- **Option C, BI-6 owns all of it**, /learn and /promote together, and BI-10 keeps only reading memory and its tiers.

**Lean: A.** By his rule a promoted learning ends in the product's memory (BI-6), while the tool and its guardrails are
the foundation every intent stands on (BI-10's outcome: "agents decide from three tiers of memory").

### Disagreement 4: /learn-outcomes, which intent and on what inputs

`names.md` keeps "/learn-outcomes (stays)" under the Specifier role, and ADR 066 puts `learn` with `specify`, BI-1's
verb. Phoenix memory's naming files put `learn` at Run → Product. What it wrote, the model's meaning, is now BI-1's
Update the spec, which calls it "an older play". Every input it reads is gone or stale.

- **Option A, rebuild it as BI-6's play on new inputs**: what people report from use and the records of the path. It
  compares them with each intent, proposes "met", names the gaps, raises memory updates, and hands every page change to
  BI-1's features instead of writing pages itself.
- **Option B, rebuild it as BI-1's play** for Keep the spec matched, which is what it did before, and give BI-6 a new
  play.
- **Option C, drop it**, as /shape-measure-lens was, and build BI-6's parts new.

**Lean: A.** Its name and Phoenix memory's naming put it at Run → Product, handing page changes to BI-1 respects the
approved pages, and a rebuild on new inputs is what ADR 053 §4 asked for.

### Disagreement 5: marking an intent met, and the value each piece brought

The ontology says an intent "is met by its proof, never because its work is finished", and What was done holds "the
value each piece brought". BI-1's approved pages list both the growing record and marking an intent met as BI-1's own
not built. Checking a proof against what happened is BI-6's "What happened is compared with what was intended."

- **Option A, BI-6 judges both**: it checks each proof against what happened and proposes "met" and each piece's value
  to a person; BI-1's update feature writes the page from those approved words.
- **Option B, all in BI-1**, as its page says now.
- **Option C, split**: "What was delivered", added as work finishes, stays with BI-1, because it is inside the work;
  "the value each piece brought" and "met", which need evidence from use, go to BI-6. BI-1 writes the page in both.

**Lean: C.** It keeps BI-1's approved page true for the part about the work, and gives BI-6 only what needs evidence
from use.

### Disagreement 6: ideas and experiments, BI-11 or BI-6

BI-11's outcome holds "a source of new ideas and experiments", its proof "The model proposes an idea with its
evidence, a person confirms it, and an experiment records the result", and the agreed Manage the model line ends "the
source of what to try next". The ADLC note says "The Product Graph is a representation. It cannot give a signal.
Signals are received on intents" (lines 340-341). Evidence from use is BI-6's.

- **Option A, BI-6 lands what happened on intents as evidence; BI-11 turns evidence into an idea**, and an experiment's
  result comes back to BI-6 as one more thing that happened.
- **Option B, BI-6 holds the whole loop**: evidence, idea, experiment and result.
- **Option C, leave it to BI-11's review**, and keep ideas out of BI-6 until then.

**Lean: A.** It keeps the rule that signals land on intents, keeps "the source of what to try next" with the model as
agreed, and gives each intent one clear output.

### Disagreement 7: "agentic and highly autonomous" against BI-6's must-not and the pinned learn gate

The product owner on 2026-11-10, on CI: "I would expect it to find the drifts and look at what issues are being
committed and what it can fix automatically. It would act like an agent ... reflecting and telling us what needs to be
done." (`capabilities.md` line 59). BI-6's must-not: "Change an intent, or promote memory, without a person." Phoenix
memory pins the learn checkpoint (`gate-config.md` line 100), and BI-1 says "Never: fix drift in silence."

- **Option A, the agent works on its own except where the must-not names a person.** It watches, compares, finds,
  drafts and hands each fix to its owner without stopping; a person says yes to each change of an intent's words or
  stage and each promotion, and each drift fix keeps BI-1's yes. The pinned learn gate narrows to those.
- **Option B, autonomy grows with the agents**, as a setting a person records, starting with a person on every
  learning ("It depends on the maturity of the agents", ADLC note line 362; its open question 3).
- **Option C, a fixed run of plays with a person's yes at each learning**, as /learn-outcomes was.

**Lean: A.** It is the shape he asked for in CI and CD, and keeps exactly the person BI-6's must-not asks for. B can be
added on top later.

### Disagreement 8: measuring intents (#545), BI-6 or a governance harness

#545 is filed under BI-6's tracker issue and parked. The ADLC note places the step change in measurement in a
governance harness, "(third, later)" (lines 145 and 394), outside Garura.

- **Option A, keep it as a planned BI-6 capability, parked** as he said, with the session stamps as its raw data.
- **Option B, leave measurement to the governance harness**; BI-6 reads its results as one more thing that happened.
- **Option C, split**: agent-intent measures (speed, autonomy, how often a person stepped in) go to Orchestration
  (BI-9), where the session stamps and checkpoint records are; business-intent outcomes stay with BI-6.

**Lean: A.** By his rule a measure on an intent ends in the product, the tracker already holds it under BI-6, and the
governance harness does not exist.

### Other places where the two do not match (no options asked)

- **The domain.** "It does not release the work or run the product" (`domain.md` line 4). A person decides whether
  BI-6's capabilities sit in software delivery planning, with that line changed, or in a domain of their own.
- **Phoenix memory's naming** reads "Read what happened and correct the intent." (`naming.yaml` line 11); BI-6's
  must-not and BI-1 forbid an agent to correct an intent without a person.
- **Two meanings of "learn".** ADR 045 and `loops.md` line 79 say /learn moves memory from short-term memory into Garura
  memory; /learn-outcomes updates the product model. The model is part of Garura memory (ADR 039), so both write
  Garura memory, but the two descriptions differ.
- **"Know what to do next"** is in IDSD's Learn (`docs/philosophy/idsd.md` line 176) and ADR 028 §5; /next is dropped
  (ADR 051) and the plan is the work list; the agreed Manage the model holds "the source of what to try next".
- **ADR 028's loop "around learning from everything"** (line 70) was never defined.
- **BI-6's outcome** says "the intents, model and memory stay true", but inside the work the intents and the model are
  BI-1's, drift inside the model is BI-11's, and checks on memory are BI-10's.
- **BI-6 has no capability in the spine**, and its tracker issue holds only #611 and #545, whose old parents (#594,
  #606) were closed as not planned.

## 17. Proposed BI-6 capabilities

From BI-6's page, the agreed lists, built parts, ADRs, open issues and the product owner's words. No page is drafted.

1. **Take in what happens in use** (from BI-6's outcome, "What happens in use flows back"; the ADLC note, "Signals land
   on intents. Only on intents." and "those signals come from humans", lines 335 and 402; #545, "Human-reported signals
   on a business intent accumulate over time as a history"). Planned. What people report about the product in use, and
   later what a listener outside Garura reports, is taken in as it was given, kept as a Source, and placed on the
   intents it bears on; production is never read. Built today: none; the dropped /report-bug (capture, then a person
   triages) and Specify the product's Source copy are patterns.
2. **Compare what happened with what was intended** (from BI-6's outcome, "What happened is compared with what was
   intended"; IDSD's Learn, line 176; the ontology, "It is met by its proof"). Planned. Each intent's outcome and proof
   are set against what happened in use and on the path; each gap is named to a person with where it comes from; a
   proof that holds is proposed as met, with the value each piece brought. Built today: none. A slice's eval checks the
   built work against the intent before release (BI-4); the rebuild eval compares the model with a prototype (BI-1).
3. **Learn from outcomes and hand each change to its owner** (from /learn-outcomes, whose name `names.md` keeps; the
   product owner on CI, "reflecting and telling us what needs to be done"; BI-1's "Each fix is made by the part that
   owns it"). Planned; stale /learn-outcomes. From each named gap, the change it calls for is drafted and handed to the
   part that owns it: a page to Update the spec to match what's built (BI-1), a new need to Specify against what
   exists (BI-1), a defect to Fix defects test first (BI-3), an intent's words or stage to the person; each material
   learning is recorded, as /learn-outcomes did. It never changes an intent itself.
4. **Choose and promote each learning on purpose** (from BI-6's proof, "Each learning is promoted on purpose", and
   must-not; ADR 045's /learn and /promote; #611; /promote-memory in the glossary; the /learn-memory and /promote-memory
   plays named in `updates.py`). Planned. What finished work and use taught, kept in short-term memory, is chosen and
   proposed for Garura memory or Phoenix memory one at a time, and moves up only on a person's yes, with a record of
   the work that needed it. Built today: the front half only (propose, decide, apply into short-term memory, BI-10);
   promotion is a hand copy (#921). Under disagreement 3's lean, the tool's promote path is BI-10's.
5. **Measure each intent** (from #545, under BI-6's tracker issue; the ADLC note, lines 387-388). Planned, parked by
   the product owner ("we will come back to it some day"). Each business intent is measured on whether it got what it
   wanted, and each agent intent on how fast it moved and how often a person stepped in. Built today: raw records only,
   the session stamp on every play run (#463).

Not proposed as BI-6 capabilities: finding drift inside the work, updating spec pages, intent links, replacing and
retiring intents and the tracker's words (BI-1, Keep the spec matched); drift inside the model, ideas and experiments,
and the model tool (#1030) (BI-11, Manage the model); the memory tiers, the memory tool, its checks and Phoenix memory
against the source (#921, #949, #966) (BI-10, Memory); the learned checkpoint policy (BI-10, Settings); fixing defects
(BI-3); acceptance and release records (BI-5, parked); the review tool's memory section (#664, BI-8);
/loop-run-product (Orchestration, which runs BI-6's plays).

## 18. Where the agentic ask bears on BI-6

The product owner, 2026-11-10, recorded in `capabilities.md` line 59: "This needs to be built for high autonomy. For
CI, I would expect it to find the drifts and look at what issues are being committed and what it can fix
automatically. It would act like an agent ... reflecting and telling us what needs to be done." and "I almost feel
like that part of CI/CD needs to sit outside of Khoros" (assumed there: Garura).

- **One agent loop, not a fixed chain.** Capabilities 1 to 3 read as one loop that watches, compares, reflects and
  hands off, run by /loop-run-product in rounds until nothing new is found, rather than once per delivered unit as
  /learn-outcomes was ("One delivered unit per run", its C1).
- **The listening part has a planned home outside Garura.** The ADLC note's Griffin "Listens ... and reports. It can
  also spawn its own agents to act on what it hears." (line 144), which matches his sense that the autonomous part sits
  outside. Garura keeps the part that writes intents, the model and memory, through its skills and a person's yes.
- **Autonomy has two fixed limits.** BI-6's must-not (no change of an intent and no promotion without a person) and
  BI-1's "Never: fix drift in silence". Everything else can run on its own; the pinned learn gate would narrow to those
  (disagreement 7).
- **Who resolves a signal can move to agents over time**: "It depends on the maturity of the agents" (ADLC note line
  362), with "How agent maturity is declared and raised" still open (its open question 3).
- **It never stops a person**: BI-9's must-not, "Every gate has a way past it that records what's owed." A learning no
  one has answered waits as owed and blocks no other work.
