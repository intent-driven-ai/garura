# ADR 049 — A Slice Is Shaped, Then Planned, Then Given Its Eval: One Plan for Each Business Intent, the Eval Kept in the Plan's Folder, and No Failure Condition Reaches the Builder

**Status:** Accepted
**Date:** 2026-10-23
**Level:** framework
**Decided by:** the product owner · **Decided in:** #824 (records product ontology v9, #816 and PR #823, and v10, #826 and PR #827, both decided with the product owner at the three `/edit-ontology` checkpoints, plan #788)
**Supersedes:** ADR 048 (in part — Decision §2, its first paragraph: "A Plan is given one business intent. It picks the slice or slices that best serve it, by two tests … It creates one Epic for each slice it picks"; and, in its list "What this changes in older ADRs", the ADR 022 line "the Plan's first test refuses a slice with none". The slice definition in §2 stands, and §1, §3, §4 and §5 stand)
**Amends:** ADR 017 — §1 "Strict `.garura/` folder whitelist": under `.garura/project/` the whitelist gains `plans/`, which holds one file `<id>.yaml` for each plan and its folder `<id>/`, with `evals/<slug>/` (the slice's eval and its hidden file `failure-and-recovery.md`) and `guides/<slug>.md`. The rest of §1 stands
**Affects:** `core/components/memory/standards/schemas/product-os/ontology.md` (v9 and v10, landed), `core/components/memory/standards/rules/expectation-generation.md` (the section "A story's recovery (product ICE)", landed), `CLAUDE.md` (Work Tracking, landed), `.garura/user-provided/managing-work.md` (still says "a plan picks a slice"), `core/components/memory/standards/schemas/product-os/spine.yaml` and `slice.yaml` (the slice entry gains `intents`), `core/components/plays/shape-slice/`, `core/components/plays/build-epic/` (its context sub-agent), the plan play and the eval play (not built yet), and the folder `.garura/project/plans/`
**ICE impact:** The product ICE does not change: each capability and each feature keeps one ICE in three parts (ADR 047). What changes is where each part of it goes, so that the routing table in `docs/philosophy/idd-principles.md` holds word for word. The plan play reads both ICE of a story once. The story gets the goal, the limits, the expectations and the Context guidance. The slice's hidden file gets the failure conditions, with one recovery condition each. The build play's context sub-agent and the builder never open an ICE page or a plan's evals folder. The eval play reads the epic, its stories and the hidden file; the running eval reads the eval, the usage guide, the Context guidance in the eval and only the recovery parts of the hidden file. The ICE of `/shape-slice` and `/build-epic` change in meaning when they are rebuilt; the plan play and the eval play get their ICE when they are built.
**Business intent check:** kind — the Business Intent kind changes: a slice serves it (the link is kept on the slice's side only), it is a destination that does not point at its slices, and it has exactly one plan. No person's business intent changes: the v9 and v10 commits touch no page in `.garura/product/product-os/intents/`
**Related:** ADR 017, ADR 022, ADR 027, ADR 031, ADR 047, ADR 048, #788, #816, PR #823, #822, #826, PR #827, #828

## Context

The delivery chain (#788) shapes the work, builds a hidden eval, builds the work without the eval, then checks it. ADR 048 put the Slice in the model and the Epic in the tracker, with the Plan between them. It said a plan is given a business intent and picks slices by two tests.

Ontology v9 (#816) changed how the work is made, and no ADR records it. At the checkpoints the product owner said three things. First, `/shape-slice` must only shape the slice and pass on to the plan, so that no work is done twice ("I don't want to duplicate the functionality"). Second, the shaping work is three plays in a row: shape the slice, build the plan, build the eval. Third, only one place interprets the ICE ("I don't want two or three different things to talk to ICE and have different interpretations").

v9 then broke a principle. In v9 a story's scope of work said "what must never happen", and the builder reads the story. So failure conditions reached the builder, and recovery conditions had no place. The routing table in `docs/philosophy/idd-principles.md` says the builder never gets them. The product owner said: "idd principles need to hold true … we cant break the principle". Ontology v10 (#826) fixed it.

`/record-decision` cannot join an open change (#822), so this ADR is its own record. The product owner asked for it to be drafted in place, with no change cycle.

Note from the ADR keeper: ADR 048 §3 says a story writes its scope of work from two ICE, and no work item carries an ICE. That still holds, so §3 is not amended; this ADR adds to it (Decision §4). ADR 047 is not changed: the ICE keeps its three parts.

## Decision

### 1. The shaping loop: three plays, one after the other

1. `/shape-slice` shapes one slice and writes one link: "slice serves business intent" (the slice's `intents` list; the first is the intent it was first shaped for). It writes nothing else: no plan, no epic, no story, no eval. A thing with no screen or surface that a person can test end to end is not a slice, and `/shape-slice` does not shape it. That rule is now the Slice's own.
2. The plan play runs right after it, with no stop between them. It makes the plan, the epic for the slice (or uses the one that exists), one story for each feature of the slice, and the slice's hidden file.
3. The eval play builds the slice's eval.

The plan does not pick, rank or test slices. The person chose the slice at `/shape-slice`. This replaces the two tests of ADR 048 §2.

### 2. One plan for each business intent

A business intent has one plan, and never a second. The plan's ID is the intent's issue number. The plan holds every slice that serves its intent, found by reading the link "slice serves business intent". When a new slice is shaped for an intent that has a plan, the plan play adds the slice and its epic to that plan. A slice that serves two intents has one epic, used by both plans.

### 3. Where the eval, the hidden file and the usage guide live

- The slice's eval and its hidden file: `.garura/project/plans/<plan-id>/evals/<slug>/` (the eval, and `failure-and-recovery.md`).
- The slice's usage guide: `.garura/project/plans/<plan-id>/guides/<slug>.md`, beside the evals folder, not in it.
- `<plan-id>` is the slice's home plan: the plan for the intent it was first shaped for. It is worked out, never stored. Another plan that holds the slice points to these files and never copies them.
- The build writes the usage guide. It is the eval's only way into the built product.

This adds `plans/` under `.garura/project/`, which the folder list of ADR 017 §1 does not name.

### 4. How the ICE reaches the eval and the builder

- **The plan play reads all of each ICE, once.** For each story it reads the feature's ICE and that feature's capability's ICE.
- **The story** holds the goal, the limits and the expectations in its scope of work, and the Context guidance (the four Context lines: what to read, what never to read, the persona, the scope) as its own property. It never holds a failure condition or a recovery condition, and it never holds the context itself.
- **The build play's context sub-agent** reads the story's Context guidance, collects the context at run time and puts it in the issue's short-term memory, `.garura/project/issues/<issue>/`. It never opens an ICE page or a plan's evals folder. The builder reads the story and that collected context.
- **The hidden file**, written by the plan play from the same two ICE: for each story, its failure conditions, and exactly one recovery condition for each (when, way back, who fixes).
- **The eval is read at two times.** The eval play, before the build, reads the epic, its stories and the hidden file, never the guide or the code. The running eval, after the build, reads the eval, the usage guide, the Context guidance in the eval and only the recovery parts of the hidden file, never the failure conditions.
- **A failure gives a handoff plan.** It says what the product does wrong, as a symptom, and the way back. It never names the failure condition, its id or the check. It goes to the builder or to a person, as the recovery condition says.
- When an ICE changes after its story is made, the story and its hidden-file entry are drift. They are made again together, from the same two ICE.

Today the eval is kept from the builder by a read rule only: no builder, no skill that builds the software and no context sub-agent reads a plan's evals folder. Encrypting the evals is #828.

### 5. The recovery rule covers a story

`core/components/memory/standards/rules/expectation-generation.md` now gives a story its recovery, by the same rule as a play's: one recovery condition for each "Fails if" line, marked "the builder can fix this alone" or "a person must decide".

### What this changes in older ADRs

- **ADR 048 §2, first paragraph** — superseded. The plan does not pick slices by two tests; it holds every slice that serves its intent. The surface rule moves to the Slice and to `/shape-slice`, so ADR 048's line that "the Plan's first test refuses a slice with none" goes too. The definition of a slice in §2 stands.
- **ADR 017 §1** — amended. The whitelist under `.garura/project/` gains `plans/`.

### What this does not change

- ADR 047: the ICE, its three parts and its ready check.
- ADR 048 §1, §3, §4 and §5: the two layers, the Epic and the Story, the rename, and the fields that leave the model.
- The routing table in `docs/philosophy/idd-principles.md`: it is not changed; this decision makes it hold.
- No person's business intent.

## Consequences

### Positive

- Each play has one job. Shaping, planning and eval building do not repeat each other's work.
- Each ICE is interpreted once, by the plan play. The story, the hidden file and the eval cannot read the ICE in different ways.
- The builder never sees a failure condition or the eval, so it cannot build to the test. The routing table holds.
- One plan for each intent: a person sees all the work for one intent in one place.
- A shared slice has one eval, one hidden file and one guide, so they cannot drift apart.

### Negative / Risks

- Until #828, only a read rule keeps the eval from the builder. A play that breaks the rule is not stopped by anything on disk.
- The plan play and the eval play are not built yet, and `/shape-slice` still cuts a slice into epics. Until they change, the plays and the ontology say different things.
- The story's Context guidance is a copy of the ICE's Context. When the ICE changes, the copy is out of date until the Alignment loop finds it.
- Where the handoff plan is kept, and how it reaches the builder, is not decided.
- The spine's slice entry has no `intents` field yet, so the link "slice serves business intent" has no place on disk today.

## Alternatives Considered

- **The plan picks slices by two tests (ADR 048 §2)** — lost: the person already chose the slice at `/shape-slice`; testing it again in the plan does the work twice.
- **`/shape-slice` also makes the plan, the epic and the stories** — lost: the product owner wanted `/shape-slice` to stop at the slice and pass on to the plan, with no duplicated work.
- **The eval reads the ICE of the features and capabilities itself** — lost: two readers of one ICE give two interpretations. The eval reads what the plan play wrote.
- **The story's scope of work says what must never happen (v9)** — lost: the builder reads the story, so failure conditions would reach it, against the routing table.
- **The story carries the context itself** — lost: the story holds guidance only; the context sub-agent collects the context when the build runs, so it is current.
- **A plan copies the eval of a slice it shares with another plan** — lost: two copies drift; the other plan points to the home plan's files.

## Work This Creates

- `/shape-slice` shapes the slice and writes only the link "slice serves business intent".
- Build the plan play and the eval play.
- `/build-epic`: its context sub-agent collects the context from the story's Context guidance into short-term memory and never reads a plan's evals folder.
- `spine.yaml` and `slice.yaml`: the slice entry gains `intents`.
- `.garura/user-provided/managing-work.md`: drop "a plan picks a slice".
- #828 — encrypt the evals.
- Decide where the handoff plan is kept and how it reaches the builder.
- After acceptance: the forward pointers on ADR 048 and ADR 017, and close #816.

## References

- `.garura/project/issues/824/context/issue.md` — the brief
- `.garura/project/issues/816/context/edit-ontology/decisions.json` — the product owner's answers for v9
- `.garura/project/issues/826/context/edit-ontology/need.md` and `decisions.json` — the need and the answers for v10
- `core/components/memory/standards/schemas/product-os/ontology.md` — v9 and v10 log lines; the Slice, Plan, Story and ICE kinds
- `docs/philosophy/idd-principles.md` — "The Routing Table"
- `core/components/memory/standards/rules/expectation-generation.md` — "A story's recovery (product ICE)"
