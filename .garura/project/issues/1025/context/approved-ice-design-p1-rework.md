# Approved ICE design — P1 rework of /shape-plan and /design-eval

Approved by the product owner on 2026-11-12 ("yes"). Rules it follows: ADR 068, ADR 069, product ontology v17 (all on main).

## /shape-plan

**Intent.** /shape-plan makes the intent's one plan:
- the plan file, with the business intent at the top, the `epic:` mark, and a Slices list with each slice at Not Started;
- ONE epic for the plan;
- one Feature issue for each feature not yet built, across all the plan's slices.

Each Feature issue holds its scope of work and Context guidance, written from its feature's ICE and its capability's ICE. The play files no Stories: those are pieces of work that come later, from the build.

**C3: how a work item is found.**
- The plan's epic is found by the plan file's `epic:` mark.
- A feature's issue is found by its `represents` mark in the plan file. When there is none, it is found by an issue of type Feature that carries the exact line `Represents: <feature id>`.
- A play never finds an issue by its title.
- When two Feature issues name one feature, the run stops and asks the person.
- A Feature issue that sits under another plan's epic is shown as `held_by`. The play never moves it without the person's answer.

**New: clean as you go.** For a feature with no Feature issue, the play searches the tracker for old work on that feature, and proposes one action in the brief:
- An old open story is found: file the Feature issue and move the story inside it.
- The old work is finished: file the Feature issue already closed, so the feature counts as built and is left out of the plan.
- Nothing is found: file a new Feature issue.

Nothing happens without the person's yes. The play looks only at the plan's own features.

**New: built features.** A feature whose Feature issue is closed as completed is built. It is not put in the plan, and the brief names it as left out.

**C13: the tracker shape.** The plan's epic is an issue of type Epic. Each Feature issue is of type Feature, sits under the epic, and has no label. The epic stands for the plan, not for a slice.

**Scenarios (new).**
- S12: one plan with two slices → one epic, and one Feature issue for each pending feature of both slices.
- S13: an old open story is found → a Feature issue is filed and the story is moved inside it, after the yes.
- S14: old finished work is found → a closed Feature issue is filed, and the feature is left out of the plan.
- S15: two Feature issues name one feature → the run stops and names both.

S10 and S11, which were written for ADR 067's model-held issue number, go.

## /design-eval

**Intent.** /design-eval writes the plan's ONE eval. It reads only:
- the plan's epic, with its map;
- its Feature issues, meaning their scope of work and Context guidance;
- the hidden file of each slice the plan holds.

The eval covers every feature of every slice, including `held_by` ones.

**C2: where it writes.** It writes in the plan's evals folder:
- one file for each Feature issue, `eval.<feature-id>.feature.md`;
- one plan file, `eval.<plan-id>.md`. It lists the features slice by slice, in build order, with each slice's surface kind, the time limits, the pass rule and the names. It has one section for each slice.

**C3: the Gherkin.** Each file has one Gherkin `Feature:`, which is the Feature issue.

**C8, C12 and C14.**
- A plan whose epic, Feature issues or any slice's hidden file is missing gets no eval, and the run names it.
- Each slice's surface kind comes from its own hidden file.
- The eval covers only the plan's features.
