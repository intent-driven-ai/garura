# The plan for business intent #788: Agents design a named piece of work

This run makes the plan for this business intent, or brings it up to date: the plan file, one epic for each slice and one story for each feature. Nothing below is written yet. Read each write, then type yes to write all of it, change: <what> to have it drafted again, or stop to write nothing.

## What the run writes in the tracker

### Slice sl-intent-to-design: From a named piece of work to its design

- Use epic #794 "The shaping loop turns a business intent into a testable slice, its plan and its eval": set its type to Feature (it is not set now); add the line "Represents: sl-intent-to-design" at the end of its text; write its feature-to-story map: fn-795 → #795, fn-818 → #818, fn-798 → #798.
- Use story #795 "/shape-slice grills within the tier and assembles the slice that delivers the business intent" for fn-795: add the sections "Scope of work" and "Context guidance" at the end; every line a person wrote stays; set its type to Story (it is not set now).
  - Goals:
    - When the product owner runs /shape-slice on a business intent, the spine gets one slice that serves that intent, with its features in build order, its one surface and the persona who tests it.
    - One person can test the slice end to end on that one surface.
    - The same run puts the slice's hidden file in the plan's evals folder, with one entry for each feature of the slice and each entry closed by exactly one way back. This part is not built yet; decision 6 adds it.
  - Limits:
    - Write only the slice, its link to the business intent it serves, its record, the model parts the slice lacks (each marked to be deepened) and the hidden file.
    - Write no plan, epic, story or eval.
    - Put the hidden file only in .garura/project/plans/<plan-id>/evals/<slug>/.
    - The confirmation the product owner sees shows the slice only.
    - Ask the product owner only what the product model and memory do not answer, and stay inside the question tier.
  - Expectations:
    - The product owner runs /shape-slice 788 in Claude Code and finds one slice in the spine and the hidden file in plans/788/evals/<slug>/.
    - No other new file appears outside the product model.
    - Run on a real business intent, the play writes one slice and its hidden file, and no plan, epic, story or eval.
  - Read: the business intent's page, the spine, the Slice kind in the ontology, memory, and the play's own folder in core/components/plays/shape-slice/ (built in #795)
  - Never read: the plan, its epics and stories, and the eval: they come after this play
  - Persona: the product owner, who names the intent, answers the questions and approves in Claude Code; /shape-plan and /shape-eval read the slice after
  - In and out: in: the intent page when the model has none, the questions, reuse of a slice that already serves, the missing model parts, the slice, its record and its hidden file, and the stop at a typed yes, change or stop; out: the plan, the epic, the stories and the eval
- Use story #818 "The plan play makes the plan file, the epic and one story per feature" for fn-818: add the sections "Scope of work" and "Context guidance" at the end; every line a person wrote stays; set its type to Story (it is not set now).
  - Goals:
    - When the product owner runs /shape-plan on a business intent, the intent's one plan file (.garura/project/plans/<intent>.yaml) exists, with one epic for each slice that serves the intent and one story for each feature of that slice.
    - The plan names every capability and feature it holds, each with its ICE.
    - A second run finds the plan, the epics and the stories that exist, and makes no copies of them.
  - Limits:
    - Write only the plan file, the epics and the stories.
    - Each story holds the goals, the limits, the expectations and the Context guidance from its feature's ICE and that feature's capability's ICE, and nothing from the hidden file.
    - The hidden file and all that it holds belong to /shape-slice (decision 6); the eval belongs to /shape-eval.
    - Nothing goes to the tracker before the product owner types yes.
    - Do not pick, rank or test slices; the product owner chose the slice at /shape-slice.
    - Do not wait for a full product model; write a missing model page as a light page during the run.
  - Expectations:
    - The product owner runs /shape-plan 788 in Claude Code after /shape-slice and finds the plan file, one epic, and one story for each feature of the slice.
    - No story holds any line from the hidden file.
    - Building the plans for #717 and its partner gives the same trees that were filed by hand on 2026-10-21.
  - Read: the slice in the spine, and the ICE of each feature and of its capability, once for each story
  - Never read: the slice's hidden file and the evals folder
  - Persona: the product owner, who runs and tracks the plan; the build play reads the stories after
  - In and out: in: the plan file in .garura/project/plans/ and the tracker's epics and stories; out: picking the slice, the hidden file, the eval and the build (not built yet, #818)
- Use story #798 "The eval play writes the slice's eval: is the business intent met, tested on the slice's surface" for fn-798: add the sections "Scope of work" and "Context guidance" at the end; every line a person wrote stays; set its type to Story (it is not set now).
  - Goals:
    - When the product owner runs /shape-eval on a business intent, the slice's evals folder holds one eval for that slice.
    - The eval checks from the outside, on the slice's surface, each goal and expectation of the stories, and checks that nothing the hidden file warns about happens.
    - The eval says if the business intent is met on the slice's surface.
  - Limits:
    - Read only the epic, its stories and the slice's hidden file.
    - Never read an ICE page, the usage guide or the code.
    - Write the eval only in the plan's evals folder (.garura/project/plans/<plan-id>/evals/<slug>/), and nowhere else.
  - Expectations:
    - The product owner runs /shape-eval 788 in Claude Code after /shape-plan and finds the eval in plans/788/evals/<slug>/.
    - No build play's inputs name the evals folder.
  - Read: the epic and the stories that /shape-plan wrote, and the hidden file that /shape-slice wrote
  - Never read: any ICE page, the usage guide (guides/<slug>.md) and the code
  - Persona: the product owner, who wants proof that the intent is met; the running eval after the build uses what this play writes
  - In and out: in: writing the eval, which for Garura often runs a play on a test project and reaches the slice only through its usage guide; out: running the eval and encrypting it (until #828 only a read rule keeps builders away from the folder; not built yet, #798)

## The plan file

- Update `.garura/project/plans/788.yaml`. Every other node and line stays as it is.
- No node changes. The file stays as it is.

## Skipped features

- None. Every feature's ICE is ready.

## Your answer

The run makes 4 tracker write(s) of the kinds above, and then the plan-file change.
Type **yes** to write all of it, **change: <what>** to have the epic or stories drafted again, or **stop** to write nothing.
