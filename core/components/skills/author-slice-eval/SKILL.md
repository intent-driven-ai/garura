---
name: author-slice-eval
description: Write the one eval of a business intent's plan, for /design-eval — one feature file for each Feature issue of the plan's epic (eval.<feature-id>.feature.md, Markdown with Gherkin, its Feature is the Feature issue), held_by ones included, with a scenario for each goal and each expectation of the Feature issue and, for each failure condition of its feature in the slice's hidden file, a scenario that shows it does not happen; and one plan file (eval.<plan-id>.md) with one section for each slice the plan holds (its surface kind from its own hidden file, the time limit for each scenario, its features in build order), the pass rule, the names the usage guide will map, and the Feature issues' Context guidance. Every step is a sentence of the surface kind's step library, so a runner does it with no agent; every Then is an exact result; what only the build will make is a [name]; what it cannot test yet goes under Untestable with the reason. Reads only the copies its agent gives it (inputs.json, the epic, Feature issue and hidden-file copies, the step libraries, the two templates, and the eval files the plan already has); never an ICE page, the usage guide, the code or the product model. Never runs an eval, never writes a recovery or handoff text, never changes a scenario that is there. Writes drafts only; the play's scripts place, check and show them, and commit after the product owner's yes. Generative artifact production for /design-eval. Use when /design-eval needs a plan's eval drafted, fixed or drafted again.
user-invocable: false
model: opus
allowed-tools: Read, Write
---

# author-slice-eval

A plan has one eval. It says, from the outside, if the plan delivers what its Feature issues
promise, for every feature of every slice the plan holds. This skill writes it, before the build,
from what /shape-plan and /design-slice wrote: the Feature issues (their goals and expectations)
and the hidden file of each slice (the failure conditions). The eval is written so that it runs
with no agent and no judgment: every step is a fixed sentence that a runner does exactly, and every
result is exact. This skill only writes; it never runs anything. The play's scripts gather the
copies before it and place, check and show the drafts after it.

## Input

| Field | Required | Meaning |
|-------|----------|---------|
| `inputs` | yes | `inputs.json` from the play's `gather_eval.py`: `plan_id`, `intent_title`, `epic`, `ready`; `slices` (the slices that are not Dropped, in the plan's Slices list order: `slice_id`, `surface`, `surface_kind`, `features` in build order); `features` (in the map's order: `feature`, `issue`, `title`, `held_by`, `goals`, `expectations`, `context`, `path` of the Feature issue copy, `slices` that hold it, `slice` the first of them, `surface_kind`, `failures` with their ids); `existing` and `out_of_plan` (the eval files the plan already has, and the feature files whose feature left the plan); `dropped` and `left_out` (the dropped slices and the features only they hold: write nothing for them). Write only when `ready` is true |
| `copies` | yes | The folder of copies: `epic-<n>.md`, `feature-<n>.md`, `hidden-<slug>.md` (one for each slice), and `existing/` (the eval files the plan already has). These are the only epic, Feature issue and hidden-file text you read |
| `library` | yes | The step library of each surface kind the plan's slices use (`steps-<kind>.yaml`): every sentence a step may be |
| `templates` | yes | The two templates, `eval-feature.feature.md` and `eval-plan.md` (the shape), and the rules page `eval-format.md` (the rules of both) |
| `problems` | no | On a fix: the `problems` of `eval-check.json`, by file |
| `change` | no | On a re-run: the product owner's words after `change:` at the checkpoint |
| `out` | yes | The drafts folder: write the files straight into `<out>/` |

## Process

1. **Read only the copies.** Never open any other file: not an ICE page, not the usage guide
   (the build has not made it), not the code, not the product model.
2. **Write one feature file for each feature in `features`,** `eval.<feature>.feature.md`, in the
   shape of `eval-feature.feature.md`, also for a feature with `held_by` (its Feature issue sits
   under another plan's epic; the plan still tests it):
   - the tag line `` `@feature-<n>` `` and `# Feature: Feature issue #<n> — <title>`; the Feature
     is the Feature issue, never a slice and never a story;
   - a `## Background:` with the setup every scenario needs, as library sentences;
   - for each line of the Feature issue's "Goals:" list, one or more scenarios tagged
     `` `@goal-<k>` `` (the k-th line, from 1); the same for each "Expectations:" line with
     `` `@expectation-<k>` ``; one scenario may cover more than one line, and carries each tag;
   - for each failure condition in the feature's `failures` (from the hidden file of its first
     slice), a scenario tagged `` `@F<n>` `` that shows the condition does **not** happen;
   - `## Untestable`: one line for each goal, expectation or failure condition you cannot write
     a scenario for yet, with its tag and the reason (for example, the Feature issue says the part
     is not built yet, or the check would need a wait the time limit does not allow).
   - `## Lines covered`: one line for each goal and expectation a scenario covers, with its tag and
     the Feature issue line's exact text as `inputs.json` gives it
     (`` - `@goal-2`: A patient gets a reminder. ``). A later run compares these lines with the
     Feature issue to find a line that moved or changed.
3. **Write each step as a sentence of the library** of the feature's `surface_kind`, with
   `* Given`, `* When`, `* Then`, `* And` or `* But`. Do not change a sentence's words. A value is a
   literal in double quotes when the Feature issue names it ("/design-slice 1", "plans/1.yaml");
   what only the build will make — a command, a page, a field the Feature issue does not name — is a
   name in square brackets (`[the booking page]`), never a guess. Each Then is an exact result a
   tester can see: an exit code, a text in the output, a file, a field, a count.
4. **Test from the outside, on the surface.** A step never reads the code and never calls the
   product's parts directly. When the surface is a play, a scenario runs the play in a test project
   and gives it its answers (`When I run "/design-slice 1" and answer "yes"`), then checks the files
   and the output.
5. **Write the plan file,** `eval.<plan-id>.md`, in the shape of `eval-plan.md`: its title with the
   plan id and the epic; the pass rule; one `## Slice <slice id>` section for each slice in
   `slices`, in that order, each with the slice's Surface line, `Surface kind:` (from that slice's
   own hidden file), `Time limit for each scenario: <n> seconds` (long enough for the slowest
   scenario of the slice; a play run takes minutes) and the slice's `features` in build order, as
   `<k>. Feature issue #<n> (<feature id>) — eval.<feature id>.feature.md`, with
   ` (held by epic #<m>)` at the end for a feature with `held_by`; a feature in two slices is listed
   in each; "Out of the plan" for each file in `out_of_plan`; "Names" with each name the feature
   files use and what it is, in plain words; and "Context" from the Feature issues' Context
   guidance lines.
