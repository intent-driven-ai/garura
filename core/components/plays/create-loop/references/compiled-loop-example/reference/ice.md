# ICE — sample-loop

A worked example of a loop's ICE, for `/create-loop` and the loop linter's tests. It
runs two plays, `/discover-intent` then `/discover-domains`.

## Intent

**Goal:** from a written statement of what a product is for, end with proposed business
intents and a seeded domain, on one branch, running its plays in rounds and asking the person
only what none of its plays, memory or approved research answers.

### Constraints

- C1 — The loop works on one issue and one branch; everything it and its plays write is under
  that issue.
- C2 — The loop asks its own questions before any play runs and reads no memory itself. A
  question one play cannot answer is the loop's, not a stop: the play records it and finishes
  what it can, and the other play, the next round or the knowledge step may answer it. The loop
  briefs the person only on what none of them can — a few gaps, each with its context and our
  proposed answer (ADR 041, ADR 059).
- C3 — The plays read the statement independently and each writes its own kind — `/discover-intent`
  business intents, `/discover-domains` domains — in rounds until the loop's job is done; no play takes
  another's output as its input; after each round the loop's gap skills link what they wrote
  and give the work still missing to the play that does it (ADR 043). Each play proves its own
  done check, and the round is committed once.
- C4 — A checker that is not the loop's own model checks the result, and a reject halts the
  loop.

### Failure conditions

- F1 — A play wrote outside the loop's issue, or the loop opened a second issue or branch.
- F2 — A play ran before the loop's questions were asked, a play picked an answer for a
  question nothing supported, or the person was asked something a play, memory or approved
  research answers.
- F3 — A play took another play's output as its input, or started on an unclean tree; or the
  loop ended done with a node not linked.
- F4 — The loop ended as done without a checker's pass.

## Context

ADR 029 (loops), ADR 034 (a play answers from memory inside a loop), ADR 039 (the issue ID
governs), ADR 041 (rounds; a play's question is the loop's), `standards/rules/loop-contract.md`.

## Plays

| Order | Play | Inputs from the contract | Answers from the questions |
|-------|------|--------------------------|----------------------------|
| 1 | discover-intent | `statement` — the written statement | `who_asks`, `proof` |
| 2 | discover-domains | `goal` — the written statement (it reads no other play's output; ADR 043) | — |

## Questions first

- Who asks for this product? → `answers.discover-intent.who_asks`
- How will we know it worked? → `answers.discover-intent.proof`

## Checker

`loops.sample-loop.checker` — checks the Done means against the loop's outputs only.

## Runner

`loops.sample-loop.runner` — `subagent` (default) or `headless`.

## End

The injected end sequence: `commit-change` → `propose-change` → `check-change` →
`merge-change`, the merge keeping its pinned human approval.

## Expectation

### Success scenarios

- S1 — product owner. Given a written statement and answers to both questions; then both plays
  run, the checker passes, and one pull request carries the change; measure: the contract,
  both plays' done verdicts reading held, and the checker's `pass` exist under the issue.
- S2 — product owner. Given a statement where `/discover-domains` leaves a question no play or memory
  answers; then `/discover-domains` records it and finishes, the knowledge step runs, the loop shows the
  brief and the person confirms or corrects our proposed answer, and the next round fills it; measure: the answer is in the
  issue's short-term memory with `from: person`, and `/discover-domains`'s done verdict reads held.

### Recovery

| For | Trigger | Direction | Handoff |
|-----|---------|-----------|---------|
| F1 | a write outside the issue, or a second issue or branch | move the record under the loop's issue and run on the contract's branch | autonomous |
| F2 | a play ran before the questions, answered from nothing, or the person was asked what a play or memory answers | ask the loop's own questions first; send an unanswered question to the loop (`open-<play>.json`), run the knowledge step, brief the person on what is left, then run the next round | human |
| F3 | a play took another's output, an unclean tree, or done with a node not linked | halt; re-run the play on the statement alone; commit the round; run the gap skills and the plays they give work to | human |
| F4 | the loop would end done with no checker pass | run the checker; a reject halts the loop | autonomous |

### Done means

- D1 — the loop's contract exists. Check: `artifact_exists` `contract.json`.
- D2 — `/discover-intent` proved its done check. Check: `field_equals` `discover-intent-done.json` `done` = `true`.
- D3 — `/discover-domains` proved its done check. Check: `field_equals` `discover-domains-done.json` `done` = `true`.
- D4 — the checker passed. Check: `field_equals` `check.yaml` `verdict` = `pass`.
