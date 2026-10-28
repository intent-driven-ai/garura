# Severity — how a review finding and a defect get P1 to P4

**Purpose:** a finding that needs judgment — a design-conformance finding of `/check-change`,
a defect found in a review or in a run, a Bug filed in the tracker — gets its severity from
these rules, never from a feeling. The mechanical findings of `check-pr-quality` keep their
table (`standards/rules/pr.md`); this page covers everything that table cannot match.

Set by the product owner, 2026-10-28, on PR #932 (round 1): "you are categorising some defect
wrong … defect identification should mark the severity." The four calls of that review are the
first examples below.

## First: is it a defect at all?

A finding is a **defect** when something the change made, or something already there, behaves
differently from what was intended. It is **a change, not a defect** when the change adds
something new that a neighbouring part does not know about yet: a new field that a schema or a
linter does not list, a new page an index does not name yet. A change gets no severity. It is
work the change owes: do it in the same change, or file it as a Story.

## Then: ask in this order; the first that fits is the severity

- **P1 — Blocker. It must be fixed before the merge.**
  1. The change breaks the rule it sets out to enforce, or a guardrail of the harness: memory is
     reached only through the memory tool; only agents call the memory tool; a play reads no
     memory; an installed part reads only installed files; no write outside the issue's scope;
     only a person decides what a person decides.
  2. A run can no longer reach done: a check that can never pass, a record written where its
     reader never looks, a step that halts every run.
  3. Data is lost, a secret is exposed, or a security hole opens (the P1 rows of `pr.md`).
- **P2 — Major. Fix it in this change unless the person says otherwise.** An instruction that
  an agent, a play or a person follows invites a forbidden act or a wrong result, though nothing
  has done it yet: a loophole. Or a guarantee is weakened: a guard still runs, but lets more
  through than its rule allows.
- **P3 — Minor.** A check, a guard or a link silently covers less than before: something that
  used to be caught is no longer caught, and nothing has gone wrong yet.
- **P4 — Nit.** Wording, wrapping, a count in prose, a stale line that misleads no decision.

A severity always names its rule: `P1 (1)`, `P2`, `P3`. A finding whose rule cannot be named is
not finished.

## Examples, from several kinds of work

| Severity | Example | Rule |
|----------|---------|------|
| P1 | A script added by the change that makes "only agents call the memory tool" true itself calls the memory tool (PR #932, H-2) | 1 |
| P1 | A fix for double payments that retries the charge without the payment's idempotency key | 1 |
| P1 | A play writes its done record under its old name, so its loop's done check never finds it and no round can pass (#923) | 2 |
| P1 | A nightly import that now drops every row with an empty optional column | 3 |
| P2 | An agent's instructions say a memory page "is a repository file: read it as one", which invites an installed agent to read memory by its path (PR #932, H-1) | — |
| P2 | A runbook step says "if it hangs, restart with --force", and --force skips the backup | — |
| P3 | Two lines removed from the rename map, so the old-name check stops catching two retired names (PR #932, F1) | — |
| P3 | A test fixture removed with its feature, so one edge case of a kept feature is no longer tested | — |
| P4 | A page says "six" change plays where its table lists five (PR #932, F3) | — |
| change | A new field in the ADR template that the decision schema and the ADR linter do not list yet (PR #932, F2) | — |

## Where the severity is written

- **A review finding:** its `severity` field, with the rule in its `basis`. `compute_verdict.py`
  rejects on any P1.
- **A Bug in the tracker:** the first line of its text, `Severity: P<n> (<rule>) — <why, in one
  line>`. It is never a label (no labels for now, `managing-work.md`).
- **A defect found inside a run:** the run's own record of it carries the same line.

When the person sets a severity, theirs stands, and the case is added here as an example.
