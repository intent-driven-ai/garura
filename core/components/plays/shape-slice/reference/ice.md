# shape-slice — ICE source

The clean ICE triple this play is compiled from. Update this and recompile via
edit-play; never hand-edit the compiled SKILL.md.

## Intent

A person names a business intent. /shape-slice shapes the one slice that a person can test end
to end to show the intent is served. It fills the product model with what that slice needs, and
writes the slice with its link to the intent. It does nothing else: no plan, no epic, no story,
no eval.

### Constraints

- C1 — The entry is a business intent's issue number. The run reads the intent from the product
  model, never from the issue text alone. When the model has no page for the intent, the run
  writes that page from the issue, and says so; it does not stop.
- C2 — The run reads the product model and memory first. It asks the person only about what
  neither of them answers.
- C3 — The questions follow the shared rule for asking a person: all at once, an opening that
  says what the person decides, and for each question one thing, with Question, Answer, Why it
  matters and Example (several domains), each able to stand alone.
- C4 — The run asks no more questions than the configured question tier allows. Questions only
  the person can answer (blocking) are always asked and count first. Every gap left open because
  of the budget is written as an assumption, and the person sees each assumption at the
  checkpoint.
- C5 — Every question and every answer is recorded in the issue's short-term memory. A question
  already answered there is never asked again.
- C6 — The slice holds features from any capability, in build order. It names one person who
  tests it and the one surface they test it on. A slice with no such person or surface is not
  written; the run says why.
- C7 — A slice that already serves the intent (it lists the intent, or it has the same features
  and the same surface) is reused: the run adds the intent to it and makes no new slice.
- C8 — The run fills the model. A domain, capability, feature or ICE that the slice needs and
  the model lacks is added at the depth the run knows, and marked to be deepened later. Nothing
  the slice needs is skipped.
- C9 — The run writes only: the slice (its features in build order, its surface, the business
  intents it serves), the slice's record, and what C1 and C8 add. A slice links to
  capabilities, and through them to its domains; it has no domain home.
