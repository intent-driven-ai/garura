---
name: propose-kb-node
description: The nothing-fits path for find-work-placement. When find-work-placement returns unmatched (a piece of work has no home in the knowledge base), research the gap, draft a properly-shaped node at the right level (new domain, capability, or feature) following the shelf template and feature baseline, and emit a proposal for human review. NEVER writes to memory — its agent raises the proposal as a memory update a person approves (ADR 036, ADR 039). Use when find-work-placement reports unmatched, or when a play hits work the model does not yet cover.
version: 0.1.0
user-invocable: false
model: sonnet
allowed-tools: Bash, Read, WebSearch, WebFetch
---

# propose-kb-node

The escalation behind `find-work-placement`. Runs when routing comes back **unmatched** — the
work has no home in the KB. It proposes a new node for the user to review. It does
**not** change the KB.

## Inputs

- `work` — the piece of work that did not route.
- `domains_dir` — the domain shelves, copied into short-term memory by the agent through the
  memory tool. Read only these copies — never memory itself (ADR 039).
- `out_proposal` — where to write the proposal.
- (optional) the weak hints `find-work-placement` returned (nearest domains/capabilities).

## Procedure

1. **Confirm the gap.** Read the domain shelves in `domains_dir` (their front matter and
   `## Capabilities`) and reason: does the work
   truly fit nowhere, or is it a missing **feature** under an existing
   capability, a missing **capability** under an existing domain, or a missing whole
   **domain**? Pick the *smallest* level that closes the gap — prefer adding a
   feature/capability to an existing shelf over inventing a domain.

2. **Research.** Use WebSearch/WebFetch to ground the draft in real practice — the
   genuine capabilities/features and vocabulary of that area. Capture 2–4
   sources. Do not invent from thin air.
   **A new domain is one the world already recognises.** Name it as the industry or a known
   product category names it in your sources (for example "requirements management" or
   "customer support"), never with a name made from the product's own screens, its sample
   data, or the words of the work you were handed. If no source names such a domain, place
   the work under the nearest recognised one and say why. A domain is a field the industry identifies itself with — a product category or market that vendors, analysts and buyers name (for example application lifecycle management, customer relationship management, e-commerce). A principle, a practice, a regulation or a quality (human oversight, accessibility, compliance) is never a domain: it is a rule or a need inside one.

3. **Draft to the template.** Write the node in the locked shelf shape:
   - new **feature**: `name — what it is`, a maturity ladder OR flat list, and
     a decisive profile condition (`shape.*`/`nfr.*`/`compliance`, or "the floor").
   - new **capability**: the capability + its features (same baseline).
   - new **domain**: a full shelf — stance, "Intents this domain captures", and
     `## Capabilities` with features — matching the existing shelves and the
     feature baseline.

4. **Emit a proposal** (shape below) at `out_proposal` and **STOP.** Your agent raises it
   as a memory update (`propose`, `draft_source: web`) in the issue's short-term memory. It
   is used only after a person approves it; moving it up into memory is a promotion a person
   makes (ADR 036, ADR 039). Until then nothing is written to memory.

## Output — kb_proposal

```yaml
kb_proposal:
  work: "let users file support tickets and live-chat with an agent"
  gap: "no existing domain covers customer support / helpdesk; nearest (notifications,
        collaboration) only touch messaging, not ticketing or agent workflows"
  level: new-domain            # new-domain | new-capability | new-feature
  parent: null                 # null for new-domain; else <domain> or <domain>.<capability>
  proposed:
    name: support
    title: "Support: how we build it"
    trigger: "the product handles inbound user issues — tickets, live chat, help center"
    draft: |
      <markdown of the proposed node, in the shelf shape — abbreviated is fine>
  sources:
    - "<url or note from research>"
  status: "PROPOSED — awaiting user review; NOT written to the KB"
```

Emit it as JSON. It must validate: `python3 scripts/validate_proposal.py <out_proposal>`.

## Rules

- **Never write to memory.** The proposal goes to your agent, which raises it as a memory
  update a person approves.
- **Smallest level that fits.** Don't invent a domain when a capability or
  feature on an existing shelf closes the gap.
- **A recognised domain, never a made-up one.** A new domain's name comes from the research
  sources, which the domain page then lists under `## Sources`.
- **Ground in research.** Cite sources; follow the shelf template + feature
  baseline so an approved proposal drops in cleanly.
- **State the gap plainly** — why the existing model didn't cover it.
