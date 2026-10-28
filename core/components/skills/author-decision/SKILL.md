---
name: author-decision
description: 'Draft a decision record (ADR) from the one ADR template (standards/templates/adr.md), in either of its two shapes — a Markdown ADR for Garura''s own decisions (docs/adr/NNN-<slug>.md) or a decision.yaml record for a product decision — from a decision brief and the context the adr-keeper agent gathered: the older ADRs it supersedes or amends (with what part), what it affects, its effect on agent intent (ICE), and its business-intent check. Always writes the record as proposed; only a person accepts it, through the /record-decision play or the calling play''s review. Its bundled scripts/adr.py does the mechanical work — next number, lint, index, overlap candidates, forward pointers, accept, and the business-intent guard. Generative artifact production for /record-decision, and for plays that record product decisions once they are wired to it (follow-up). Use when a decision needs to be written down as an ADR.'
user-invocable: false
model: opus
allowed-tools: Read, Write, Glob
---

# author-decision

Writes the **draft** of one decision record from the template at
`standards/templates/adr.md`. The template has one set of core fields and two shapes:

- **Markdown** — Garura's own ADRs, `docs/adr/NNN-<slug>.md`, read by people.
- **YAML** — a product decision, a `decision.yaml` record (with the #632 fields) in the product model.

You draft; you never accept. Every record you write has status `proposed`. A person accepts it
— by hand through the `/record-decision` play, or at the review of the play or loop that made the decision.

## Input

| Field | Required | Meaning |
|-------|----------|---------|
| `brief` | yes | The decision brief (`<working>/brief.md`): what is decided, why now, the options considered, who is deciding, where it was decided |
| `context` | yes | The gathered context (`<working>/adr-context.yaml`) from `adr-keeper`: the shape, the number or id, the older ADRs it supersedes or amends (each with the part), what it affects, its ICE impact, its business-intent check, related ADRs, and the points for the person who accepts it (`for_the_accepter`), each with its five parts |
| `template_path` | yes | The short-term copy of `standards/templates/adr.md` that template-manager wrote and the play handed to `adr-keeper` |
| `draft_path` | yes | Where to write the record |

## Process

1. **Read the template** — its core fields, its rules, and the shape the context names.
2. **Read the brief and the context.** The context's supersede/amend list, affects list, ICE
   impact and business-intent check are the agent's judgment — use them as given; if one looks
   wrong, say so in the draft's Context, never silently change it.
3. **Write the title as a statement** of what is decided, not a topic ("Keep the cache in
   memory for now", not "Caching").
4. **Write Context, Decision, Consequences and Alternatives** in plain words a stranger reads
   cold. Number the Decision's parts when there are several. Every alternative says why it
   lost. Consequences name what gets harder or riskier, not only what improves.
5. **Write "For the Person Who Accepts This"** when the context lists points for the accepter
   (`for_the_accepter`): one sub-heading per point, each with its five parts from the template
   (what and where, what is wrong or worth knowing, why it matters, what this decision does,
   what you decide). Give the detail itself, never a summary: which page, which lines, which
   names, which agent, which rule. A finding you only mention in passing in Context belongs
   here instead.
6. **Fill the header (Markdown) or the fields (YAML)** from the context: status `proposed`,
   level, `decided_in`, supersedes and amends (each with the part), affects, ICE impact,
   business-intent check. Leave `decided_by` (Markdown) or `metadata.accepted_by` (YAML) empty —
   it is filled when a person accepts.
7. **Never write a forward pointer on an older ADR**, and never change an older ADR. The play
   does that, after acceptance, with `scripts/adr.py pointer`.
8. **Check your own draft against the template's rules** before you return it. The agent runs
   the linter and the guard on it (`scripts/adr.py lint` / `guard`); you have no shell, so you
   cannot accept an ADR or write a pointer — those are the play's, after a person's word. A
   business-intent check of `instance` stays as the context says — the play takes it to the
   person.

## Output

Write `draft_path` and return its path — never the content:

```yaml
draft_path: <path>
shape: markdown | yaml
```

## Scripts

`scripts/adr.py` (tests: `scripts/test_adr.py`) — deterministic, no git, no LLM. Run by the
`adr-keeper` agent (number, overlaps, lint, guard) and by the `/record-decision` play (index, pointer,
accept — only after a person's word); this skill does not run it:

| Command | What it does |
|---------|--------------|
| `number --dir docs/adr` | the next free ADR number |
| `lint --adr <file>` | checks a record against the template, either shape |
| `index --dir docs/adr --out docs/adr/_index.md` | writes the ADR index |
| `overlaps --adr <new> --dir docs/adr` | older ADRs it may supersede or amend — candidates for the agent to judge |
| `pointer --older <f> --newer <f> --kind amended\|superseded [--what <part>]` | writes the forward pointer on an older ADR — the only edit an accepted ADR ever gets |
| `accept --adr <f> --by <person> --date <d>` | proposed → accepted, naming the person |
| `guard --adr <f> [--intents-dir <dir>]` | exit 4 when the decision would change a person's business intent |

## Constraints

- **Draft only, always proposed.** Only a person accepts.
- **Old ADRs are never edited** — not by this skill. Pointers are written by the play, after acceptance.
- **Never change a business intent.** A decision that would change a person's business intent is
  recorded with `business_intent_check: instance` and goes to the person.
- **Plain words.** Written for the person who reads it cold.
