# Pipeline Position

Single source of truth for how a play declares where it sits in the delivery pipeline and
what start/end machinery build-play folds into it. This is the D2 auto-build rule (#434):
the composition lives here once, so every play build-play compiles wires the same
start-work opening and the same commit → propose → review → merge closing — instead of
each play re-deciding how a change is opened and landed.

It governs only the **delivery pipeline** (the path that opens an issue, does the work, and
lands it on main). Every play declares where it sits; many model-building plays now open and
land their own change. As compiled today: `both` — /specify-domains, /specify-capabilities (#616), /shape-measure-lens,
/design-slice, /learn-outcomes, /fix-work, /refactor-work, /specify-intent (#612), /design-adr (#632), /specify-ontology (#777 — a meta play that opens and lands its own change); `start` — /design-architecture, /design-surface, /build-work; `end` —
/shape-marketing-lens, /design-env, /validate-uat; `none` — /design-agentic, /design-quality, /validate-slice, /release-increment,
/list-issues. (A `none` play runs on whatever branch is already started.) Inside a loop the
opening and the end sequence are both skipped — the loop opens and lands the change — and a
play knows it is inside a loop from the loop's contract (`standards/rules/loop-contract.md`;
ADR 029, ADR 030 P4). Wired so far: /specify-intent (#612, its own contract check), and /specify-domains (#614) and
/specify-capabilities (#615), both with the shared `check_loop_contract.py`.

## The declaration

Every play declares one frontmatter field:

```yaml
position: start | end | both | none
```

- **none** (default) — standalone play; nothing is injected. Strategic/model-building
  plays and one-off utilities use this.
- **start** — the play opens a pipeline. build-play injects **start-work** as the
  play's first step: resolve or create the issue, cut its branch, set up a worktree when config
  asks for one, and init STM. An issue in a plan gets `plan/<plan-id>/<issue>-<slug>`, cut from
  its plan's branch `plan/<plan-id>/base`; an issue in no plan gets a branch off fresh main.
- **end** — the play closes a pipeline. build-play injects the **end sequence** as the
  play's closing steps, in order: **commit-work → review-work → validate-work →
  merge-work**, placed after the play's own work and before the Standard Play Close.
- **both** — the play is self-contained: start-work is injected at the front and the end
  sequence at the back, bracketing the play's own work. This is the "start, do everything,
  close the loop" shape — e.g. a `fix-defect` play that opens the issue, fixes it, and
  lands it in one command.

There are only these positions. There is no "middle" — a play's own work simply sits
between the injected start and end; the work is not a declared position.

## The two sequences

| Sequence | Member plays (in order) | Injected when position is |
|----------|-------------------------|---------------------------|
| start | `start-work` | `start` or `both` |
| end | `commit-work` → `review-work` → `validate-work` → `merge-work` | `end` or `both` |

These five plays are the **members** — the building blocks. A member play declares the
`position` of the sequence it belongs to (`start-work: start`; the four end plays: `end`)
so build-play knows the sequence composition. **A member is never injected into itself**:
build-play recognizes the members by name and injects no sequence into one of them.
Everything else with a non-`none` position is a **consumer** that receives injection.
"Member" means only these change plays: no step of a loop is a member play (ADR 059).

## How build-play injects it (explicit, named)

Injection is explicit, not a hidden macro. The injected pieces appear as named sub-play
steps in the compiled play, wired as JSON-contract handoffs over files on disk (the same
discipline as any other step) and run as sub-plays — each is dispatched with
`parent_run_id` so it emits only its C1 evidence and the parent's close absorbs it (per
`_shared/play-close.md` (beside the plays)).

- **start** → prepend a first step that runs `start-work`, before the play's own first
  work step. The play's Task DAG gains that step at the head; everything else `blockedBy`
  it.
- **end** → append four closing steps that run `commit-work`, then `review-work`, then
  `validate-work`, then `merge-work`, each `blockedBy` the previous, after the play's last
  work step and before the Evidence & Close step. validate-work's verdict gates
  merge-work (a reject stops the sequence; the config `review-pr.bypass` governs whether
  it hard-blocks).
- **both** → both of the above, bracketing the work.

The compiled play shows each injected piece by name in its Workflow and Task DAG — a reader
sees exactly what runs and a partial/resumed run is followable. build-play does NOT
collapse the end sequence into one opaque "close the change" step.

## Relationship to start-work / the end plays

This rule defines the *composition*; the member plays define the *behavior*. They converge:
build-play injects calls to the member plays — it never re-implements their steps inline.
A consumer play that hand-rolls its own issue/branch/PR/merge steps instead of declaring a
position and receiving the injection is a violation (it duplicates and drifts from the
members).

## Enforced

Two layers — what the linter checks mechanically, and what build-play enforces at
compile.

**Linter (`scripts/lint_play.py`, per-compile, mechanical):**
- The frontmatter MUST carry a `position` field with one of `start | end | both | none`.
  Missing or invalid ⇒ lint failure. (`position` is required on compiled
  delivery/consumer plays; strategic, model-building, and meta plays are `none` — except a meta play that opens and lands its own change, which is `both`.)

**build-play (compile time):**
- For a **consumer** play (position not `none`, name not a member): build-play injects
  the member calls for the declared position in the required place — `start-work` at the
  head of the Task DAG; the end sequence as the ordered closing steps before the Standard
  Play Close (step 4b).
- For a **member** play: never inject its own sequence into itself; its `position` matches
  its sequence (`start-work: start`; the four end plays: `end`).
- No consumer play hand-rolls issue/branch/PR/merge steps that duplicate a member; those
  come only via injection.

A mechanical lint check that a consumer's compiled output *contains* the injected sequence
in order lands with the **first consumer play (Phase E)** — the five plays here are all
members, so no consumer exists yet to check. Until then, injection correctness is enforced
by build-play at compile, not re-verified by the linter.

## Related

- `_shared/play-close.md` (beside the plays) — the Standard Play Close the end sequence is appended before; sub-play
  (`parent_run_id`) evidence convention
- `evidence-recording.md` — D1; the injected sub-plays record evidence the play-only way
- `start-work`, `commit-work`, `review-work`, `validate-work`, `merge-work` — the
  member plays this rule composes
- `loop-contract.md` — inside a loop the injected opening and end sequence are skipped
