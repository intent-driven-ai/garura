# Feature: /shape-slice writes the slice and its hidden file

## What it does
/shape-slice <intent> reads the business intent and the product model, asks the person only what the model and memory do not answer, and writes one slice into the spine with its link to the intent. It also writes the slice's hidden file (failure-and-recovery.md, one entry for each feature) in the plan's evals folder, and a thin ICE for each part the slice needs that has no ICE (ontology v11, ADR 052). It writes no plan, no epic, no story and no eval. Built in #795. Not built yet: the hidden file and the thin ICE need the play's /edit-play change (#842).

> To be deepened later: written by /shape-slice for bi-788 at the directional depth. /discover-domains or /discover-capabilities raises it to the detailed depth.

## Inputs / Outputs
- In: the business intent page (`intents/<id>.md`), or its issue when the model has no page for it.
- In: the product model (the spine and the pages of each domain, capability and feature) and memory.
- In: the person's answers to the questions that the model and memory do not answer.
- Out: one slice in the spine, with its features in build order, its one surface, its tester and its link to the intent, and the slice's record.
- Out: the pages the slice needs and the model lacks, marked to be deepened later.
- Out (not built yet, #842): the slice's hidden file (failure-and-recovery.md) in the plan's evals folder: one entry for each feature, with its capability, which of its two ICE is thin, each "Fails if" line and exactly one recovery for each (ontology v11, Slice).

## Rules & behavior
- The play reads the model and memory first, and asks the person only what neither answers, all questions at once.
- Each gap that the play does not ask about is written down as an assumption.
- When a slice already serves the intent, the play uses that slice again and makes no new one.
- The confirmation shows the slice only: what you run, who tests it, the features under each capability, and what is left out (decision 4).
- Nothing is kept before the person types yes. A stop undoes every write.
- For a part the slice needs that has no ICE, the play proposes a thin ICE (at least a goal, a limit and one "Fails if" line, one Context line and one Expectation line), marks it thin and warns the person; it never sends the person back (ontology v11, ICE; ADR 052 §5). Not built yet (#842).

## Acceptance criteria
- Given an intent with no slice, when the product owner runs /shape-slice for it and types yes, then the spine holds one slice that serves the intent.
- Given an intent that a slice already serves, when the play runs again, then it makes no second slice.
- Given a run, when it ends, then no plan, epic, story or eval was written.
- Given a run after decision 6 is built, when it ends, then the hidden file is in the plan's evals folder with one entry for each feature of the slice.
- Thin: the checks for the hidden file wait for its /edit-play change.

## Out of scope
- The plan file, the epic and the stories. /shape-plan writes them (fn-818).
- The eval. /shape-eval writes it (fn-798).
- The loop that runs the three plays and its one approval (#796, decision 1).
- Eval encryption (#828) and the author-slice skill (#838), decision 3.

Thin: proposed by `/shape-slice` from the person's answers; deepen with `/discover-capabilities`.

## Agent intent (ICE)
- Goal: After /shape-slice <intent>, the spine holds one slice that serves the business intent, with its features in build order, its one surface and its tester.
- Goal: After /shape-slice <intent>, the plan's evals folder holds the slice's hidden file, with one entry for each feature of the slice. (Not built yet: decision 6 adds it.)
- Limit: Write no plan, epic, story or eval. The hidden file goes only in .garura/project/plans/<plan-id>/evals/<slug>/, and the confirmation the person sees shows the slice only.
- Fails if: /shape-slice writes a plan, an epic, a story or an eval.
- Fails if: a new slice is made for an intent that a slice already serves.
- Fails if: the hidden file is not written, or a failure condition in it has no recovery or more than one.
- Context: serves the product owner, who runs it in Claude Code; built in #795 (core/components/plays/shape-slice/): it reads the intent from the model and writes the intent page from the issue when the model has none, asks within the tier, reuses a slice that serves, fills the model, writes the slice and its record, and stops at a typed yes / change / stop.
- Checked by: the product owner runs /shape-slice 788 in Claude Code and finds one slice in the spine, the hidden file in plans/788/evals/<slug>/, and no other new file outside the model.
