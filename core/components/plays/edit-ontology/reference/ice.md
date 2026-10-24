# edit-ontology — ICE source

The clean ICE triple this play is compiled from. Update this and recompile via
edit-play; never hand-edit the compiled SKILL.md.

## Intent

A person changes Garura's product ontology — its kinds, their links and their rules — one
need at a time. Every change is agreed with the product owner, checked by a script, and
landed through the change plays.

### Constraints

- C1 — Every run works on one need, and changes only the kinds that need touches.
- C2 — The product owner decides. The run stops for a typed yes at three points: the
  questions the ontology must answer, the kinds, and the links and rules. Nothing is
  written as agreed before that yes.
- C3 — Reuse before you invent. An existing kind is never redefined without a log line that
  says so.
- C4 — Every page a person reads is in ASD-STE100 plain English, uses personas and never
  names, and has a real example. Every draft shown at a checkpoint follows the shared rule
  for asking a person (`_shared/asking-a-person.md`): an opening that says what the
  person decides, and each question with Question / Answer / Why it matters / Example, the
  example from several domains.
- C5 — A script decides whether the ontology is valid, not the model. The run ends only when
  the ontology check passes.
- C6 — The ontology version goes up by one, the date is set, and one log line says what
  changed and why.
- C7 — The run opens its own change, and lands it through commit-change, propose-change,
  check-change and merge-change. When the issue is in a plan, it lands on the plan's branch.
- C8 — The play runs the ontology skill. A person never runs the skill directly.

### Failure conditions

- F1 — The run changed a kind that its need does not touch.
- F2 — Something was written as agreed without the product owner's yes at one of the three
  points.
- F3 — An existing kind changed meaning, and no log line says so.
- F4 — A page names a real person, or a person cannot follow it, or a checkpoint draft does
  not follow the rule for asking a person.
- F5 — The run closed while the ontology check still failed.
- F6 — The version, the date or the log line is missing.
- F7 — The change landed outside the change plays, or on the wrong branch.
- F8 — The ontology skill ran outside this play.

## Context

- The ontology: `core/components/memory/standards/schemas/product-os/ontology.md` (source; the
  installed copy is read-only).
- The skill that does the work: `author-product-ontology` (seven steps; its check
  `check_ontology.py`).
- The agent that gathers sources and runs the skill: `product-os-keeper`.
- The format: `standards/templates/product-ontology.md`.
- The rule for asking a person: `_shared/asking-a-person.md`, the shared file the install
  lays beside the installed skills. It is not memory. In the three draft stages,
  `product-os-keeper` passes its path to the skill as the input `asking_rule`; nothing looks
  for it through the memory tool.
- Persona: the product owner, who decides; the agents and plays that read the ontology.

## Expectation

### Success scenarios

- S1 — (product owner, a new kind) Given the need "the ICE as its own kind", when the run
  ends, then the ontology has the ICE kind with its properties, links, rules and a real
  example; the version goes from 5 to 6, with one log line; and the change is merged into
  the plan's branch. Measure: the ontology check reads valid, and the PR is merged into the
  branch the target script gives.
- S2 — (product owner, a change at a checkpoint) Given a run waiting at the kinds
  checkpoint, when the product owner types a change, then the run applies it and asks again,
  and nothing is written as agreed until the product owner types yes. Measure: the decision
  record holds one yes for each of the three checkpoints, each recorded after its draft was
  shown.
- S3 — (reviewer, scope) Given a need that touches one kind, when the change is reviewed,
  then only that kind, the kinds it links to, the questions, the version and the log
  changed. Measure: the scope report lists no other kind as changed.
- S4 — (reader, plain words) Given the new kind's text, when a newcomer reads it, then it
  holds no real names and has a real example. Measure: the name check finds no name, and the
  kind has an example.
- S5 — (product owner, a check that fails) Given an ontology that fails the check, when the
  run reaches its end, then it fixes the problems and runs the check again, and it never
  lands while the check fails. Measure: the last check report reads valid.

### Done means

- D1 — the ontology check report exists and reads valid.
  check: { type: field_equals, file: "context/edit-ontology/ontology-check.json", field: "valid", equals: true }
- D2 — the decision record holds a yes for each of the three checkpoints.
  check: { type: field_equals, file: "context/edit-ontology/decisions.json", field: "all_agreed", equals: true }
- D3 — the scope report says only the kinds the need touches changed.
  check: { type: field_equals, file: "context/edit-ontology/change-check.json", field: "scope_ok", equals: true }
- D4 — the version is up by one, the date is today, and there is one new log line.
  check: { type: field_equals, file: "context/edit-ontology/change-check.json", field: "version_ok", equals: true }

### Recovery (one per failure condition)

- REC1 (F1) — undo the change to the out-of-scope kind, and show it to the product owner as
  a separate need. Handoff: autonomous.
- REC2 (F2) — take the unagreed write back to draft, and ask again at that checkpoint.
  Handoff: human.
- REC3 (F3) — add the log line that names the changed meaning, or undo the change. Handoff:
  autonomous.
- REC4 (F4) — rewrite the text with personas and plain words, in the shape the rule for
  asking a person gives, and run the name check again. Handoff: autonomous.
- REC5 (F5) — fix each problem the check report lists, and run the check again; the run
  stays open until the check passes. Handoff: autonomous.
- REC6 (F6) — set the version, the date and the log line, and run the check again. Handoff:
  autonomous.
- REC7 (F7) — stop; land the change through the change plays, on the branch the target
  script gives. Handoff: human.
- REC8 (F8) — throw away a result the skill made outside the play, and run it through this
  play. Handoff: autonomous.
