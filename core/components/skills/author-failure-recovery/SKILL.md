---
name: author-failure-recovery
description: Draft, for each feature of a slice, its entry in the slice's hidden file — one recovery for each "Fails if" line of the feature's ICE and of its capability's ICE (when it shows, the way back, and who fixes it, "the builder can fix this alone" or "a person must decide"), by standards/rules/expectation-generation.md, "A feature's recovery". It reads the lines its agent put in short-term memory (write_hidden_file.py lines), drafts only the entries that are not kept, and says when one of the two ICE is thin. Draft only — it never writes the hidden file; the play's write_hidden_file.py checks the draft and writes it. Generative artifact production for /shape-slice (ontology v11, ADR 052). Use when /shape-slice needs the recoveries of a slice's features drafted.
user-invocable: false
model: opus
allowed-tools: Read, Write
---

# author-failure-recovery

A slice's hidden file tells the eval what must never happen when a person tests the slice,
and what to do when it does. Each "Fails if" line of a feature's ICE, and of its capability's
ICE, gets exactly one recovery. This skill drafts those recoveries. The play's script lists
the lines before it and checks and writes the file after it, so this skill does only the
judgment: what the eval sees, the way back, and who can fix it.

## Input

| Field | Required | Meaning |
|-------|----------|---------|
| `lines` | yes | `hidden-lines.json` from `write_hidden_file.py lines`: the slice, its home plan, the file's path, and for each feature its capability, which ICE is thin, whether the entry is `kept`, and its lines `{id, from, text}` |
| `ice_pages` | yes | The pages that hold the two ICE of each feature that is not kept (the part's page with its `## Agent intent (ICE)` section, or its `ice.md`), so the recovery fits the goal and the limits |
| `rule` | yes | The copy of `standards/rules/expectation-generation.md` that the agent put in short-term memory (the handoff rule and "A feature's recovery") |
| `out` | yes | Where to write `hidden-recoveries.json` |

## Process

1. **Skip each kept entry.** An entry with `kept: true` is already in the file. Draft nothing
   for it; the script keeps it byte for byte.
2. **For each line of each other entry, draft one recovery** by the rule:
   - **when** — the "Fails if" line said again as a symptom that the eval can see from the
     outside, on the slice's surface. Not a cause, not a guess about the code.
   - **way back** — the opposite of the failure: the state that must be true again, as
     guidance a builder or a person can follow. Never code, never a file name, never a
     command.
   - **who fixes** — exactly one of the two phrases:
     - `the builder can fix this alone` — the way back is a change the builder controls and
       can make from what it already has (a wrong order, a missing check, a lost message);
     - `a person must decide` — the way back needs judgment or authority the builder does
       not have: money goes out or comes back, a person's data is shown to the wrong
       person, an approval, a choice between options that the ICE does not settle, or
       anything that cannot be undone.
3. **One recovery per line, no more.** Never merge two lines into one recovery, and never
   split one line into two.
4. **Say when an ICE is thin.** When the entry's `thin` names the feature ICE or the
   capability ICE, write a short `thin_note` for the entry: which ICE is thin, and that its
   recovery may be weak until `/discover-capabilities` deepens it. Do not stop, and do not
   send the person anywhere.
5. **A line you cannot judge** — a "Fails if" line too vague to say what the eval sees — still
   gets one recovery: write the symptom as plainly as the line allows, and mark who fixes as
   `a person must decide`. Add the line's id to `vague` so the agent can tell the person.

## Output

`hidden-recoveries.json`:

```json
{"entries": [{"feature": "ft-pick-a-free-slot",
              "thin_note": "The feature ICE is thin; its recovery may be weak until /discover-capabilities deepens it.",
              "recoveries": [{"line": "F1",
                              "when": "two bookings are on one slot",
                              "way_back": "keep the first booking, free the second, and tell the second patient",
                              "who_fixes": "the builder can fix this alone"}]}],
 "vague": []}
```

Examples from different fields:
- A shop: "Fails if: a card is charged twice" — when: one order has two charges; way back:
  refund the second charge and tell the shopper; who fixes: a person must decide (money goes
  out).
- A school: "Fails if: a note goes home to the wrong family" — when: a parent sees a note for
  a child who is not theirs; way back: take the note back and send it to the right family;
  who fixes: a person must decide (a child's data was shown to the wrong person).
- A clinic: "Fails if: a past slot is offered" — when: the booking screen shows a slot whose
  time has gone; way back: show only slots later than now; who fixes: the builder can fix this
  alone.

## Rules

- Draft only. Never write the hidden file, the spine, a model page or a plan; the play's
  `write_hidden_file.py write` checks the draft (one recovery per line, the two phrases
  only) and writes the file.
- Every recovery traces to one line of `lines`; never add a failure that no ICE holds.
- Plain words (ASD-STE100), personas only, no real names.
- A builder never reads the hidden file. Write nothing a builder needs to build the feature.