- C10 — A proposed answer to a question traces to a source the run can name (model, memory, or
  a person's earlier answer). Where it cannot, the question carries no proposed answer, and the
  run reports how many questions have none.
- C11 — The product model's own checks pass after the write: the structure and link check, and
  the old-name guard.
- C12 — The person approves at a typed checkpoint (yes / change / stop) before anything is
  committed. A change goes back and is shown again. A stop undoes every write.
- C13 — The run opens its own change and lands it through the change plays; when the intent is
  in a plan, it lands on the plan's branch.
- C14 — Every page a person reads is in plain English (ASD-STE100), uses personas, and names no
  real person.

### Failure conditions

- F1 — The run worked from the issue text alone, or stopped because the model had no page for
  the intent.
- F2 — The run asked a question that the model or memory already answers.
- F3 — A question broke the rule for asking a person (not all at once, more than one thing,
  a part missing, or it cannot stand alone).
- F4 — The run asked more questions than the tier allows (beyond the blocking ones), or left a
  gap open with no written assumption, or the person did not see an assumption.
- F5 — A question or answer was not recorded, or an answered question was asked again.
- F6 — A slice was written with no tester, with no surface, or with more than one surface.
- F7 — A new slice was made for an intent that an existing slice already serves.
- F8 — A part the slice needs was skipped instead of added to the model.
- F9 — The run wrote something outside C9: a plan, an epic, a story, an eval, or another file.
- F10 — A proposed answer has no source the run can name, or the count of questions with no
  proposed answer is missing or wrong.
- F11 — The model's checks fail, and the run went on.
- F12 — Something was committed without the person's yes, or a stop left writes behind.
- F13 — The change landed outside the change plays, or on the wrong branch.
- F14 — A page names a real person, or a person cannot follow it.

## Context

- The product model: `core/components/memory/standards/schemas/product-os/ontology.md` (v10:
  Slice, Business Intent, Q25–Q35); `spine.yaml` and `slice.yaml` schemas; ADR 049 (the shaping
  loop: /shape-slice, then the plan play, then the eval play).
- The rules: `standards/rules/asking-a-person.md`, `standards/rules/user-questions.md`,
  `standards/rules/no-unbacked-recommendation.md`.
- The question tier: `shape-slice.grill-tier` in config (xs 5, s 12, m 25, l 45, xl 70; default
  m), and the budget script built for #817.
- The agent that gathers model and memory and runs the skills: `product-os-keeper`.
- The product owner's decisions for this play: `.garura/project/issues/795/context/decisions.md`.
- Personas: the product owner (gives the intent, answers, approves); the plays after it in the
  shaping loop (the plan play #818, the eval play #798), which read the slice.

## Expectation

### Success scenarios

- S1 — (product owner, a new slice) Given a confirmed business intent with a model page and no
  slice that serves it, when the run ends, then one slice is in the model with features in
  build order, one surface with its tester, and the intent in its `intents`; the model's
  checks pass; the commit exists only after a typed yes. Measure: the slice check reads valid,
  the approval record reads yes, and the write report lists only allowed paths.
- S2 — (product owner, no intent page) Given an intent issue that the model has no page for,
  when the run ends, then the model has the intent's page, written from the issue, and the run
  said so; the slice is shaped as in S1. Measure: the intent page exists, and the run record
  names it as written by this run.
- S3 — (product owner, a slice already serves) Given an intent that an existing slice already
  serves (same features and surface), when the run ends, then no new slice is made and the
  intent is in that slice's `intents`. Measure: the spine has the same number of slices, and
  the existing slice lists the intent.
- S4 — (product owner, a small budget) Given tier xs (5) and 8 gaps, 2 of them blocking, when
  the questions are shown, then at most 5 are asked, both blocking ones among them, and the
  other gaps are shown as written assumptions at the checkpoint. Measure: the question record
  holds 5 or fewer asked questions including both blocking ones, and one assumption for each
  gap not asked.
- S5 — (product owner, no surface) Given an intent for which no person can test anything end to
  end, when the run ends, then no slice is written, and the run says why. Measure: the spine's
  slices are unchanged, and the run record holds the reason.
- S6 — (product owner, stop at the checkpoint) Given a shaped slice, when the person types
  stop, then the model is as it was before the run, and nothing is committed. Measure: the
  model tree has no change against the run's start, and no commit was made.

### Done means

- D1 — the slice check report exists and reads valid.
  check: { type: field_equals, file: "context/shape-slice/slice-check.json", field: "valid", equals: true }
- D2 — the person's approval is recorded as yes.
  check: { type: field_equals, file: "context/shape-slice/approval.json", field: "decision", equals: "yes" }
- D3 — the write report shows only allowed paths were written.
  check: { type: field_equals, file: "context/shape-slice/guard-report.json", field: "ok", equals: true }
- D4 — the question record exists, with every question and answer of the run.
  check: { type: artifact_exists, path: "context/grounding-questions.md" }
- D5 — the trace check of the run's decisions names no decision whose source is gone or
  changed.
  check: { type: field_equals, file: "context/shape-slice/citations-check.json", field: "problems", equals: [] }

### Recovery (one per failure condition)

- REC1 (F1) — read the intent from the model; write the missing page from the issue, then go
  on. Handoff: autonomous.
- REC2 (F2) — drop the question, and use the answer the model or memory gives. Handoff:
  autonomous.
- REC3 (F3) — rewrite the questions to the rule and show them again. Handoff: autonomous.
- REC4 (F4) — cut the questions to the budget, blocking first, and write an assumption for
  every gap not asked; show the assumptions at the checkpoint. Handoff: autonomous.
- REC5 (F5) — record every question and answer, and take back any repeat question. Handoff:
  autonomous.
- REC6 (F6) — do not write the slice; ask for the tester or the surface, or say why there is
  none. Handoff: human.
- REC7 (F7) — remove the new slice, and add the intent to the slice that already serves it.
  Handoff: autonomous.
- REC8 (F8) — add the skipped part at the depth known, marked to be deepened. Handoff:
  autonomous.
- REC9 (F9) — undo the write outside the allowed set. Handoff: autonomous.
- REC10 (F10) — strip the proposed answer that has no source (never replace it with another),
  and report the count. Handoff: autonomous.
- REC11 (F11) — fix each problem the check lists, and run the check again; the run does not go
  on until it passes. Handoff: autonomous.
- REC12 (F12) — take the commit back, or undo the writes a stop left. Handoff: human.
- REC13 (F13) — land the change through the change plays, on the branch the target script
  gives. Handoff: human.
- REC14 (F14) — rewrite with personas and plain words. Handoff: autonomous.
