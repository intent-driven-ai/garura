---
name: propose-answers
description: For each gap a loop's search could not close and only the person can confirm — who may decide, how we will know it works, how big it will get — draft our own proposed answer from what the loop's sources, memory and run already show, with its basis and the context the person needs to judge it, so the person confirms or corrects instead of answering a bare question. Closes as settled a gap the context already answers (an internal tool is not asked how it earns money). Used by the knowledge-builder agent in the loop's knowledge step (Shared Loop Run, R5c), and by the product-os-keeper agent in /shape-slice (one proposal per gap question; the play's record_questions.py merge-proposals copies them into the questions). A value with no source gets no proposed answer.
user-invocable: false
model: sonnet
allowed-tools: Read, Write, Glob, Grep
---

# propose-answers

A person who gave a loop a prototype knows what it is for. A list of questions makes them do
the loop's work. This skill does that work: it drafts the answer we would put, from what we
already saw, and shows why — so the person only says yes or corrects.

## Input

| Field | Required | Meaning |
|-------|----------|---------|
| `gaps` | yes | The gaps only the person can confirm, each with its id, its plain question, what is missing, and any partial answer. For the loop's knowledge step: the search groups still `partly` or `open` that research cannot answer. For /shape-slice: `questions.json`, one gap per question (its `id` is the group) |
| `sources` | yes | What the answers may rest on. For the loop's knowledge step: the loop's Source evidence (for a prototype: views, journeys, the page) and the memory lines the agent read for the gap, each with its trace. For /shape-slice: `gather.json` and its short-term copies (the model pages and memory lines read), and the question record (a person's earlier answers) |
| `run` | yes | What the run made. For the loop's knowledge step: the proposed intents, the domain, its capabilities (the product model's files for this run). For /shape-slice: the intent page |
| `out` | yes | Where to write the proposals (`<working>/proposals.json`) |

## Process

1. For each gap, ask first: **does the context already settle it?** A product the prototype shows
   as an internal tool has no revenue question; a tool the prototype shows one person using is
   not asked about teams of thousands. If so, close it `settled`, say what settles it, and name
   what that rests on (`basis`: the quote, screen or trace). A settled point is shown to the
   person in the brief; it is never dropped silently.
2. Otherwise draft **our proposed answer** — the answer we would put if no one corrected us:
   - start from what the source shows (one reviewer on every screen → "the person who asked
     decides"), what memory holds, and what the run made (a counter of what waits → "settled
     when nothing waits");
   - make it concrete and checkable (a number, a role, a rule), never "it depends";
   - a value the person must set (a target, a period) that no source names gets no proposed
     answer: leave the gap open, so the person sets it.
3. Write its **basis** as `{kind, ref}`: `kind` is `model` (a model page), `memory` (a memory
   line), `person` (a person's earlier answer) or `source` (the loop's Source evidence: a
   quote or a screen); `ref` names the page and lines, the memory path and lines, the question
   id answered, or the screen. Write its
   **context** — the one or two facts the person needs to judge it without opening the
   prototype.
4. Never write a question as a proposal, and never answer from the model alone. If nothing in
   the source, memory or the run supports an answer, the gap stays open for research
   (`author-knowledge-page`) — not a guess.

## Output

`proposals.json`: `{"proposals": [{"group", "closed_by": "proposal | settled", "answer",
"basis": {"kind", "ref"}, "context", "why"}]}` — `answer`, `basis` and `context` for a
proposal; `why` and `basis` for settled.

```json
{"proposals": [
  {"group": "Q-payment-1", "closed_by": "proposal", "answer": "A patient pays at the desk after the visit.",
   "basis": {"kind": "model", "ref": "product/product-os/care/booking/capability.md:18-19"},
   "context": "The booking page names no payment step.", "why": ""},
  {"group": "Q-revenue-1", "closed_by": "settled", "answer": "",
   "basis": {"kind": "source", "ref": "the prototype has no pricing, plan or customer screen"},
   "context": "", "why": "An internal tool earns no money."}]}
```

For /shape-slice only the kinds `model`, `memory` and `person` count: the play's script sets
no proposed answer for any other kind, or for an empty `ref`.

## Rules

- No basis, no proposal: every proposed answer names what it rests on. A value with no source
  gets no proposed answer — never a default in its place.
- Sample data is sample data: the shop inside a review tool's mockup tells you how the tool
  shows things, not facts about the tool's own users.
- Never decide for the person; a proposal is what they confirm or correct.
