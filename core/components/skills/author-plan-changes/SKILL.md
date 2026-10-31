---
name: author-plan-changes
description: Turn one instruction a person gives in an /update-plan session, in their own words, into the list entries it means for the plan — a status set, an item added (an issue that exists, or a new one), moved, renamed, given a new text or a new kind, a new feature found while the plan is in progress, or the plan's own Status or Direction — read against the plan file, the issues as the tracker holds them now and the list so far. Asks a question instead of guessing when the words fit two readings or name no item. Writes draft-entries.json only; the play's check script tests each entry against the plan's rules, and nothing reaches the plan file, the tracker or the model before the person approves the whole list. Generative artifact production for /update-plan (#730), through project-orchestrator.
user-invocable: false
model: sonnet
allowed-tools: Read, Write
---

# author-plan-changes

A person talks to `/update-plan` in their own words: "#730 is done", "drop #909", "put #1001
under #730", "change the scope of #730 to …", "set the plan to Paused, direction 2", "we found
a new feature: a person can undo the last update". This skill turns one such instruction into
the list entries it means. It decides what the words mean; it does not check the rules (the
play's script does) and it writes nothing but its draft.

## Input

| Field | Required | Meaning |
|-------|----------|---------|
| `instruction` | yes | The person's words, as typed |
| `plan_file` | yes | The plan file on the plan's branch |
| `snapshot` | yes | `snapshot.json`: each issue of the plan as the tracker holds it now (title, type, state, close reason, text, parent) |
| `changes` | yes | `changes.yaml`: the list so far (empty at the start) |
| `out` | yes | Where to write `draft-entries.json` |

## Process

1. **Find what the words name.** Each issue number the person gives, or the item whose title
   their words plainly name. When the words could name two items, or none, do not pick one:
   write a question (step 4).
2. **Write one entry for each change the words ask for**, by its `op`:

   | op | When the person… | Fields |
   |----|------------------|--------|
   | `status` | says an item is done, dropped, started, being worked on now, blocked, or not started | `issue`, `to` (Not Started, In Progress, Now, Blocked, Done, Dropped) |
   | `add` | puts an issue into the plan, or asks for a new one | `issue` (null for a new one), `kind` (epic, feature, story, spike, chore, bug), `parent`; for a new one also `title` and `body`; for a new story the person ties to a feature of the product model ("add the story for feature X"), also `feature_ref`: the feature as the person named it (its id, its short name or its page title), and `body` in their words — the play finds the feature and drafts the story from its ICE when it has one |
   | `move` | puts an item under another parent | `issue`, `to` (the new parent) |
   | `retitle` | renames an item | `issue`, `to` (the new title) |
   | `text` | changes what an item's text says | `issue`, `body` (the whole new text: every line of the old text kept except the lines the person changed), `summary` (one line: what changed) |
   | `kind` | says an item is another kind | `issue`, `to` |
   | `new-feature` | names a feature the plan did not know about | `issue` (null, or the story that exists for it), `title`, `parent` (where the person wants its story), `description` (the person's words about what a person can do), and `capability` only when the person names it (the play's script places the rest) |
   | `plan-status` | sets the plan's own status | `to` (Not Started, In Progress, Paused, Done, Dropped) |
   | `plan-direction` | sets the plan's direction | `to` (1, 2, 3, or null for none) |

   When the person asks where an item sits in the product model ("find this story in the model",
   "which feature is #931"), write no entry: add `{"story": <n>}` (or `{"ref": "<their words>"}`
   for a feature) to `model_lookups`; the play answers from the model.

   Give only the new value; the play's script reads the old one from the plan file and the
   tracker. "Finish #730 and its chores" is one `status` entry for each item. A change the person
   did not ask for is never added, even when it looks owed (a parent closed because its
   children are done): there are no roll-ups.
3. **Keep the person's words.** A new title, a new text and a description use the person's own
   words, in plain English, with personas, never a real name.
4. **Ask when unsure.** Read `_shared/asking-a-person.md` (laid beside the installed skills) and
   write each question in `questions` in its four parts: `question` (the one thing the person
   decides, naming the item), `answer` (the two readings you see, or the answer you propose, and
   that it is proposed), `why` (what goes wrong if the answer is wrong) and `examples` (several,
   from different domains). Read each back with no context; a stranger must be able to answer
   it. Write no entry for a part you asked about.
5. **Write `draft-entries.json`.** Check it parses, and that each entry has its fields.

## Output

```json
{"instruction": "#730 is done; rename #931 to 'Add a feature found mid-plan'",
 "entries": [{"op": "status", "issue": 730, "to": "Done"},
             {"op": "retitle", "issue": 931, "to": "Add a feature found mid-plan"}],
 "questions": []}
```

A question, when the words fit two readings:

```json
{"question": "Should 'drop the reminder' drop story #44 'Send a reminder', or only its chore #47 'Retry a failed SMS'?",
 "answer": "Two readings: drop the story and the work under it, or drop the chore only.",
 "why": "Dropping the story closes it on GitHub and takes it out of the plan; the chore alone leaves the story open.",
 "examples": ["a clinic: drop the whole reminder story", "a shop: drop only the retry chore of the receipt story",
              "a bank: drop the alert story and its chores"]}
```

Examples from different fields:
- A clinic plan: "the reminder story is blocked on the SMS contract" → `status` of the story
  named "Send a reminder", `to: Blocked`.
- A shop plan: "drop the guest wish list, we are not doing it" → `status`, `to: Dropped`.
- A bank plan: "the upload story needs a chore to move the limits to config" → `add`, a new
  chore under that story, with the person's words as its title.

## Rules

- Only what the person asked for, in their words; never a roll-up and never a guess.
- Draft only: never write the plan file, the tracker, the model or the list.
- Plain words (ASD-STE100), personas only, no real names.
