---
name: author-slice-eval
description: Write the eval of each ready slice of a business intent's plan, for /shape-eval — one story file for each story of the slice's epic (eval.<feature-id>.feature.md, Markdown with Gherkin, its Feature is the story) with a scenario for each goal and each expectation of the story and, for each failure condition of the story's feature in the slice's hidden file, a scenario that shows it does not happen; and one slice file (eval.<slice-id>.md) that lists the stories in build order with the surface kind, the time limit for each scenario, the pass rule, the names the usage guide will map, and the stories' Context guidance. Every step is a sentence of the surface kind's step library, so a runner does it with no agent; every Then is an exact result; what only the build will make is a [name]; what it cannot test yet goes under Untestable with the reason. Reads only the copies its agent gives it (inputs.json, the story, epic and hidden-file copies, the step library, the two templates, and the eval files the slice already has); never an ICE page, the usage guide, the code or the product model. Never runs an eval, never writes a recovery or handoff text, never changes a scenario that is there. Writes drafts only; the play's scripts place, check and show them, and commit after the product owner's yes. Generative artifact production for /shape-eval. Use when /shape-eval needs a slice's eval drafted, fixed or drafted again.
user-invocable: false
model: opus
allowed-tools: Read, Write
---

# author-slice-eval

A slice's eval says, from the outside, if the slice's epic delivers what its stories promise.
This skill writes it, before the build, from what /shape-plan and /shape-slice wrote: the
stories (their goals and expectations) and the slice's hidden file (the failure conditions).
The eval is written so that it runs with no agent and no judgment: every step is a fixed
sentence that a runner does exactly, and every result is exact. This skill only writes; it never
runs anything. The play's scripts gather the copies before it and place, check and show the
drafts after it.

## Input

| Field | Required | Meaning |
|-------|----------|---------|
| `inputs` | yes | `inputs.json` from the play's `gather_eval.py`. For each slice: `slice_id`, `slug`, `epic`, `ready`, `surface`, `surface_kind`, `stories` (in build order: `feature`, `issue`, `title`, `goals`, `expectations`, `context`, `path` of the story copy), `failures` (each feature's failure conditions with their ids), `existing` and `out_of_slice` (the eval files the slice already has, and the story files whose feature left the slice). Write only for slices with `ready: true` |
| `copies` | yes | The folder of copies: `epic-<n>.md`, `story-<n>.md`, `hidden-<slug>.md`, and `existing/<slug>/` (the eval files the slice already has). These are the only story, epic and hidden-file text you read |
| `library` | yes | The step library of each surface kind the ready slices use (`steps-<kind>.yaml`): every sentence a step may be |
| `templates` | yes | The two templates: `eval-story.feature.md` and `eval-slice.md` |
| `problems` | no | On a fix: the `problems` of `eval-check.json`, by file |
| `change` | no | On a re-run: the product owner's words after `change:` at the checkpoint |
| `out` | yes | The drafts folder: write `<out>/<slug>/` for each ready slice |

## Process

1. **Read only the copies.** Never open any other file: not an ICE page, not the usage guide
   (the build has not made it), not the code, not the product model.
2. **For each ready slice, write one story file for each story,** `eval.<feature>.feature.md`,
   in the shape of `eval-story.feature.md`:
   - the tag line `` `@story-<n>` `` and `# Feature: Story #<n> — <story title>`; the Feature
     is the story, never the slice;
   - a `## Background:` with the setup every scenario needs, as library sentences;
   - for each line of the story's "Goals:" list, one or more scenarios tagged `` `@goal-<k>` ``
     (the k-th line, from 1); the same for each "Expectations:" line with `` `@expectation-<k>` ``;
     one scenario may cover more than one line, and carries each tag;
   - for each failure condition of the story's feature in the hidden file, a scenario tagged
     `` `@F<n>` `` that shows the condition does **not** happen;
   - `## Untestable`: one line for each goal, expectation or failure condition you cannot write
     a scenario for yet, with its tag and the reason (for example, the story says the part is
     not built yet, or the check would need a wait the time limit does not allow).
3. **Write each step as a sentence of the library** of the slice's surface kind, with `* Given`,
   `* When`, `* Then`, `* And` or `* But`. Do not change a sentence's words. A value is a literal
   in double quotes when the story names it ("/shape-slice 1", "plans/1.yaml"); what only the
   build will make — a command, a page, a field the story does not name — is a name in square
   brackets (`[the booking page]`), never a guess. Each Then is an exact result a tester can see:
   an exit code, a text in the output, a file, a field, a count.
4. **Test from the outside, on the surface.** A step never reads the code and never calls the
   product's parts directly. When the surface is a play, a scenario runs the play in a test project
   and gives it its answers (`When I run "/shape-slice 1" and answer "yes"`), then checks the files
   and the output.
5. **Write the slice file,** `eval.<slice-id>.md`, in the shape of `eval-slice.md`: its title
   with the slice id and the epic; the Surface line from the hidden file; `Surface kind:`; `Time
   limit for each scenario: <n> seconds` (long enough for the slowest scenario; a play run takes
   minutes); the pass rule; the stories in the order of `inputs.json` (the epic's map); "Out of
   the slice" for each file in `out_of_slice`; "Names" with each name the story files use and what
   it is, in plain words; and "Context" from the stories' Context guidance lines.
6. **Never write a recovery or a handoff text.** Not "the builder can fix this alone", not "a person
   must decide", not "Way back:", not "Who fixes:", and no recovery line of the hidden file. The
   recovery stays in the hidden file.
7. **A slice that already has eval files** (`existing`): never change or drop a scenario that is
   there. Write the story file with the scenarios it has, word for word, and add only scenarios for
   what it does not cover yet; the play's `place_eval.py` keeps the file's lines in any case.
8. **On a fix,** rewrite only what each problem names, and keep every other draft as it is. **On a
   change,** draft again what the product owner's change names, and keep the rest.

## Output

The drafts folder, one folder for each ready slice:

```
<out>/<slug>/eval.<feature-id>.feature.md   (one for each story)
<out>/<slug>/eval.<slice-id>.md
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
- Every step is a library sentence; every Then is exact; there is no score.
- Each scenario covers only what its story or its feature's hidden-file entry says.
- Plain words (ASD-STE100), personas only, no real names.
