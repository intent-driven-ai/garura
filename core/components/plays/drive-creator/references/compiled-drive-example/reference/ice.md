# ICE — sample-drive

A worked example of a drive's ICE, for `/drive-creator` and the drive linter's tests. It
runs two plays, `/intent` then `/vision`.

## Intent

**Goal:** from a written statement of what a product is for, end with proposed business
intents and a seeded domain, on one branch, with no stop except a question memory cannot
answer.

### Constraints

- C1 — The drive works on one issue and one branch; everything it and its plays write is under
  that issue.
- C2 — The drive asks its questions before any play runs; a question memory and the answers do
  not cover stops the drive and goes to the person.
- C3 — The plays run in the fixed order `/intent` → `/vision`; each must prove its own done
  check before the next one starts.
- C4 — A checker that is not the drive's own model checks the result, and a reject halts the
  drive.

### Failure conditions

- F1 — A play wrote outside the drive's issue, or the drive opened a second issue or branch.
- F2 — A play ran before the drive's questions were asked, or a play picked an answer for a
  question nothing supported.
- F3 — A play started while the one before it had not proven its done check, or on an unclean
  tree.
- F4 — The drive ended as done without a checker's pass.

## Context

ADR 029 (drives), ADR 034 (a play answers from memory inside a drive), ADR 039 (the issue ID
governs), `standards/rules/drive-contract.md`.

## Plays

| Order | Play | Inputs from the contract | Answers from the questions |
|-------|------|--------------------------|----------------------------|
| 1 | intent | `statement` — the written statement | `who_asks`, `proof` |
| 2 | vision | `intents` — after `/intent`: the intents it saved (the drive adds them to the contract before `/vision` starts) | — |

## Questions first

- Who asks for this product? → `answers.intent.who_asks`
- How will we know it worked? → `answers.intent.proof`

## Checker

`drives.sample-drive.checker` — checks the Done means against the drive's outputs only.

## Runner

`drives.sample-drive.runner` — `subagent` (default) or `headless`.

## End

The injected end sequence: `commit-change` → `propose-change` → `review-change` →
`merge-change`, the merge keeping its pinned human approval.

## Expectation

### Success scenarios

- S1 — product owner. Given a written statement and answers to both questions; then both plays
  run, the checker passes, and one pull request carries the change; measure: the contract,
  both plays' done verdicts reading held, and the checker's `pass` exist under the issue.
- S2 — product owner. Given a statement where `/vision` stops on a question no memory answers;
  then the drive brings the question to the person and resumes the same play with the answer;
  measure: the answer is in the issue's short-term memory and `/vision`'s done verdict reads
  held.

### Recovery

| For | Trigger | Direction | Handoff |
|-----|---------|-----------|---------|
| F1 | a write outside the issue, or a second issue or branch | move the record under the drive's issue and run on the contract's branch | autonomous |
| F2 | a play ran before the questions, or answered from nothing | stop, ask the person, record the answer, re-run the play | human |
| F3 | a play started before the last one proved done, or on an unclean tree | halt; finish or fix the earlier play, commit its run files, resume | human |
| F4 | the drive would end done with no checker pass | run the checker; a reject halts the drive | autonomous |

### Done means

- D1 — the drive's contract exists. Check: `artifact_exists` `contract.json`.
- D2 — `/intent` proved its done check. Check: `field_equals` `intent-done.json` `done` = `true`.
- D3 — `/vision` proved its done check. Check: `field_equals` `vision-done.json` `done` = `true`.
- D4 — the checker passed. Check: `field_equals` `check.yaml` `verdict` = `pass`.
