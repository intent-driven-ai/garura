# The plan for business intent #788: Agents design a named piece of work

This run makes the plan for this business intent, or brings it up to date: the plan file, one epic for each slice and one story for each feature. Nothing below is written yet. Read each write, then type yes to write all of it, change: <what> to have it drafted again, or stop to write nothing.

## What the run writes in the tracker

### Slice sl-intent-to-design: From a named piece of work to its design

- Use epic #794 "The shaping loop turns a business intent into a testable slice, its plan and its eval": write its feature-to-story map: fn-795 → #795, fn-818 → #818, fn-798 → #798, fn-898 → #898.
- Use story #795 "/shape-slice grills within the tier and assembles the slice that delivers the business intent" for fn-795, as it is.
- Use story #818 "The plan play makes the plan file, the epic and one story per feature" for fn-818, as it is.
- Use story #798 "The eval play writes the slice's eval: is the business intent met, tested on the slice's surface" for fn-798, as it is.
- Use story #898 "Agents build for the business intent, not only to pass the eval: the build is given the intent, never the eval" for fn-898: add the sections "Scope of work" and "Context guidance" at the end; every line a person wrote stays.
  - Goals:
    - No build play, build skill, build agent or context sub-agent that a build starts is given the eval, the hidden file or the plan's evals folder.
    - A build is given the business intent through the slice's stories.
    - Each build session that read the plan's evals folder has a flag in that build run's evidence that names the read.
    - Each slice has one eval that says, from the outside, if its business intent is met on the slice's surface.
  - Limits:
    - The check flags a read and never blocks a build.
    - Only /shape-slice, /shape-eval and the eval may name the evals folder.
    - The eval play reads the epic, its stories and the hidden file, never an ICE page, the usage guide or the code, and writes only in the plan's evals folder.
  - Expectations:
    - The lint check runs over the build plays and stops a build play whose inputs name the evals folder.
    - The test of the session-ledger check flags, in the evidence, one session that read the evals folder, and passes a clean session.
    - After /shape-plan, /shape-eval writes the eval in the plan's evals folder, and the inputs of no build play name that folder.
  - Read: The build plays' inputs, and a build session's ledger, found through the session stamp in the run's evidence.
  - Never read: The eval, the hidden file and the rest of the plan's evals folder.
  - Persona: The product owner, who trusts an eval pass only when the build aimed at the intent.
  - In and out: In: the flag in the build run's evidence and the lint check over the build plays. Out: blocking by a hook (#893), encryption (#828, dropped) and the drift checks and evidence warnings in Griffin.

## The plan file

- Update `.garura/project/plans/788.yaml`. Every other node and line stays as it is.
- No node changes. The file stays as it is.

## Skipped features

- None. Every feature's ICE is ready.

## Your answer

The run makes 2 tracker write(s) of the kinds above, and then the plan-file change.
Type **yes** to write all of it, **change: <what>** to have the epic or stories drafted again, or **stop** to write nothing.
