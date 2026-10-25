# adr — ICE source

The clean ICE triple this play is compiled from. Update this and recompile via
edit-play; never hand-edit the compiled SKILL.md.

## Intent

Record a decision as an ADR, written from the one ADR template, with what it overrides and what
it changes in plain view. It becomes accepted only on a person's word, and every older ADR it
changes points forward to it.

### Constraints

- C1 — It starts from a decision brief: what is decided, why now, the options considered, who
  decides, and where it was decided — from the person, or from the play that made the
  decision.
- C2 — Every record is written from the one ADR template, in the shape the decision needs (a
  person-read record for the framework's own decisions, a structured record for a product
  decision), and passes the template's structural check. The play asks `template-manager`
  for the template (`standards/templates/adr.md`) and hands its short-term copy to `adr-keeper`
  in the contract; `adr-keeper` does not fetch the template itself.
- C3 — Every older ADR it supersedes or amends is named, with the part it changes. Candidates
  are found mechanically; which ones really apply is judged by reading them.
- C4 — What it changes is recorded with real names: the files, rules, schemas, plays and agents
  it affects, and its effect on agent intent (ICE).
- C5 — An ADR never changes a person's business intent. A decision that would is shown to the
  person and not applied — run by hand or inside a loop, where it is a new question that stops
  the loop; changing the Business Intent kind (framework doctrine) is allowed and recorded as
  such.
