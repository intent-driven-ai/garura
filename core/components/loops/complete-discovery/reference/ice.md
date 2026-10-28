# ICE — discovery

The first loop (ADR 029 §6). It solves product → intent: from a working prototype to business
intents the person has decided and a detailed product model. Built from #613's acceptance
criteria and the runner design (`.garura/project/issues/613/specs/runner-design.md`).

## Intent

**Goal:** from a working prototype and the person's short write-up, end with business intents
the person has decided, the domains the product sits in, its capabilities and features
— each read from the screens on its own and all of them linked — on one issue and one branch,
asking the person only what none of its plays, memory or approved research answers, and
checked by a checker the config picks (ADR 043).

### Constraints

- C1 — The loop works on one issue and one branch. Everything the loop and its plays write is
  under that issue, and no play opens an issue or a branch of its own.
- C2 — A working prototype is given — a file, a project folder or a link — and it runs (a link
  answers; a folder or file is there and the person says how it starts). Without one the loop
  halts before it opens anything. Beside it the person gives a short write-up in five parts:
  what the product is; who uses it; the field it serves and the job it does there; what on the
  screens is only sample data; a walkthrough of the steps a person takes (Kapil, 2026-10-21:
  "prototype isn't enough … a small write up … that explains the prototype … this will guide
  the drive and internally plays very well"). Without it the loop asks for it before any play
  runs; it never writes it itself.
- C3 — The loop asks its own questions and gets the write-up before any play runs, and records
  where every answer and document came from. It reads the prototype once, through the
  `prototype-reader` agent, and hands that one capture and the write-up to every play. The
  loop reads no memory itself (ADR 039); its plays' agents do.
- C4 — The plays read the prototype independently and each writes one kind (ADR 043):
  `/discover-intent` business intents, `/discover-domains` domains, `/discover-capabilities` capabilities and features
  with their ICE. No play takes another play's output as its input, so their readings are
  independent and their agreement is the check. They run **in rounds, until the loop's job is
  done** (Kapil, 2026-10-20: "the idea of a drive is to have it loop between those three things
  until the job is getting done"): after each round the loop has the model's gaps found and
  closed (`find-model-gaps`, `link-model-gaps`, through `product-os-keeper`) — every
  feature linked to its capability, every capability to its domain, each node to the
  intents it serves, duplicates merged — and gives the work still missing to the play that does
  it; the next round runs only those plays, on exactly that work (Kapil, 2026-10-21: "The whole
  point of a drive is that these loops are closed … connecting the three meaningfully so that
  the work gets done"). Each play proves its own done check, and the round is committed once.
  The first build runs the plays one after another, in turn.
- C5 — Nothing comes from the model alone. A question one play cannot answer is the loop's,
  not a stop: the play records it and finishes what it can, and the other plays — and the next
  round — may answer it. The loop stops and asks the person only what no play of the loop,
  no memory and no approved research can answer: after a round that answered nothing new, or at
  the round limit. **First it finds and builds the missing knowledge** in one step of the loop,
  run by the `knowledge-builder` agent (Shared Loop Run R5c, ADR 059): what the prototype shows
  is answered from it, what memory holds from memory (through the memory tool), what research
  can answer is drafted as knowledge pages for the person to approve, and for what only the
  person can confirm we draft our own answer. Only then does it reach the person — with the
  brief that step writes (R5b): what we understood, what we built, and a few gaps each with its
  context and our proposed answer, never a questionnaire (Kapil, 2026-10-20). The answers are
  kept in the issue's short-term memory.
- C6 — A checker the config picks, which is not the loop's own model, judges the result against
  this intent from the loop's outputs only. A reject halts the loop.
- C7 — The loop never confirms or drops an intent, and never changes an intent's state in the
  model. Until the review tool exists (#641–#650), the loop ends at the pull request: the
  person types **confirm** or **drop** for each proposed intent, and the loop records their
  exact words in the issue's short-term memory. The intents stay `proposed` in the model until
  the review tool's review step writes the approval (#650, ADR 033). The merge keeps its pinned
  human approval.
- C8 — The loop records its evidence, whatever the global evidence setting says.

### Failure conditions

- F1 — The loop or a play wrote outside the loop's issue, or opened a second issue or branch.
- F2 — The loop ran without a working prototype, or with one that does not run.
- F3 — A play ran before the loop's questions were asked or the write-up was given, an answer
  or the write-up has no source, or a play walked the prototype again instead of reading the
  one capture.
- F4 — A play took another play's output as its input, wrote a kind that is not its own, or
  started on an unclean tree; or the loop ended done with a node not linked, a duplicate not
  merged, or a screen no node covers.
- F5 — An answer came from the model alone: a question nothing supported was answered instead of
  asked; or the loop stopped to ask a question another of its plays, or a later round, could
  have answered; or it asked the person about something it had not shown them.
- F6 — The loop ended as done without the checker's pass.
- F7 — The loop changed an intent's state in the model, or recorded a decision on an intent
  without the person's own typed word.
- F8 — The loop closed with no evidence record.

## Context

ADR 029 (loops; Discovery, §6), ADR 031 (business intent and ICE; only a person confirms an
intent, D10), ADR 032 and 033 (the review; approval in the model), ADR 034 (a play answers from
memory inside a loop), ADR 039 (the issue ID governs), `standards/rules/loop-contract.md`, the
Shared Loop Run (`../_shared/loop-run.md`). The #662 run proved the three plays run from
memory alone under one contract.

The plays' own content questions depend on what the prototype shows, so the loop cannot ask
them before the plays read it. A play that cannot answer one makes it the loop's question (C5); the
other plays, the next round and the knowledge step may answer it, and the person is briefed only
on what none of them can (ADR 041, ADR 059). The loop asks first only what it can know up front.

Not built yet: ADR 029 §6 gives Discovery a second output, a plan and its issues for the person,
with `approve-change` in its done check. This loop makes only the product model; the plan and
its issues are an open item on #613's plan, waiting on Kapil.

## Plays

No play's input is another play's output (ADR 043). The order is only the order they run in,
in turn.

| Play | Writes | Inputs from the contract | Answers from the questions |
|------|--------|--------------------------|----------------------------|
| discover-intent | business intents | `argument` — the prototype; `capture`; `write_up`; on a later round `targets` | `may_change_data` (a link) |
| discover-domains | domains | `capture`; `write_up`; on a later round `targets` | — |
| discover-capabilities | capabilities and features, with their ICE | `capture`; `write_up`; on a later round `targets` | — |

## Questions first

Asked at pre-flight, before the loop opens anything, because the prototype check needs them (C2):

- Where is the working prototype — a file, a project folder or a link? → `inputs.discover-intent.argument`
- For a file or a folder: how does it start? → `prototype.json` (`start`), the pre-flight's
  proof it runs
- For a link: may the walk press buttons that change data on it (pay, delete, submit)?
  → `answers.discover-intent.may_change_data` (`true` only on the person's yes; a file or local
  prototype needs no answer — nothing real changes)
- The write-up, in five parts (C2), when the person did not give it with the prototype →
  `write-up.md` in the run folder, `from: person`; captured as a Source with the prototype and
  handed to every play inside its `inputs.<play>.capture`

## Checker

`loops.complete-discovery.checker` — default `kind: subagent` on a model that is not the session's. It
judges this goal and these constraints against the loop's outputs only (`judge-loop-result`).

## Runner

`loops.complete-discovery.runner` — `subagent` (default) or `headless`. `loops.complete-discovery.max_rounds` —
the most rounds before the loop asks (default 3).

## End

Stand-in until the review tool (C7; Kapil, 2026-10-20, "2"): `commit-change` →
`propose-change` → **the person types confirm or drop for each proposed intent; the loop
records their words** in `confirmation.yaml` in its run folder (the intents stay `proposed` in
the model) → `check-change` → `merge-change`, the merge keeping its pinned approval. The
review tool's review step replaces the typed step and writes the approval into the model
(#650).

## Expectation

### Success scenarios

- S1 — business owner. Given a deployed prototype link; then the three plays run without a stop
  for approval, the checker passes, a pull request opens, the owner types confirm
  or drop for each intent, and the change merges on their approval; measure: `contract.json`,
  the three plays' done files reading `done: true`, `check.yaml` reading `verdict: pass`, and
  `confirmation.yaml` holding one decision per proposed intent in the owner's own words exist
  under the issue, and every intent page still reads `proposed`.
- S2 — business owner. Given no prototype, or a link that does not answer; then the loop halts
  before it opens an issue or a branch; measure: no new branch exists and the loop closed
  HALTED with `exit_reason: preflight`.
- S3 — business owner. Given a prototype and its write-up, where round 1 leaves nodes unlinked
  and work missing; then the gap skills link what the model can take, the next round runs only
  the plays given work, and the owner is briefed only on what is still open — our proposed
  answers with their context; measure: `round-1.json` reads `again` with `next` naming plays
  and their targets, the last `round-<n>.json` reads `gaps_left: 0`, any brief comes after a
  `round-<n>.json` that reads `ask` with its `knowledge-check.json` reading `ok: true`, and each
  answer is in the issue's short-term memory with `from: person`.
- S4 — business owner. Given a run the checker rejects; then the loop halts with the
  checker's reasons and opens no pull request; measure: `check.yaml` reads `verdict: reject`
  with a reason for each failed criterion, and no pull request exists for the branch.

### Recovery

| For | Trigger | Direction | Handoff |
|-----|---------|-----------|---------|
| F1 | a write outside the issue, or a second issue or branch | move the record under the loop's issue; run on the contract's branch | autonomous |
| F2 | no prototype, or one that does not run | halt before opening; ask the person for a working prototype | human |
| F3 | a play ran before the questions or the write-up, an answer or the write-up has no source, or a play walked the prototype again | stop; get the write-up and ask the questions, record each source, read the prototype once, re-run the play on the capture | autonomous |
| F4 | a play took another's output or wrote another's kind, an unclean tree, or done with gaps left | halt; re-run the play on the capture alone, writing only its kind; commit the round; run the gap skills and the plays they give work to | autonomous |
| F5 | an answer from the model alone, a stop for a question the loop could still answer, or a bare question put to the person | strip the answer, or go on round the loop; brief the person only on what no play answers (the knowledge step's brief: our proposed answer with its context); re-run the play | human |
| F6 | done without the checker's pass | run the checker; a reject halts the loop | autonomous |
| F7 | the loop changed an intent's state, or recorded a decision without the person's word | undo the change to the intent page; ask the person and record their own words | human |
| F8 | no evidence record | write the evidence before closing; the close stays HALTED until it exists | autonomous |

### Done means

- D1 — the loop's contract exists. Check: `artifact_exists` `contract.json`.
- D2 — `/discover-intent` proved its done check. Check: `field_equals` `discover-intent-done.json` `done` = `true`.
- D3 — `/discover-domains` proved its done check. Check: `field_equals` `discover-domains-done.json` `done` = `true`.
- D4 — `/discover-capabilities` proved its done check. Check: `field_equals` `discover-capabilities-done.json` `done` = `true`.
- D5 — the checker passed. Check: `field_equals` `check.yaml` `verdict` = `pass`.
- D6 — the person decided every proposed intent, in their own words. Check: `field_equals`
  `confirmation.yaml` `by` = `person`.
- D7 — no question is left open when the loop ends. Check: `field_equals` `rounds.json`
  `open_left` = `0`.
- D8 — the model's gaps are closed: every node linked, no screen uncovered. Check:
  `field_equals` `rounds.json` `gaps_left` = `0`.
