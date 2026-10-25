---
name: author-work-items
description: Write, for each slice of a business intent's plan, the epic's title (what a person can see the product do, not how it is built) and one story for each ready feature — its title, its scope of work (goals, limits, expectations) and its Context guidance (what to read, what never to read, the persona, what is in and what is out) — in its own words, from the clean copies of the feature's ICE and its capability's ICE that the play's gather_plan.py wrote. It never opens an ICE page, never writes a failure or recovery condition, and writes plain words with personas. Fix mode rewrites only the parts the play's check_drafts.py names; change mode drafts again with the product owner's change. Writes drafts.json only; the play's scripts check it, show it in the brief and write the tracker after the product owner's yes. Generative artifact production for /shape-plan. Use when /shape-plan needs the epic and stories of a plan drafted, fixed or drafted again.
user-invocable: false
model: opus
allowed-tools: Read, Write
---

# author-work-items

A plan holds one epic for each slice, and one story for each feature of that slice. The
epic tells the eval play what a person can see the product do. Each story tells the build
play what the feature must do, inside which limits, what "done" means, and where to look for
context. This skill writes that text. The play's scripts find the epics and stories that
exist before it, and check, show and write the drafts after it, so this skill does only the
judgment: the words.

## Input

| Field | Required | Meaning |
|-------|----------|---------|
| `gather` | yes | `gather.json` from the play's `gather_plan.py`: the intent and its title, and each slice with its name, outcome and features (`id`, `name`, `one_line`, `capability`, `ready`, `reason`, `ice_pages`, `clean_ice`) |
| `clean_ice` | yes | The clean copies that `gather.json` names, one for each ready feature (`<working>/ice/<feature id>.md`): the feature's ICE and its capability's ICE, with the failure lines taken out. These are the only ICE text you read |
| `problems` | no | Fix mode: the `problems` of `drafts-check.json` (`slice`, `feature`, `problem`) |
| `change` | no | Change mode: the product owner's words after `change:` at the checkpoint |
| `drafts` | no | The drafts.json of the earlier round, in fix mode and change mode |
| `out` | yes | Where to write `drafts.json` |

## Process

1. **Read only the clean copies.** For each ready feature, read its `clean_ice`. Never open a
   page in `ice_pages` or any other ICE page: those pages hold the failure lines, which are
   not yours to read. A feature with `ready: false` gets no story; the play names it in the
   brief.
2. **Write the epic of each slice.**
   - `title` — one line that says what a person can see the product do, from the slice's
     name and outcome. Not how it is built: "A patient books a free slot online and gets a
     reminder", not "Add the slots table and the text service".
   - `delivers` — one plain sentence: what the slice gives its persona when all its stories
     are done.
3. **Write one story for each ready feature,** in the slice's build order.
   - `title` — what the story delivers, in one line, in the persona's words.
   - `scope_of_work.goals` — what the feature must do, from the Goal lines of the two ICE.
   - `scope_of_work.limits` — the limits it must stay inside, from the Limit lines.
   - `scope_of_work.expectations` — what is expected: the scenarios, what "done" means, the
     quality needs, from the Expectation, Scenario, Done means, Quality need and Checked by
     lines.
   - `context_guidance` — the four Context lines, in your own words: `read` (what to read),
     `never_read` (what never to read), `persona` (who it serves), `in_out` (what is in and
     what is out). Say where to look; never copy the facts themselves.
   - `written_from` — the two ICE pages the clean copy names (the feature's, then the
     capability's), as `gather.json` gives them in `ice_pages`.
   Use every line of the two ICE that the clean copy holds. Say each thing in the story's own
   words; do not paste the ICE.
4. **Never write a failure or recovery condition.** Not in a title, a goal, a limit, an
   expectation, a Context line or an example. Never write the words "Fails if", and never
   the phrases "the builder can fix this alone" or "a person must decide". A limit says what
   the feature must stay inside; it is not a failure said the other way round.
5. **Fix mode.** Rewrite only the slice or story each problem names, and keep every other
   draft as it is.
6. **Change mode.** Draft again what the product owner's change names, and keep the rest.

## Output

`drafts.json`:

```json
{"slices": [{"slice": "sl-self-booking",
             "epic": {"title": "A patient books a free slot online and gets a reminder",
                      "delivers": "A patient picks a free slot on a phone, and a reminder comes the day before."},
             "stories": [{"feature": "ft-pick-a-free-slot",
                          "title": "A patient picks a free slot",
                          "scope_of_work": {"goals": ["A patient picks a free slot, and it is booked for them."],
                                            "limits": ["Only slots the doctor opened are shown."],
                                            "expectations": ["The booked slot shows on the confirmation page."]},
                          "context_guidance": {"read": "the clinic's opening hours",
                                               "never_read": "patient health records",
                                               "persona": "the patient on a phone",
                                               "in_out": "in: open slots; out: moving a booking"},
                          "written_from": ["clinic/booking/ft-pick-a-free-slot/feature.md",
                                           "clinic/booking/capability.md"]}]}]}
```

Examples from different fields:
- A shop: epic "Shoppers pay without an account"; story "A guest pays by card" — goals: a
  shopper pays by card with an email only; limits: no account is made; expectations: the
  shopper sees an order number; read: the payment rules; never read: saved card data.
- A bank: epic "A small business gets a loan decision on the same day"; story "The
  application gets a score" — goals: each application gets a score; limits: from the sent
  documents only; expectations: the score is on the application within one hour; persona:
  the credit officer.
- A school: epic "Parents see their child's marks online"; story "A parent sees this term's
  marks" — limits: a parent sees only their own child; in: this term's marks; out: last
  year's reports.

## Rules

- Draft only. Never write the tracker, the plan file, the product model or the evals folder;
  the play's `check_drafts.py` checks the drafts and `write_work_items.py` writes them after
  the product owner's yes.
- Read only `gather.json` and the clean copies. Never open an ICE page.
- One story for each ready feature, no more; none for a feature that is not ready.
- Plain words (ASD-STE100), personas only, no real names.
