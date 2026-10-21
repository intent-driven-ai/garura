---
name: search-kb
description: Search the product knowledge base for where a piece of work belongs — its domain, capability, and functionality — by reasoning over the domain shelves its agent puts in short-term memory. Runs the inference sandwich (list the domains, reason to the domain, read that shelf, reason to the capability/functionality) and emits a lightweight routing-result with the decision and why. Placement only — it does not evaluate product-profile conditions (that is selection, /shape's job). Use whenever a play or agent needs to know which part of the product model a request maps to.
version: 0.1.0
user-invocable: false
model: sonnet
allowed-tools: Bash, Read
---

# search-kb

Routes a **piece of work** to its place in the KB tree: **domain → capability →
functionality**, with the decision and the reasoning recorded. This is C2 (#434).

## Input

| Field | Required | Description |
|-------|----------|-------------|
| `work` | yes | The piece of work to place. |
| `domains_dir` | yes | The domain shelves (`knowledge/domains/*.md`), copied into short-term memory by the agent through the memory tool. The skill reads only these copies — never memory itself (ADR 039). |
| `out_route` | yes | Where to write the routing result. |

Each shelf opens with front matter: `id`, `title`, and `conditions.trigger` (when the domain
applies). That is the routing entry.

## Procedure — the inference sandwich

Reasoning is yours (the skill); the agent only retrieves.

1. **List + reason to the domain (placement).** Read the front matter of every shelf in
   `domains_dir`: its `title` and `conditions.trigger`. Read the ~10 triggers and reason which domains the work belongs to.
   Ask two questions, in order: **which field does the product serve** — judged by what its
   screens or its words are about (what the user works on there) — and **which job does it do
   in that field**. Each answer may be a domain of its own, so a product often sits in more than
   one: name every domain it genuinely sits in, and set `spans_multiple_domains`. A domain no
   shelf holds is recorded as unmatched for the nothing-fits path, by name and with why. This is **semantic placement** — do NOT
   consider product-profile conditions here.
2. **Read the shelf + reason to capability/functionality.** Read the chosen shelf in
   `domains_dir`. Reason over its `## Capabilities` to pick the
   capability and the functionality(ies) the work maps to. Note their profile
   conditions as metadata — do not evaluate them (that is selection, not placement).
   Placement records where the work fits on the shelf; it writes nothing. A caller that
   writes domains only (/vision, ADR 043) uses the capability and functionality placements
   as research notes for the domain page, never as capability entries.
3. **Emit the routing result** (schema below) with `why` for each placement.

If step 1 finds no domain that fits, set `unmatched: true` and stop — the
nothing-fits path (the `/route` caller) handles drafting a new node for review.

## Output — routing_result (lightweight; NOT an ADR)

```yaml
routing_result:
  work: "add SMS password reset for locked-out users"
  placements:
    - domain: user-management
      capability: Account Recovery
      functionality: [Password reset, Multi-channel support]
      confidence: high            # high | medium | low
      why: "credential recovery delivered over a non-default channel (SMS)"
      conditions:                 # metadata, copied — NOT evaluated here
        - "Multi-channel support — when shape.surfaces spans more than one, or shape.users: public"
  spans_multiple_domains: false
  unmatched: false
```

Emit it as JSON (the machine form) at `out_route`. It must validate:
`python3 scripts/validate_route.py <out_route>`.

## Rules

- **Placement, not selection.** Never reject a placement because a profile condition
  fails — the asker already decided to build it. Return conditions as metadata only.
- **Reason over the small set.** With ~10 domains, read every trigger and reason; a
  keyword match is a hint, never the decision.
- **Record why.** Every placement carries a one-line rationale.
- **Honest confidence.** `low` when the work is vague or could sit in several places;
  flag `spans_multiple_domains` when it truly does.
