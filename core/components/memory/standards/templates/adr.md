# ADR — Decision Record Template

> The one template every decision record is written from (#632). A decision record IS an ADR,
> at any level (`schemas/product-os/decision.yaml`). It has **two shapes over the same core
> fields**:
>
> - **Markdown** — Garura's own ADRs, `docs/adr/NNN-<slug>.md`, read by people.
> - **YAML** — product decisions, a `decision.yaml` record in the product model, written by the
>   plays that make them. YAML records are machine data: a forward pointer or an acceptance
>   rewrites the record, and comments in it are not kept.
>
> The `/adr` play and the `author-adr` skill write from this template; `adr.py lint` (in the `author-adr`
> skill) checks a record against it. It checks the shape, never the merit — whether a decision is *right* is a
> person's call (`knowledge/review/adrs.md`). Built from `decision.yaml`, that review playbook,
> and the shape ADRs 029–031 share. ADRs written before it stay as they are until they are
> reviewed (#632, A4).

## Core fields — both shapes

| Field | What it holds | Required |
|-------|---------------|----------|
| `id` | Markdown: the three-digit number (`031`). YAML: the record id | yes |
| `title` | The decision in one line, as a statement — not a topic | yes |
| `status` | `proposed`, `accepted`, `superseded` or `rejected`. Only a person moves it to `accepted` or `rejected` | yes |
| `date` | When it was decided (accepted), or proposed | yes |
| `level` | `framework`, `product`, `capability` or `functionality` | yes |
| `node_ref` | The part of the product it affects; empty for a framework ADR | product levels |
| `accepted_by` | The PERSON who accepted it; empty while proposed. Markdown: the **Decided by:** line. YAML: `metadata.accepted_by` (YAML's `metadata.decided_by` keeps its original meaning: the play that recorded it) | once accepted |
| `decided_in` | Where it was decided — the issue, the run, the review | yes |
| `supersedes` | Older ADRs it replaces, in full or in part (each with what part) | when any |
| `amends` | Older ADRs it changes in part, and what part | when any |
| `superseded_by` / `amended_by` | The forward pointers — the ONLY fields ever written on an accepted ADR after it is accepted; a record is superseded in full only once | when any |
| `affects` | The files, rules, schemas, plays and agents the decision changes | yes |
| `ice_impact` | The agent intents (ICE) the decision changes, or `none` — and why | yes |
| `business_intent_check` | `none` — no business intent changes; `kind` — it changes the Business Intent *kind* (framework doctrine), no person's intent; `instance` — it would change a person's business intent: the person is asked, it is never applied by the ADR | yes |
| `related` | ADRs and issues to read with it | no |
| `context` | Why a decision is needed now: the situation and the forces | yes |
| `decision` | What is decided, in plain words, numbered when there are several parts | yes |
| `consequences` | What gets better and what gets harder or riskier | yes |
| `alternatives` | Each option not taken, and why not | yes |
| `work_this_creates` | Follow-up work the decision opens | no |
| `references` | Sources: decisions, issues, files | no |

**Rules**

- An accepted ADR is never edited. A new ADR supersedes or amends it, and the older one gains
  only its forward pointer (`superseded_by` / `amended_by`) and, when superseded in full, the
  status `superseded`.
- Every ADR it supersedes or amends names it back through that pointer — both directions. In
  the YAML shape `superseded_by` holds the one full supersede; an amendment or a supersede in
  part points back through `amended_by`, which can hold many.
- Every Markdown ADR is listed in `docs/adr/_index.md`; `/adr` rebuilds the index after each
  acceptance (`adr.py index`).
- An ADR never changes a person's business intent. `business_intent_check: instance` stops the
  ADR from being applied and goes to the person (ADR 031: only a person confirms or drops a
  business intent).
- Inside a drive, an ADR is written as `proposed` and accepted at the drive's final review; run
  by hand, the person accepts it before it is written as `accepted`.

## Shape 1 — Markdown (Garura's ADRs)

File: `docs/adr/NNN-<slug>.md`. Headings in this order; header lines are bold field lines.

```markdown
# ADR NNN — <Title as a statement>

**Status:** Proposed | Accepted | Superseded by [ADR MMM](MMM-<slug>.md) | Rejected
**Date:** YYYY-MM-DD
**Level:** framework | product | capability | functionality
**Decided by:** <person> · **Decided in:** #<issue> (<what kind of work>)
**Supersedes:** ADR MMM (<in full | in part — what part>) · …            (omit when none)
**Amends:** ADR MMM — <what part> · …                                      (omit when none)
**Affects:** <files, rules, schemas, plays, agents>
**ICE impact:** <the agent intents it changes, or "none — <why>">
**Business intent check:** none | kind — <which kind> | instance — <flagged to the person>
**Related:** <ADRs and issues>                                              (optional)

## Context

<Why a decision is needed now.>

## Decision

<What is decided. Number the parts when there are several: "### 1. …">

## Consequences

### Positive

- <…>

### Negative / Risks

- <…>

## Alternatives Considered

- **<Option>** — <why not>.

## Work This Creates                                                         (optional)

- <…>

## References                                                                (optional)

- <…>
```

A forward pointer on an older Markdown ADR is written into its `**Status:**` line only:
`Accepted — amended in part by [ADR MMM](MMM-<slug>.md): <what changed>` or
`Superseded by [ADR MMM](MMM-<slug>.md)`.

## Shape 2 — YAML (product decisions)

A `decision.yaml` record (the core fields above, added in #632 without changing the original ones):

```yaml
decision:
  id: <id>
  title: <the decision as a statement>
  status: proposed | accepted | superseded | rejected
  level: framework | product | capability | functionality
  node_ref: <the node it affects — empty for framework or product level>
  reason: <context and decision, in plain words>          # v1 field: context + decision
  alternatives:
    - { name: <option>, why_not: <why> }
  supersedes: [ { id: <older id>, part: full | <what part> } ]
  amends: [ { id: <older id>, part: <what part> } ]
  superseded_by: <id or null>
  amended_by: [<ids>]
  affects: [<files, rules, schemas, nodes>]
  ice_impact: <the ICE it changes, or "none — why">
  business_intent_check: none | kind | instance
  consequences: { positive: [<…>], negative: [<…>] }
  metadata:
    decided_by: <play that recorded it>                    # v1 meaning kept
    accepted_by: <person, once accepted>
    decided_in: <issue or run>
    date: <date>
    version: <n>
```

## Gold example — Markdown

ADR 031 (`docs/adr/031-business-intent-and-ice.md`) is the nearest written example; written
from this template its header would read:

```markdown
# ADR 031 — Business Intent and ICE: Two Levels, Written Freely, Worked Only When Confirmed

**Status:** Accepted
**Date:** 2026-10-09
**Level:** framework
**Decided by:** the owner · **Decided in:** #612 (the /intent play) and the review of PR #631
**Amends:** ADR 029 — §6, what /intent and /vision do in Kickoff · ADR 027 — the IDSD row · ADR 026 — /intent by hand confirms before it writes
**Affects:** ontology.md (v3), spine.yaml, every lint_grounding.py copy, play-creator, gate-config.md, direct-model-write.md
**ICE impact:** ICE may be written before its capability has a domain; an ICE is workable only when built from a confirmed business intent
**Business intent check:** kind — the Business Intent and ICE kinds change; no person's business intent changes
```
