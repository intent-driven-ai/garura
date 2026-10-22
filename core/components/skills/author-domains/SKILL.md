---
name: author-domains
description: Author or grow the domains of the product model for /discover-domains — a detailed domain grounding doc for each domain the product sits in (the field it serves and the job it does there), each ending with its sources — straight to the live model, starting from business intents, a typed goal, a prototype's capture, or any mix, and from whatever the model already holds; and emit the matching spine-delta (new domain entries, the named updates to existing ones, and the directional profile) as structured manifest data. Writes domains only (ADR 043) — never a capability or a feature, which are /discover-capabilities's. Writes per-node docs only; never a shared file. Generative artifact production for the /discover-domains play.
version: 0.6.0
user-invocable: false
model: opus
allowed-tools: Read, Write, Bash, Glob
---

# author-domains

Turns a business goal, intents or a prototype's capture, plus their KB grounding, into the
**domains** of the product model. This is /discover-domains's generative worker: it details each
domain, sketches the directional profile, and lays down the domain spine entries. Under
direct-model-write (ADR 026) it writes the domain grounding docs straight to the live model
and emits the spine-delta as structured manifest data; /discover-domains's checkpoint and keyed persist
script turn that manifest into the spine/profile writes.

## Altitude — write at CXO level

/discover-domains is the **CXO conversation**: what you take to a CXO and what they give back. So the
grounding here is strategic and outcome-led — the domain and the bet, the kinds of capability
it covers, what "good" looks like at a strategic level. Writing and detailing the
capabilities and their features is the **product manager's** job (/discover-capabilities);
breaking them into deliverable verticals is the **product owner's** job (/shape-scope). Write
nothing at those altitudes here.

Each **domain** is named AND detailed — a full domain grounding doc a CXO would recognise as
their product's strategy. A product often sits in more than one domain: the field it serves
(judged by what its screens or its words are about) and the job it does in that field. Write
one page for each.

## Every kind written on its own (ADR 043)

Each kind has one writer: /discover-intent writes business intents, you write domains, /discover-capabilities
writes capabilities and features. None waits for another, and the links between them
are made later. So you start from whatever is there: business intents (proposed is fine —
never check workability, never wait), light domain pages, and any capability already in the
model, which you read as context only — you never write, place, move or detail one. Anything
missing or odd is a `warnings` line in the manifest, not a stop.

## Write discipline — direct-model-write containment split (ADR 026)

This skill is the LLM worker in a direct-model-write play. Per
`standards/rules/direct-model-write.md` it obeys the **containment split**, and this is
mandatory:

- It writes ONLY domain grounding docs — one `domain.md` per domain — **straight to the live
  model** under `{product_base}product-os/`, each its own file. There is no `draft/` tree. It
  writes no capability or feature page.
- It writes a NEW doc where none exists, and UPDATES an existing domain doc only to grow it
  at its own altitude, **keeping every section it had** (the play's keep check fails the run
  if one is lost): raise a light domain page (`## Intent` only) to the full Theme page,
  keeping its intent. It never removes or moves a doc.
- It **NEVER** writes any shared model file: not `_spine.yaml`, not the profile block, not an
  intent page. The spine/profile changes and the intent pages' Touches lists are the job of
  /discover-domains's deterministic keyed persist script, which reads this skill's manifest.
- The spine-delta — the domain entries and the directional profile block — is emitted as
  **structured data in `seed-manifest.yaml`** (a non-model STM artifact). The keyed persist
  script merges those entries into the live spine additively (add-only by id; profile only if
  absent) and refuses any capability or feature entry.

## The grounding contract (non-negotiable)

Every domain doc you write conforms to its locked template (`standards/schemas/product-os/grounding/domain.md`,
read from `schemas_dir`, the copy your agent put in short-term memory) and clears the content
standard (`_content-standard.md`) — because the play runs the linter (shape) and the
content-quality eval (a judge) over your docs, and a thin doc is rejected:

- `domain.md` → the **Theme** template (full): Intent, Business goal, Guiding rules,
  Capabilities, Scope (In / Out), then `## Sources`. The Capabilities section describes, in
  plain words, the kinds of capability the domain covers and why each is distinct — drawn
  from the shelf or the research; it names no capability entry and writes no capability page.