- C6 — Only a person accepts an ADR. Run by hand, the person accepts or rejects it before it is
  written as accepted (a pinned gate, class one-way-door: a record of a decision is the
  project's memory). Inside a loop there is no approval stop: it is saved as proposed and
  accepted at the loop's final review. A proposed ADR can later be accepted by hand, which
  completes it.
- C7 — An older ADR is never edited, except for its forward pointer, and pointers are written
  only once the new ADR is accepted.
- C8 — The index of the framework's ADRs is rebuilt after each one is accepted, so it is never
  stale.
- C9 — Additive and contained: run by hand, it starts from a clean record tree (no uncommitted
  change to the framework's ADRs or the product model); it writes only the new record, the
  forward pointers and the index; nothing else in the repository changes.
- C10 — Stands alone, or runs inside a loop: run by hand it opens and lands its own change;
  handed a loop's contract, it opens no issue or branch of its own and works on the loop's
  branch.
- C11 — The play ends by proving its done checks at close; it never reads COMPLETED with them
  unmet.

### Failure conditions

- F1 — A record was written without a decision brief, or the brief lacks the decision, the
  reason, or the options.
- F2 — A record does not follow the template, or fails its structural check; or the template
  did not come from `template-manager` through the play's contract.
- F3 — An older ADR the decision supersedes or amends is not named, or is named without the
  part it changes.
- F4 — What the decision affects, or its effect on agent intent, is missing or names things
  that do not exist.
- F5 — An ADR changed, or was applied as changing, a person's business intent.
- F6 — An ADR was marked accepted without a person, a rejected ADR was written, or a loop
  stopped to wait for approval.
- F7 — An older ADR was edited beyond its forward pointer, or a pointer was written before the
  new ADR was accepted.
- F8 — The index does not list an accepted framework ADR, or lists it with the wrong status.
- F9 — Run by hand from a record tree that was not clean, or something other than the new
  record, the pointers and the index changed.
- F10 — Run by hand, the change was not opened and landed; or, handed a loop's contract, the
  play opened an issue or a branch of its own.
- F11 — The run closed COMPLETED without its done checks held.

## Context

Decisions were recorded by hand: writing ADR 031 needed a manual search for the older ADRs it
amends, and the review of PR #631 found the gaps. Decided with Kapil on #632 (A1–A8): every form
of ADR, from one template in core memory with two shapes — Garura's Markdown ADRs and product
`decision.yaml` records; existing ADRs stay as written for now; a sub-agent gathers the context
and checks, a skill drafts, scripts do the mechanical work; a small play holds the person's
approval. ADR 031 sets the loop rule this play follows: a loop asks questions but never stops
for approval, and its final review accepts. Plays that make product decisions call the skill
directly and accept at their own review; this play is the by-hand path and the place a proposed
ADR is later accepted.

## Expectation

### Success scenarios

- S1 — (framework author, a new Garura ADR that amends older ones) Given a brief for a decision
  that changes parts of older ADRs, when `/record-decision` runs by hand and the person accepts, then the
  new ADR is written from the template, names each older ADR it changes with the part, and each
  of those older ADRs points forward to it. Measure: the manifest reads `decided: true`,
  `status: accepted`, `lint_ok: true` and `linked: true`; each older ADR named in the new one's
  Supersedes/Amends line carries a pointer to it on its Status line and is otherwise unchanged.
- S2 — (framework author, a decision that would change a business intent) Given a brief whose
  decision would change a person's business intent, when `/record-decision` runs, then the ADR is shown to
  the person and not applied. Measure: the guard exits 4; no new ADR file exists under the ADR
  folder; the run closes HALTED with `exit_reason: business_intent`.
- S3 — (product owner, a product decision) Given a brief for a product decision on a node, when
  `/record-decision` runs by hand and the person accepts, then a structured decision record is written for
  that node. Measure: the record passes the structural check, reads `status: accepted` with
  `metadata.accepted_by`, and names its node.
- S4 — (Discovery loop, inside a loop) Given a loop hands `/record-decision` its contract, when it runs,
  then it does not stop for approval: the ADR is saved as proposed, no pointer is written, and
  no issue or branch is opened. Measure: the run record reads `in_loop: true`; the manifest
  reads `status: proposed` and `pointers_deferred: true`; no older ADR changed.
- S5 — (framework author, rejects) Given the person rejects the drafted ADR, when the run
  reaches approval, then nothing is written. Measure: no new ADR file, no older ADR changed, the
  index unchanged; the run closes HALTED with `exit_reason: rejected`.
- S6 — (framework author, the index) Given an accepted framework ADR, when the run ends, then
  the ADR index lists it with its status. Measure: the index file has a row for the new number
  reading Accepted, and every ADR file in the folder has a row.

### Done means

Paths are relative to the run's working folder, `{stm_base}_adr/<run-ts>/` — fixed, because
run by hand the play starts before its issue exists.

- D1 — says: "the decision record was saved"
  check: { type: artifact_exists, path: "adr-manifest.json" }
- D2 — says: "it was decided — accepted by a person (by hand), or saved as proposed for the
  loop's final review"
  check: { type: field_equals, file: "adr-manifest.json", field: "decided", equals: true }
- D3 — says: "it follows the template"
  check: { type: field_equals, file: "adr-manifest.json", field: "lint_ok", equals: true }
- D4 — says: "every older ADR it changes points forward to it (or, when proposed, the pointers
  wait for acceptance)"
  check: { type: field_equals, file: "adr-manifest.json", field: "linked", equals: true }
- D5 — says: "nothing else in the repository changed"
  check: { type: field_equals, file: "guard-report.json", field: "ok", equals: true }

### Recovery (one per failure condition)

- REC1 (F1) — trigger: no brief, or the brief lacks the decision, the reason or the options.
  direction: ask the person (or the calling play) for what is missing; never fill it in.
  handoff: human.
- REC2 (F2) — trigger: the record fails the structural check, or the template did not come
  through the play's contract. direction: load the template through `template-manager`, hand
  its copy to `adr-keeper`, and re-draft against it with the check's report. handoff:
  autonomous.
- REC3 (F3) — trigger: an older ADR it changes is unnamed or has no part. direction: re-read
  the overlap candidates, name each one with the part, re-draft. handoff: autonomous.
- REC4 (F4) — trigger: affects or ICE impact missing or naming things that do not exist.
  direction: search the repository for the real names and re-draft. handoff: autonomous.
- REC5 (F5) — trigger: the decision would change a person's business intent. direction: stop
  before writing; show the person which intent and why; the person changes the brief or ends
  the run. handoff: human.
- REC6 (F6) — trigger: accepted without a person, a rejected ADR written, or a loop waited.
  direction: reset to proposed (or remove the rejected file); by hand, present and record only
  the person's own word; in a loop, save as proposed and move on. handoff: human.
- REC7 (F7) — trigger: an older ADR edited beyond its pointer, or a pointer written early.
  direction: restore the older ADR from git and re-write only the pointer, after acceptance.
  handoff: autonomous.
- REC8 (F8) — trigger: the index is stale. direction: rebuild it from the ADR folder.
  handoff: autonomous.
- REC9 (F9) — trigger: the record tree was not clean at the start, or a path outside the new
  record, the pointers and the index changed. direction: before writing, stop and ask the person
  to commit or set aside the open changes; after writing, restore the offending paths from git,
  after a person confirms. handoff: human.
- REC10 (F10) — trigger: by hand without opening or landing the change, or an issue or branch
  opened inside a loop. direction: by hand, run the missing opening or end step; in a loop,
  close the stray issue and branch and continue on the loop's branch. handoff: human.
- REC11 (F11) — trigger: the close would read COMPLETED with done checks unmet. direction:
  close HALTED with the unmet checks named; fix and re-evaluate. handoff: autonomous.