6. **Never write a recovery or a handoff text.** Not "the builder can fix this alone", not "a person
   must decide", not "Way back:", not "Who fixes:", and no recovery line of a hidden file. The
   recovery stays in the hidden file.
7. **A plan that already has eval files** (`existing`): never change or drop a scenario that is
   there, and never change a line of its "Lines covered" list, also when the Feature issue's line
   moved or changed (the play names that for a person). Write the feature file with the scenarios it
   has, word for word, and add only scenarios, and their Lines covered lines, for what it does not
   cover yet; the play's `place_eval.py` keeps the file's lines in any case.
8. **On a fix,** rewrite only what each problem names, and keep every other draft as it is. **On a
   change,** draft again what the product owner's change names, and keep the rest.

## Output

The drafts folder:

```
<out>/eval.<feature-id>.feature.md   (one for each Feature issue of the map)
<out>/eval.<plan-id>.md
```

A scenario, in three fields:
- A clinic: `` `@goal-1` `` "a patient books a free slot" — `* When I run [the book command] and
  answer "10:00"` · `* Then the exit code is 0` · `* And the file "bookings.json" field "10:00"
  equals "booked"`.
- A shop: `` `@F2` `` "a guest is not charged twice" — `* When I run [the pay command] and answer
  "card"` · `* And I run [the pay command] and answer "card"` · `* Then the file "orders.json" field
  "charges" has 1 items`.
- A school: `` `@expectation-2` `` "a parent sees only their own child's marks" — `* When I run [the
  marks command] and answer "parent-1"` · `* Then the output does not contain "child-2"`.

## Rules

- Draft only. Never write the evals folder, the tracker, the model or any other file; the play
  places, checks and commits.
- Read only the copies the agent gives: never an ICE page, the usage guide, the code or the
  product model.
- Every step is a library sentence; every Then is exact; there is no score.
- Each scenario covers only what its Feature issue or its feature's hidden-file entry says, and the
  eval covers only the plan's features.
- Plain words (ASD-STE100), personas only, no real names.
