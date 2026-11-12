---
name: author-work-items
description: Write, for a business intent's plan, the title of its ONE epic (what a person can see the product do, not how it is built) and, for each ready feature of the plan's slices (once, also when two slices hold it), the text of its Feature issue — its title, its scope of work (goals, limits, expectations) and its Context guidance (what to read, what never to read, the persona, what is in and what is out) — in its own words, from skill-input.json and the clean copies of the feature's ICE and its capability's ICE that the play's gather_plan.py wrote — the only files it reads; neither names an ICE page. It never opens an ICE page, never writes a failure or recovery condition, never drafts a Story, and writes plain words with personas. Fix mode rewrites only the parts the play's check_drafts.py names; change mode drafts again with the product owner's change. Writes drafts.json only; the play's scripts check it, show it in the brief and write the tracker after the product owner's yes. Generative artifact production for /shape-plan, and, in story mode, for /reshape-plan (the text for one feature named in a session, #1002). Use when /shape-plan needs the epic and the Feature issues of a plan drafted, fixed or drafted again, or /reshape-plan needs one feature's text drafted from its ICE.
user-invocable: false
model: opus
allowed-tools: Read, Write
---

# author-work-items

A plan has ONE epic, and one Feature issue for each feature of its slices that is not built
yet. The epic tells the eval play what a person can see the product do. Each Feature issue
tells the build play what its feature must do, inside which limits, what "done" means, and
where to look for context; the Stories inside it come later, from the build, and this skill
drafts none. This skill writes that text. The play's scripts find the epic and the Feature
issues that exist before it, and check, show and write the drafts after it, so this skill does
only the judgment: the words.

## Input

| Field | Required | Meaning |
|-------|----------|---------|
| `skill_input` | yes | `skill-input.json` from the play's `gather_plan.py`: the intent and its title, each slice with its id, name, outcome and feature ids, and each ready feature once (`id`, `name`, `one_line`, `clean_ice`, `slices`). It names no ICE page and no feature that is not ready |
| `clean_ice` | yes | The clean copies that `skill-input.json` names, one for each ready feature (`<working>/ice/<feature id>.md`): the feature's ICE and its capability's ICE, with the failure lines taken out. These are the only ICE text you read |
| `problems` | no | Fix mode: the `problems` of `drafts-check.json` (`feature`, `problem`; a null feature means the epic) |
| `change` | no | Change mode: the product owner's words after `change:` at the checkpoint |
| `drafts` | no | The drafts.json of the earlier round, in fix mode and change mode |
| `out` | yes | Where to write `drafts.json` |

## Process

1. **Read only `skill-input.json` and the clean copies.** For each feature it lists, read its
   `clean_ice`. Never open any other file, and never an ICE page: those pages hold the failure
   lines, which are not yours to read. A feature that is not ready is not in
   `skill-input.json` and gets no draft; the play names it in the brief.
2. **Write the plan's one epic.**
   - `title` — one line that says what a person can see the product do, from the names and
     outcomes of all the plan's slices. Not how it is built: "A patient books a free slot
     online and gets a reminder", not "Add the slots table and the text service".
   - `delivers` — one plain sentence: what the plan gives its persona when all its features
     are built.
3. **Write one Feature issue for each feature in `features`,** in the order given, once.
   - `title` — the one thing the feature lets a person do, in one line, in the persona's words.
   - `scope_of_work.goals` — what the feature must do, from the Goal lines of the two ICE.
   - `scope_of_work.limits` — the limits it must stay inside, from the Limit lines.
   - `scope_of_work.expectations` — what is expected: the scenarios, what "done" means, the
     quality needs, from the Expectation, Scenario, Done means, Quality need and Checked by
     lines.
   - `context_guidance` — the four Context lines, in your own words: `read` (what to read),
     `never_read` (what never to read), `persona` (who it serves), `in_out` (what is in and
     what is out). Say where to look; never copy the facts themselves.
   Do not write `written_from` or the `Represents:` line: the play's `write_work_items.py`
   adds both from its own records.
   Use every line of the two ICE that the clean copy holds. Say each thing in the Feature
   issue's own words; do not paste the ICE.
4. **Never write a failure or recovery condition.** Not in a title, a goal, a limit, an
   expectation, a Context line or an example. Never write the words "Fails if", and never
   the phrases "the builder can fix this alone" or "a person must decide". A limit says what
   the feature must stay inside; it is not a failure said the other way round.
5. **Fix mode.** Rewrite only the epic or the Feature issue each problem names, and keep every
   other draft as it is.
6. **Change mode.** Draft again what the product owner's change names, and keep the rest.

## Story mode (/reshape-plan, #1002)

When `skill_input` reads `"mode": "story"`, it holds one feature (`id`, `one_line`, `clean_ice`)
and no slice: an /reshape-plan session needs the text of one feature the person named. Write
that one text only, by step 3 and step 4 above, from the one clean copy — no epic. The output is
`{"stories": [{"feature", "title", "scope_of_work", "context_guidance"}]}`, written to the `out`
path the play gives (`story-draft-<i>.json`) in place of `drafts.json`; the play's
`feature_ice.py body` checks it the way `check_drafts.py` checks the Feature issues.

## Output

`drafts.json`:

```json
{"epic": {"title": "A patient books a free slot online and gets a reminder",
          "delivers": "A patient picks a free slot on a phone, and a reminder comes the day before."},
 "features": [{"feature": "ft-pick-a-free-slot",
               "title": "A patient picks a free slot",
               "scope_of_work": {"goals": ["A patient picks a free slot, and it is booked for them."],
                                 "limits": ["Only slots the doctor opened are shown."],
                                 "expectations": ["The booked slot shows on the confirmation page."]},
               "context_guidance": {"read": "the clinic's opening hours",
                                    "never_read": "patient health records",
                                    "persona": "the patient on a phone",
                                    "in_out": "in: open slots; out: moving a booking"}}]}
```

Examples from different fields:
- A shop: epic "Shoppers pay without an account"; Feature issue "A guest pays by card" —
  goals: a shopper pays by card with an email only; limits: no account is made; expectations:
  the shopper sees an order number; read: the payment rules; never read: saved card data.
- A bank: epic "A small business gets a loan decision on the same day"; Feature issue "The
  application gets a score" — goals: each application gets a score; limits: from the sent
  documents only; expectations: the score is on the application within one hour; persona:
  the credit officer.
- A school: epic "Parents see their child's marks online"; Feature issue "A parent sees this
  term's marks" — limits: a parent sees only their own child; in: this term's marks; out: last
  year's reports.

## Rules

- Draft only. Never write the tracker, the plan file, the product model or the evals folder;
  the play's `check_drafts.py` checks the drafts and `write_work_items.py` writes them after
  the product owner's yes.
- Read only `skill-input.json` and the clean copies. Never open an ICE page or `gather.json`.
- One epic for the plan. One Feature issue draft for each ready feature, once, no more; none
  for a feature that is not ready. No Story.
- Plain words (ASD-STE100), personas only, no real names.
