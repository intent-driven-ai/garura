# Severity — how a finding or a defect in a harness gets P1 to P4

**Purpose:** any team that builds an agentic harness on the Phoenix architecture gives its
findings and defects a severity by the same rules. These rules cover what needs judgment: a
design finding of a review, a defect found in a review or in a run, a Bug filed in the
tracker. Findings that a mechanical table matches keep that table (`standards/rules/pr.md`).

## The parts of a Phoenix harness these rules speak of

- **Play** — a workflow: steps, checks and a close. It does no judgment of its own.
- **Loop** — a play that runs other plays in rounds until its intent is met.
- **Agent** — gathers context and decides; the only part that reads memory.
- **Skill** — produces one artifact from what its agent hands it.
- **Script / tool** — mechanical work with no judgment: a check, a writer, a linter.
- **Memory** — tiers from short-term (the work item's own) to shared, reached through the
  **memory tool**.
- **Installed copy** — the parts as an install laid them in a project.

## The guardrails of the architecture

A defect that breaks one of these is P1, whatever else it does:

1. Memory is reached only through the memory tool. Nothing reads, lists or compares a
   memory file by its path.
2. Only agents call the memory tool. A play, a loop, a skill or a script does not, except a
   script the architecture's own decision names, and then only read-only.
3. A play or a loop reads no memory itself; its agents do.
4. An installed part reads only installed files, never the harness's source.
5. Every write stays inside the work item's scope. A new memory goes to short-term memory
   first, and moves up only when a person promotes it.
6. Only a person decides what a person decides: accepting a decision, confirming an intent,
   merging a change.

## First: is it a defect at all?

A finding is a **defect** when something behaves differently from what was intended. It is
**a change, not a defect** when the work adds something new that a neighbouring part does not
know about yet: a new field that a schema or a linter does not list, a new page that an index
does not name. A change gets no severity. It is work the change owes: do it in the same
change, or file it as a Story.

## Then: ask in this order; the first that fits is the severity

- **P1 — Blocker. Fixed before the merge.**
  1. A guardrail above is broken, or the change breaks the very rule it sets out to enforce.
  2. A run can no longer reach done: a check that can never pass, a step that halts every run.
  3. Data is lost, a secret is exposed, or a security hole opens.
- **P2 — Major. Fixed in this change unless the person says otherwise.**
  - An instruction that an agent, a play or a person follows invites a forbidden act or a
    wrong result, though nothing has done it yet: a loophole.
  - A guarantee is weakened: a part still works, but on less than its rule promises (a skill
    that should rest its answers on memory is handed none).
- **P3 — Minor.** A check, a guard or a link silently covers less than before: something that
  used to be caught is no longer caught, and nothing has gone wrong yet.
- **P4 — Nit.** Wording, wrapping, a count in prose, a stale line that misleads no decision.

A severity always names its rule: `P1 (guardrail 2)`, `P1 (2)`, `P2 (loophole)`. A finding whose
rule cannot be named is not finished.

**A defect that is a byproduct of another** — it exists only because of a defect already filed,
and is fixed with it — takes the severity of its own effect, and its text names the defect it
comes from.

## Examples, from several kinds of work

| Severity | Example | Rule |
|----------|---------|------|
| P1 | A script added to make "only agents call the memory tool" true calls the memory tool itself | guardrail 2 |
| P1 | A skill raises its draft through the memory tool, though only its agent may | guardrail 2 |
| P1 | An agent compares memory pages by their file paths instead of through the memory tool | guardrail 1 |
| P1 | A loop's pre-flight names its plays by old names, so every run halts before it starts | 2 |
| P1 | A fix for double payments that retries the charge without the payment's idempotency key | 1 |
| P1 | A nightly import that now drops every row with an empty optional column | 3 |
| P2 | An agent's instructions say a memory page "is a file: read it as one", which invites a read by path | loophole |
| P2 | A skill that should rest its proposals on memory is handed none, so every proposal rests on less | weakened guarantee |
| P2 | A runbook step says "if it hangs, restart with --force", and --force skips the backup | loophole |
| P3 | Two retired names dropped from a rename map, so the old-name check no longer catches them | — |
| P3 | A test fixture removed with its feature, so one edge case of a kept feature is no longer tested | — |
| P4 | A page counts six parts where its own table lists five | — |
| change | A new field in a decision template that the decision schema and its linter do not list yet | — |

## Where the severity is written

- **A review finding:** its `severity` field, with the rule in its `basis`. A review rejects on
  any P1.
- **A Bug in the tracker:** the first line of its text, `Severity: P<n> (<rule>) — <why, in
  one line>`. Not a label.
- **A defect found inside a run:** the run's own record of it carries the same line.

When the person sets a severity, theirs stands. When it differs from these rules, the rules
are corrected, or the case is added as an example, in the same change.