Every item explains itself: name the thing AND say why it matters or what it implies.
Telegraphic labels ("Local fixtures only") fail the eval.

## Inputs

| Field | Required | Description |
|-------|----------|-------------|
| `goal` | no | The business goal, free text (e.g. "order management for a D2C store"). With intents, draw it from their pages instead. |
| `capture` | no | A prototype's shared capture (#689): its source manifest (the views kept, each with its text) and its journeys. With it, the domains are read from the screens themselves — the field they are about and the job the product does there — no intents needed. |
| `intents_path` | no | `read_intents.py`'s record: the input intents (title, outcome, why, stage) and the domains and capabilities already linked to them. |
| `grounding_path` | yes | The `find-work-placement` routing result: each domain the product sits in, with its KB shelf or its proposal, and `why`; with a capture, each main section with its domain, `evidence` and `source`. |
| `proposals_dir` | no | Folder of any `propose-kb-node` proposals for domains the KB did not cover. |
| `product_base` | yes | From config (`product.base-path`). The live model root: read the existing spine + docs (to write only what is ABSENT), and WRITE the `domain.md` docs in place under `{product_base}product-os/`. Only domain docs — never a shared file. |
| `manifest_path` | yes | Where to write `seed-manifest.yaml` (STM, non-model) — carries the spine-delta as structured data for the keyed persist script. |
| `schemas_dir` | yes | The grounding templates, the content standard and the spine schema, copied into short-term memory by the agent through the memory tool. Read these copies — never memory itself (ADR 039). |
| `stm_base` | yes | From config. |
| `issue` | no | Issue/run id for provenance (often null for /discover-domains). |

## Procedure

Reasoning — detailing each domain, describing what it covers, picking directional profile
levels — is yours. Template conformance and the content bar are non-negotiable.

1. **Read the grounding and the intents.** Take the routed domains. Each must trace to a KB
   shelf (cited in the routing result) or a proposal in `proposals_dir` that names it from
   research. A domain with neither is dropped, not invented — note the gap. With
   `intents_path`, read the intents and what is already linked to them. With a capture, check
   that every main section (`main_sections` in its journeys) sits in a domain whose shelf or
   research covers that kind of work; a main section left over means a field not yet found —
   hand it back for research, never stretch a found field over it. A domain that holds no main
   section is dropped.

2. **Check what already exists.** Read `product_base`'s `_spine.yaml` (if present) and the
   live doc tree. A routed domain already in the model is grown, not added again. Never emit
   a new spine-delta entry for an id already in the live spine.

3. **Write or raise each domain's grounding doc, in place.** `{domain-slug}/domain.md` to the
   Theme template's **detailed** stage, at CXO altitude — the problem the domain owns and the
   bet behind it, the operating principles/hard rules that define it, the kinds of capability
   it covers (in plain words), and the in/out scope. If the page is absent, write it. If it is
   a light page, raise it: keep its `## Intent` (you may extend it) and add the other
   sections. End it with `## Sources`: the shelf it matched, or, for a new domain, the
   research links the proposal cites — the links that show the world recognises this domain
   by this name. If it is already detailed, extend it, keeping every section.

4. **Emit the spine-delta into the manifest (never `_spine.yaml`).** In the manifest's
   `spine_delta` block record, as structured data the keyed persist script applies:
   - for a NEW domain, one **`domains`** entry — `id`, `slug`, `status: proposed`,
     `detail: detailed`, a one-sentence `one_line`, `doc` pointing at its `domain.md`, and
     `intents` = the input intents it serves.
   - **`updates`** for domain entries already in the spine — only these fields:
     `detail: detailed` (when you raised a light page), `one_line`, `intents`. The persist
     refuses any other field, a lowered detail, and any capability or feature entry
     or update.
   - the **directional `profile`** block — `state: directional`, the `shape` at a rough cut
     (stage / users / monetization / surfaces) and `nfr` levels at a coarse directional guess.
     No firm gates, no `set`/`locked`. Omit the profile block if one already exists in the
     live spine.

