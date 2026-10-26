# Approval Prompt Format

The one format for a checkpoint: the place where a play stops and a person decides. Every
play that waits for a person's approval uses this format. A play does not write its own
prompt text.

Consumers: every checkpoint-gated play.

## Shape

```markdown
## {Stage title} — {product or issue slug}

{Opening — two or three plain sentences. What the person decides, and what happens
with their answer.}

**Under review:**
- `{path/to/primary-artifact}` — {one line: what it holds}
{add more paths as needed}

{Optional note — one to three lines. Only for something the person must know: this is
a second round after a change they asked for, or a check found a warning.}

### Question 1

- **Question:** {the one thing the person decides, in plain words}
- **Answer:** {the real answer the draft gives, in general words. If there is no
  answer yet, write the proposed answer and say "proposed".}
- **Why it matters:** {what goes wrong, or what changes, if the answer is wrong}
- **Example:** {several examples from different domains — for example a clinic, a
  shop and a bank}

### Question 2

{the same four parts}

---

Reply **yes** to go on, **change: {what to change}** to run {this stage} again with
your change, or **stop** to end the run.
```

## Before you show it

- Each question asks one thing. A question with an "and" in it is two questions.
- Read each question back with no context: not the issue, not the other questions, not
  the files. Show it only when a stranger could answer it. If a stranger could not,
  rewrite it.
- Plain English in the style of ASD-STE100: short sentences, one idea each, common words.
- Personas only (for example "the clinic manager"). Never a real person's name.
- Never paste the whole artifact. Give its path under **Under review**.

## Field rules

| Field | Rule |
|-------|------|
| Stage title | Sentence case. Names the stage the person approves (for example "Market brief", "Domain selection"). Never a general word ("Review", "Checkpoint"). |
| Product / issue slug | The slug from the play's context. The same slug in every checkpoint of one run. |
| Opening | Two or three sentences. Says what the person decides and what happens next. Counts help ("12 capabilities kept, 2 dropped"). |
| Under review | Full paths from the workspace root, each with one line that says what it holds. |
| Optional note | Only for a second round, a warning, or a fact the person cannot see from the draft. |
| Questions | One block for each decision, with the four parts in order: Question, Answer, Why it matters, Example. |
| Reply line | Always this line: `Reply **yes** to go on, **change: {what to change}** to run {this stage} again with your change, or **stop** to end the run.` |

## Reading the reply

The reply is a plain typed answer.

| Reply | Meaning | Action |
|-------|---------|--------|
| `yes` (or `y`, `approve`, `go`) | Approved | Set the checkpoint to `APPROVED` and go to the next step. |
| `change: {text}` (or other text that asks for a change) | Change asked for | Keep the text. Set the checkpoint to `CHANGE_REQUESTED`. Run the step that made the draft again, with the text as added context. Then show the checkpoint again. |
| `stop` (or `no`, `cancel`) | Rejected | Set the checkpoint to `REJECTED`. Clean up as the play's intent says (branch, drafts). Halt. |
| Anything else | Not clear | Ask again: "Reply yes, change: <what>, or stop." Show the prompt again. |

**Do not use `AskUserQuestion` for checkpoints.** Show the prompt text and wait for the
typed reply. This is a global rule from CLAUDE.md.

## Gate switch (#466, three kinds per #467)

Before rendering, resolve the checkpoint's switch per `standards/rules/gate-config.md`
(first match wins):

0. **Pinned** (declared in the play: `class: <class>, pinned`) → always render and wait.
   No config value, policy, or ledger can turn a pinned gate off.
1. `gates.plays.<play>` — explicit per-play override.
2. **Conditional plays only** (the eleven document plays — vision, understand, shape,
   roadmap, and the seven realize lenses): consult the learned policy —
   `classify_change.py` names the change's shape key; a shape in the policy's `auto:`
   block (and not in `never_auto:`) → **auto-pass**; anything else → on. A draft
   carrying ANY blocking finding (lint gap, grounding-eval fail) → on, regardless of
   policy.
3. `gates.classes.<the class this checkpoint declares>` — each checkpoint declares its
   risk class in the compiled play (`class: docs-only | standard | one-way-door`;
   undeclared ⇒ standard).
4. `gates.default` → absent ⇒ on.

- **on** → render and wait, exactly as above. Afterwards, a conditional play appends the
  live-eval line (`gate_eval.py append`): shape, `predicted: gate`, and the human's real
  action (`approved_clean` | `approved_edited` | `rejected`).
- **auto-pass** (conditional plays) → do NOT wait: record `gate auto-passed by learned
  policy (shape: <shape-key>, policy v<version>)` as a Checkpoint Decisions row, include
  the draft's diff summary in the run record, append the ledger line
  (`predicted: auto, human: auto_pass`), and proceed. An auto-pass is always visible in
  the run record — never silent.
- **off** → do NOT wait: record `gate skipped by config (<resolution path>)` as a
  Checkpoint Decisions row in the evidence file and proceed. A skip is always visible in
  evidence — never silent.

The switch gates human checkpoints ONLY. Pre-flight halts, sensitive-file blocks,
stop-condition gates, and eval failures are machine walls and never resolve here.

## Example

```markdown
## Domain selection — appointment-booking

You decide which business areas the product covers first. When you approve, the next
step writes the capabilities for these areas only. Areas you leave out wait for a later
round.

**Under review:**
- `.garura/product/product-os/_spine.yaml` — the areas, kept and dropped, with reasons

### Question 1

- **Question:** Must the first release take payment when a person books?
- **Answer:** Proposed: no. The first release books a time and sends a reminder. Payment
  comes in a later release.
- **Why it matters:** If payment is needed at booking, the first release must also
  cover refunds and failed payments. That makes it about twice as large.
- **Example:** A clinic often takes payment after the visit. A hair salon may take a
  deposit at booking. A bank branch takes no payment for an appointment.

### Question 2

- **Question:** Can one person book for another person?
- **Answer:** Proposed: yes. A parent can book for a child, and a carer for the person
  they care for.
- **Why it matters:** If the answer is no, families and carers must make an account for
  each person. Many will not.
- **Example:** A parent books a child at a clinic. An assistant books a manager at a
  bank. A person books a friend at a shop's repair desk.

---

Reply **yes** to go on, **change: {what to change}** to run domain selection again with
your change, or **stop** to end the run.
```

## Related

- `checkpoint.md` — the file the play writes next to the prompt
- `delivery-report.md` — the final report a play gives at close (not a checkpoint)