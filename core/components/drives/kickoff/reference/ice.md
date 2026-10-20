# ICE — kickoff

The first drive (ADR 029 §6). It solves product → intent: from a working prototype to business
intents the person has decided and a detailed product model. Built from #613's acceptance
criteria and the runner design (`.garura/project/issues/613/specs/runner-design.md`).

## Intent

**Goal:** from a working prototype, end with business intents the person has decided, a domain
with its capabilities, and every capability detailed — on one issue and one branch, asking the
person only what none of its plays, memory or approved research answers, and checked by a checker the config picks.

### Constraints

- C1 — The drive works on one issue and one branch. Everything the drive and its plays write is
  under that issue, and no play opens an issue or a branch of its own.
- C2 — A working prototype is given — a file, a project folder or a link — and it runs (a link
  answers; a folder or file is there and the person says how it starts). Without one the drive
  halts before it opens anything.
- C3 — The drive asks its own questions before any play runs, and records where every answer
  came from. The drive reads no memory itself (ADR 039); its plays' agents do.
- C4 — The plays run in the fixed order `/intent` → `/vision` → `/understand`, **in rounds,
  until the drive's job is done**: each round runs all three, and the next round gives each
  play what the others found (Kapil, 2026-10-20: "the idea of a drive is to have it loop between
  those three things until the job is getting done"). Each play proves its own done check, and
  its run files are committed, before the next one starts. `/understand` details every
  capability `/vision` seeded, in one run per round.
- C5 — Nothing comes from the model alone. A question one play cannot answer is the drive's,
  not a stop: the play records it and finishes what it can, and the other plays — and the next
  round — may answer it. The drive stops and asks the person only what no play of the drive,
  no memory and no approved research can answer: after a round that answered nothing new, or at
  the round limit. **First it builds the missing memory** (`/build-memory`, Kapil, 2026-10-20:
  "asking 80 questions … doesn't seem realistic"): what the prototype shows is answered from it,
  what memory holds from memory, what research can answer is drafted as knowledge pages for the
  person to approve. Only then does it ask — after showing the draft, each question once, in
  words that make sense to the person who shared the prototype — and it shows the prototype
  feedback (what the prototype should show). The answers are kept in
  the issue's short-term memory.
- C6 — A checker the config picks, which is not the drive's own model, judges the result against
  this intent from the drive's outputs only. A reject halts the drive.
- C7 — The drive never confirms or drops an intent, and never changes an intent's state in the
  model. Until the review tool exists (#641–#650), the drive ends at the pull request: the
  person types **confirm** or **drop** for each proposed intent, and the drive records their
  exact words in the issue's short-term memory. The intents stay `proposed` in the model until
  the review tool's review step writes the approval (#650, ADR 033). The merge keeps its pinned
  human approval.
- C8 — The drive records its evidence, whatever the global evidence setting says.

### Failure conditions

- F1 — The drive or a play wrote outside the drive's issue, or opened a second issue or branch.
- F2 — The drive ran without a working prototype, or with one that does not run.
- F3 — A play ran before the drive's questions were asked, or an answer has no source.
- F4 — A play started before the one before it proved its done check, or on an unclean tree; or
  a capability `/vision` seeded was left directional.
- F5 — An answer came from the model alone: a question nothing supported was answered instead of
  asked; or the drive stopped to ask a question another of its plays, or a later round, could
  have answered; or it asked the person about something it had not shown them.
- F6 — The drive ended as done without the checker's pass.
- F7 — The drive changed an intent's state in the model, or recorded a decision on an intent
  without the person's own typed word.
- F8 — The drive closed with no evidence record.

## Context

ADR 029 (drives; Kickoff, §6), ADR 031 (business intent and ICE; only a person confirms an
intent, D10), ADR 032 and 033 (the review; approval in the model), ADR 034 (a play answers from
memory inside a drive), ADR 039 (the issue ID governs), `standards/rules/drive-contract.md`, the
Shared Drive Run (`../_shared/drive-run.md`). The #662 run proved the three plays run from
memory alone under one contract.

The plays' own content questions — who asks for each intent, how we will know it is met, a
capability's seed — depend on what the prototype shows, so the drive cannot ask them before
`/intent` reads it. A play that cannot answer one makes it the drive's question (C5); the
other plays, the next round and `/build-memory` may answer it, and the person is asked only what
none of them can (ADR 041). The drive asks first only what it can know up front.

Not built yet: ADR 029 §6 gives Kickoff a second output, a plan and its issues for the person,
with `approve-change` in its done check. This drive makes only the product model; the plan and
its issues are an open item on #613's plan, waiting on Kapil.

## Plays

| Order | Play | Inputs from the contract | Answers from the questions |
|-------|------|--------------------------|----------------------------|
| 1 | intent | `argument` — the prototype (path or link), handed on the play's command line | — |
| 2 | vision | — (it finds the proposed intents `/intent` saved in the model) | — |
| 3 | understand | — (it details every capability not yet detailed) | — |

## Questions first

Asked at pre-flight, before the drive opens anything, because the prototype check needs them (C2):

- Where is the working prototype — a file, a project folder or a link? → `inputs.intent.argument`
- For a file or a folder: how does it start? → `prototype.json` (`start`), the pre-flight's
  proof it runs
- For a link: may `/intent`'s walk press buttons that change data on it (pay, delete, submit)?
  → `answers.intent.may_change_data` (`true` only on the person's yes; a file or local
  prototype needs no answer — nothing real changes)

## Checker

`drives.kickoff.checker` — default `kind: subagent` on a model that is not the session's. It
judges this goal and these constraints against the drive's outputs only (`judge-drive-result`).

## Runner

`drives.kickoff.runner` — `subagent` (default) or `headless`. `drives.kickoff.max_rounds` —
the most rounds before the drive asks (default 3).

## End

Stand-in until the review tool (C7; Kapil, 2026-10-20, "2"): `commit-change` →
`propose-change` → **the person types confirm or drop for each proposed intent; the drive
records their words** in `confirmation.yaml` in its run folder (the intents stay `proposed` in
the model) → `review-change` → `merge-change`, the merge keeping its pinned approval. The
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
- S2 — business owner. Given no prototype, or a link that does not answer; then the drive halts
  before it opens an issue or a branch; measure: no new branch exists and the drive closed
  HALTED with `exit_reason: preflight`.
- S3 — business owner. Given a prototype where `/intent` cannot answer some questions on its
  own; then the drive goes on to `/vision` and `/understand`, runs `/intent` again on the next
  round with what they found, and asks the owner only what is still open — once, after showing
  the draft; measure: `round-1.json` reads `again` (not `ask`), every question asked appears in
  a `round-<n>.json` that reads `ask`, and each answer is in the issue's short-term memory with
  `from: person`.
- S4 — business owner. Given a run the checker rejects; then the drive halts with the
  checker's reasons and opens no pull request; measure: `check.yaml` reads `verdict: reject`
  with a reason for each failed criterion, and no pull request exists for the branch.

### Recovery

| For | Trigger | Direction | Handoff |
|-----|---------|-----------|---------|
| F1 | a write outside the issue, or a second issue or branch | move the record under the drive's issue; run on the contract's branch | autonomous |
| F2 | no prototype, or one that does not run | halt before opening; ask the person for a working prototype | human |
| F3 | a play ran before the questions, or an answer has no source | stop; ask the drive's questions, record each answer's source, re-run the play | autonomous |
| F4 | a play started early or on an unclean tree, or a capability left directional | halt; finish the earlier play or commit its run files; re-run `/understand` | autonomous |
| F5 | an answer from the model alone, or a stop for a question the drive could still answer | strip the answer, or go on round the loop; ask the person only what no play answers, after showing the draft; re-run the play | human |
| F6 | done without the checker's pass | run the checker; a reject halts the drive | autonomous |
| F7 | the drive changed an intent's state, or recorded a decision without the person's word | undo the change to the intent page; ask the person and record their own words | human |
| F8 | no evidence record | write the evidence before closing; the close stays HALTED until it exists | autonomous |

### Done means

- D1 — the drive's contract exists. Check: `artifact_exists` `contract.json`.
- D2 — `/intent` proved its done check. Check: `field_equals` `intent-done.json` `done` = `true`.
- D3 — `/vision` proved its done check. Check: `field_equals` `vision-done.json` `done` = `true`.
- D4 — `/understand` proved its done check. Check: `field_equals` `understand-done.json` `done` = `true`.
- D5 — the checker passed. Check: `field_equals` `check.yaml` `verdict` = `pass`.
- D6 — the person decided every proposed intent, in their own words. Check: `field_equals`
  `confirmation.yaml` `by` = `person`.
- D7 — no question is left open when the drive ends. Check: `field_equals` `rounds.json`
  `open_left` = `0`.