5. **Write the manifest.** Write `seed-manifest.yaml` to `manifest_path` — the `spine_delta`,
   `warnings`, plus the provenance + KB grounding for EVERY domain the run adds or updates, and,
   with a capture, the `areas` — each main section with its domain, the line from that domain's
   shelf or research that covers its work (`evidence`) and where it is from (`source`) — so
   the play's grounding check and keyed persist are mechanical. Never write `_spine.yaml`,
   the profile, or an intent page yourself.

## Output — live docs + the manifest

Written straight to the live model (no draft tree):

```
{product_base}product-os/
  {domain-slug}/
    domain.md                                     # full domain grounding (Theme template), in place
```

Plus the manifest (STM, non-model) at `manifest_path`, carrying the spine-delta:

```yaml
seed:
  goal: "a tool where a team lead plans a software team's work"
  domains:                                         # provenance / KB grounding (stays in STM)
    - id: software-delivery
      name: "Software delivery"
      doc: "product-os/software-delivery/domain.md"
      grounding: { proposal: "<proposals_dir>/software-delivery.json" }   # OR: kb_shelf: "<shelf>"
    - id: work-management
      name: "Work management"
      doc: "product-os/work-management/domain.md"
      grounding: { kb_shelf: "collaboration" }
  areas:                                           # with a capture: every main section, in a domain whose research covers it
    - { section: "Board", domain: work-management, evidence: "work management tools let teams plan and track tasks on boards", source: "kb_shelf: collaboration" }
    - { section: "Releases", domain: software-delivery, evidence: "release management plans and ships software versions", source: "https://example.org/release-management" }
  spine_delta:                                     # persist merges this into the live _spine.yaml additively
    domains:
      - { id: software-delivery, slug: software-delivery, status: proposed, detail: detailed, one_line: "Build and ship software as a team", doc: software-delivery/domain.md, intents: [plan-the-week] }
    updates:                                       # named updates to domain entries already in the spine
      - { kind: domain, id: work-management, detail: detailed, intents: [plan-the-week] }
    profile:                                       # omitted entirely when a live profile already exists
      state: directional
      shape: { stage: mvp, users: teams, monetization: subscription, surfaces: [web] }
      nfr: { performance: medium, reliability: high, security: high }
  warnings: []                                     # anything missing or odd
  dropped: []                                      # domains with no grounding, not written
```

Return the enriched contract with the live doc paths written and the `seed-manifest.yaml`
path — paths, never inline content.

## Rules

- **Domains only (ADR 043).** Write domain pages and domain entries. Never write, name as an
  entry, place, move or detail a capability; never write a feature.
- **Every page says where it comes from (#689).** Each domain page ends with `## Sources`
  (its shelf, or its research links).
- **A recognised domain, never a made-up one.** A domain is named as the industry or a known
  product category names it — never from the product's own screens, its sample data or the
  words of the work. A domain is a field the industry identifies itself with — a product category or market that vendors, analysts and buyers name (for example application lifecycle management, customer relationship management, e-commerce). A principle, a practice, a regulation or a quality (human oversight, accessibility, compliance) is never a domain: it is a rule or a need inside one. Nor is the field of one feature many products share (comments, notifications, search, sign-in).
- **Every main section in a field that covers it.** With a capture, each main section sits in
  a domain whose own shelf or research lists that kind of work (`areas`); a domain that holds no
  main section is not written.
- **CXO altitude.** Strategic and directional. No acceptance criteria, no delivery sequencing.
- **Directional profile.** The profile is `state: directional`. Never emit `active`, `set` or
  `locked`.
- **Self-explaining.** Every grounding item names the thing and explains the why — it must
  clear the content standard, because the eval will judge it.
- **Docs live, shared files never (containment split, ADR 026).** Write the `domain.md` docs
  straight to the live model. NEVER write `_spine.yaml`, the profile block, or an intent page
  — emit their delta as manifest data.
- **Keep what is there.** A new doc where none exists; an existing doc only grown, never
  losing a section; a new spine entry only for an absent id, and existing entries only
  through the named `updates`.
- **Never blocked.** Start from whatever the model holds; a gap is a warning.
- **Template-true.** Every doc conforms to its grounding template; the manifest spine entries
  conform to the spine schema (`standards/schemas/product-os/spine.yaml`).
