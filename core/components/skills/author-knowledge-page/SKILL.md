---
name: author-knowledge-page
description: Draft one knowledge page for a topic a loop found missing from memory — something no screen shows and research can answer (a speed bar for a kind of product, the rules that apply to a kind of record, the usual roles in a kind of team) — researched with its sources. One page answers every question of its topic. Marks the page for the project's memory when it is a fact about the product or its team, not about one loop. Draft only — the knowledge-builder agent raises the page through the memory tool as a memory update a person approves (ADR 035, ADR 059); the skill never calls the memory tool. Used by the knowledge-builder agent in the loop's knowledge step (Shared Loop Run, R5c).
user-invocable: false
model: opus
allowed-tools: Read, Write, WebSearch, WebFetch
---

# author-knowledge-page

Some questions no prototype could answer, because they are not about screens: how fast a
review page must respond, whether GDPR applies to review records, who in a software team may
approve what. Asking the person each one is slow and asks them to be an expert. Instead, this
skill drafts the knowledge once, with its sources, for the person to approve.

## Input

| Field | Required | Meaning |
|-------|----------|---------|
| `topic` | yes | The topic (e.g. "speed bar for a review tool's pages") and the questions it must answer |
| `context` | yes | What the loop knows of the product — its intents, its domain — from the step's working files |
| `draft_path` | yes | Where to write the draft, in the loop's working folder (`<working>/knowledge-round-<n>/pages/<topic-slug>.json`) |

## Process

1. List what the page must let an agent answer — every question in the topic.
2. Research: standards, common practice, the law, well-known references. Keep each source's
   link and what it says. Prefer one clear source to many weak ones.
3. Write the page in plain words, as knowledge an agent can use on any later loop for this
   product: the facts, the usual values, the choices and when each applies. Mark what is a
   choice the person must make (a target they set), not a fact.
4. Say whether the page belongs in the **project's memory** (`for_project_memory: true`): a
   fact about this product or its team that every later loop needs. Moving it there is a
   person's promotion, later.
5. Write the draft to `draft_path`. Never write memory, and never call the memory tool: the
   agent raises the page as a memory update.

## Output

`draft_path` holds:

```json
{
  "missing": "<the topic, in one line>",
  "slug": "<topic-slug>",
  "draft": "<the page, Markdown>",
  "sources": ["<each link>"],
  "for_project_memory": true
}
```

Return its path — never the content.

## Rules

- Draft only. Never decide, apply or promote an update, and never raise one; a person decides
  (ADR 035, ADR 039).
- Every fact on the page has a source; a value the person must choose is marked as a choice.
