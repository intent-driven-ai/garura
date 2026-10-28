---
name: author-slice-brief
description: Write the opening of a /shape-slice brief — the early brief (the questions asked before the slice is shaped) or the confirmation brief (the slice shown for the person's yes) — in two or three plain sentences that say what the person decides and what happens with the reply, by the rule for asking a person, or by the play's floor when gather.json has rule_missing. Writes the opening only; the play's render_brief.py builds the rest of the brief from the run's records. Generative artifact production for /shape-slice. Use when /shape-slice needs the opening of its early or confirmation brief.
user-invocable: false
model: sonnet
allowed-tools: Read, Write
---

# author-slice-brief

The person reads the opening of a brief first. It must tell them, in a few plain words, what
they decide now and what the run does with their reply. This skill writes only that opening.
The rest of the brief — the slice, the hidden file, the assumptions, each question with its
four parts — is built by the play's `render_brief.py` from the run's records, so no part can
be left out.

## Input

| Field | Required | Meaning |
|-------|----------|---------|
| `kind` | yes | `early` (the questions asked before the slice is shaped) or `confirmation` (the slice, for the person's yes) |
| `intent_page` | yes | The business intent's page: its title is what the person knows the work by |
| `split` | yes | For `early`: `early-split.json`, the questions asked first. For `confirmation`: `brief-split.json`, the questions still open |
| `slice` | for `confirmation` | `slice.json`: the slice's name, its surface and its tester |
| `intent_page_record` | for `confirmation` | `intent-page.json`: `written: true` when this run wrote the intent page from the issue |
| `gather` | yes | `gather.json`: when it has `rule_missing`, use the floor below |
| `asking_rule` | yes | The shared rule for asking a person, `_shared/asking-a-person.md`, beside the installed skills (`../_shared/asking-a-person.md` from this skill's folder); it is not memory |
| `out` | yes | Where to write the opening (`early-opening.md` or `opening.md`) |

## Process

1. **Read the rule for asking a person** (`asking_rule`). When `gather` has `rule_missing`,
   follow the floor: an opening that says what the person decides; plain words; personas.
2. **Write two or three sentences, no more:**
   - what the person decides now, with the word "decide" — for `early`, the answers the
     slice cannot be shaped without; for `confirmation`, whether the slice that shows the
     business intent "<title>" is served is right;
   - what happens with the reply — for `early`, the run shapes the slice after the answers
     and shows it in one brief; for `confirmation`, yes keeps it, change sends it back, stop
     undoes every write;
   - for `confirmation`, when `intent_page_record` reads `written: true`, that the run wrote
     the intent page from the issue.
3. **Name a question id only when it helps** ("Answer Q-payment-1 first"). Never repeat a
   question's text: the script puts each question under the opening.

## Output

The opening as plain text, with no heading, at `out`:

```
You decide whether the slice "Self booking" shows that patients can book their own visits
online. Type yes to keep it, change with what to change, or stop to undo every write. The run
wrote the business intent's page from the issue, because the model had none.
```

Examples from different fields:
- A shop, early: "You decide two things the run cannot find in the model before it shapes the
  checkout slice. After your answers, the run shapes the slice and shows it to you in one
  brief."
- A school, confirmation: "You decide whether the slice "Send a note home" shows that
  teachers can reach each family. Type yes to keep it, change with what to change, or stop to
  undo every write."

## Rules

- Two or three sentences; the opening says what the person decides.
- Plain words (ASD-STE100), personas only, no real names, no file paths, no ids of model
  parts.
- Write the opening only; never the brief, a question or an answer.
