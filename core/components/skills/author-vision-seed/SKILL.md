---
name: author-vision-seed
description: Author or grow the /vision seed of the product model — a detailed domain grounding doc and directional capability grounding docs — straight to the live model, starting from business intents, a typed goal, or both, and from whatever the model already holds; and emit the matching spine-delta (new domain + capability entries, the named updates to existing ones, and the directional profile block) as structured data in the seed manifest. Generative artifact production for the /vision play. Under direct-model-write (ADR 026) it writes ONLY the per-node docs (domain.md, capability.md) in place — new ones, or updates that keep what was there — and NEVER writes _spine.yaml, the profile, or an intent page; the play's keyed persist script applies the spine-delta, moves holding-folder pages, and writes the intent links. Use when /vision needs the directional seed authored or grown.
version: 0.4.0
user-invocable: false
model: opus
allowed-tools: Read, Write, Bash, Glob
---

# author-vision-seed

Turns a business goal plus its KB grounding into the **seed** of the product model. This
is /vision's generative worker: it details the domain, names the capabilities and gives
them directionality, sketches the directional profile, and lays down the spine entries
that wire it together. Under direct-model-write (ADR 026) it writes the per-node grounding
docs straight to the live model and emits the spine-delta as structured manifest data;
/vision's checkpoint and keyed persist script turn that manifest into the spine/profile
writes.

## Altitude — write at CXO level

/vision is the **CXO conversation**: what you take to a CXO and what they give back.
So the grounding here is strategic and outcome-led — the domain and the bet, the big
directional capability areas, what "good" looks like at a strategic level. Detailing a
capability into functionalities is the **product manager's** job (/understand); breaking
it into deliverable verticals is the **product owner's** job (/shape). Write nothing at
those altitudes here.

What that means concretely:
- The **domain** is named AND detailed — a full domain grounding doc a CXO would
  recognize as their product's strategy.
- Each **capability** is named and given **directionality only** — what it is about, the
  rough direction of its scope, and why it matters. No benefit-proof, no boundary
  detail, no functionalities. That is /understand.

## One model, nothing waits (ontology v4, #637)

/intent and /vision write the same tree. Either may run first, and each writes at the depth
it knows. So you start from whatever is there: business intents (proposed is fine — never
check workability, never wait), capabilities another play wrote (under a domain, or in the
holding folder `capabilities/<id>/`), and light domain pages. You build on them; you never
redo them and you never wait for them. Anything missing or odd is a `warnings` line in the
manifest, not a stop.

## Write discipline — direct-model-write containment split (ADR 026)

This skill is the LLM worker in a direct-model-write play. Per
`standards/rules/direct-model-write.md` it obeys the **containment split**, and this is
mandatory:

- It writes ONLY the per-node grounding docs — the `domain.md` and one `capability.md`
  per capability — **straight to the live model** under `{product_base}product-os/`, each
  its own file. There is no `draft/` tree.
- It writes a NEW doc where none exists, and UPDATES an existing doc only to grow it at its
  own altitude, **keeping every section and every agent-intent line it had** (the play's
  keep check fails the run if one is lost): raise a light domain page (`## Intent` only) to
  the full Theme page, keeping its intent; add light directional detail to a capability's
  `## Directional intent` or its `## Agent intent (ICE)` lines. It never removes a doc and
  never moves one — the persist script moves holding-folder pages.
- It **NEVER** writes any shared model file: not `_spine.yaml`, not the profile block, not
  an intent page. The spine/profile changes, the page moves and the intent pages' Touches
  lists are the job of /vision's deterministic keyed persist script, which reads this
  skill's manifest.
- The spine-delta it used to write into a draft `_spine.yaml` — the domain entry, the
  capability entries, and the directional profile block — is now emitted as **structured
  data in `seed-manifest.yaml`** (a non-model STM artifact). The keyed persist script
  merges those entries into the live spine additively (add-only by id; profile only if
  absent).

Because the LLM only ever writes separate doc files, /vision's file-level scoped guard is
sufficient for this skill's blast radius, and node-level containment inside the shared
spine is preserved by the keyed script.

## The grounding contracts (non-negotiable)

Every grounding doc you write conforms to its locked template (`standards/schemas/product-os/grounding/`,
read from `schemas_dir`, the copy your agent put in short-term memory) and clears the content standard
(`_content-standard.md`) — because the play runs the linter (shape) and the
content-quality eval (a judge) over your docs, and a thin doc is rejected:

- `domain.md` → the **Theme** template (full): Intent, Business goal, Guiding rules,
  Capabilities, Scope (In / Out).
- `capability.md` → the capability template, **DIRECTIONAL** stage: a
  `## Directional intent` section, substantive and self-explaining (the *why*), at CXO
  altitude — not the detailed shape, which /understand writes — then, when the capability
  serves a business intent, its `## Agent intent (ICE)` section as the last section: at
  least one `- Goal:` line drawn from the intent, plus `- Limit:` / `- Fails if:` lines only
  where the intent or the KB shows them.

Every item explains itself: name the thing AND say why it matters or what it implies.
Telegraphic labels ("Local fixtures only") fail the eval.

## Inputs

| Field | Required | Description |
|-------|----------|-------------|
| `goal` | no | The business goal, free text (e.g. "order management for a D2C store"). With intents, draw it from their pages instead. One of `goal` or `intents_path` is given. |
| `intents_path` | no | `read_intents.py`'s record: the input intents (title, outcome, why, stage) and the domains and capabilities already linked to them, including those in the holding folder. |
| `grounding_path` | yes | The `search-kb` routing result mapping the goal to a domain + candidate capabilities, each with its KB shelf and `why`. |
| `proposals_dir` | no | Folder of any `propose-kb-node` proposals for parts the KB did not cover. |
| `product_base` | yes | From config (`product.base-path`). The live model root: read the existing spine + docs (to write only what is ABSENT), and WRITE the `domain.md` + `capability.md` docs in place under `{product_base}product-os/`. Only per-node docs — never a shared file. |
| `manifest_path` | yes | Where to write `seed-manifest.yaml` (STM, non-model) — carries the spine-delta as structured data for the keyed persist script. |
| `schemas_dir` | yes | The grounding templates, the content standard and the spine schema (`standards/schemas/product-os/grounding/*`, `standards/schemas/product-os/spine.yaml`), copied into short-term memory by the agent through the memory tool. Read these copies — never memory itself (ADR 039). |
| `stm_base` | yes | From config. |
| `issue` | no | Issue/run id for provenance (often null for /vision). |

## Procedure

Reasoning — detailing the domain, naming capabilities, writing their directional
intent, picking directional profile levels — is yours. Template conformance and the
content bar are non-negotiable.

1. **Read the grounding and the intents.** Take the routed domain and candidate
   capabilities. Each capability must trace to a KB shelf (cited in the routing result) or a
   proposal in `proposals_dir`. A candidate with neither is dropped, not invented — note the
   gap. With `intents_path`, read the intents and the capabilities already linked to them.

2. **Check what already exists, and match against it.** Read `product_base`'s
   `_spine.yaml` (if present) and the live doc tree. For each KB candidate, decide whether
   a capability already in the model — another play's included, in the holding folder too —
   is the same thing. If it is, record `{candidate, same_as: <capability id>}` under
   `same_as` and do not add it again. Never emit a new spine-delta entry for an id already
   in the live spine.

3. **Write or raise the domain grounding doc, in place.** `{domain-slug}/domain.md` to the
   Theme template's **detailed** stage, at CXO altitude — the problem the domain owns and
   the bet behind it, the operating principles/hard rules that define it, the directional
   capabilities (those already there and those you add), and the in/out scope. If the page
   is absent, write it. If it is a light page, raise it: keep its `## Intent` (you may
   extend it) and add the other four sections. If it is already detailed, extend its
   Capabilities list for what you add, keeping every section. This is the detailed artifact
   a CXO validates.

4. **Write each new capability grounding doc, in place; grow existing ones lightly.**
   A new capability: `{domain-slug}/{capability-slug}/capability.md` to the capability
   template's **directional** stage — `## Directional intent` (what it is about, the rough
   direction of its scope, why it matters to the domain), then `## Agent intent (ICE)` when
   it serves an intent. A capability another play wrote: leave its page where it is (the
   persist moves a holding-folder page) and add only light directional detail you can back,
   keeping every line. Never detail a capability, never write a functionality.

5. **Emit the spine-delta into the manifest (never `_spine.yaml`).** In the manifest's
   `spine_delta` block record — as structured data the keyed persist script applies —
   (first-class collections; the kind is the collection, there is no `type` field):
   - for a NEW domain, one **`domains`** entry — `id`, `slug`, `status: proposed`,
     `detail: detailed`, a one-sentence `one_line`, `doc` pointing at its `domain.md`, and
     `intents` = the input intents it serves.
   - a **`capabilities`** entry per NEW capability — `id`, `slug`, `domain` = the domain id
     (the named parent relation), `intents` = the input intents it serves (when started from
     intents), `status: proposed`, `detail: directional`, `one_line`, and `doc` pointing at
     its `capability.md`.
   - **`updates`** for entries already in the spine — only these fields: on a domain
     `detail: detailed` (when you raised a light page), `one_line`, `intents`; on a
     capability `domain` (to place one with an empty domain), `one_line`, `intents`. The
     persist refuses any other field, a lowered detail, or a detailed capability.
   - the **directional `profile`** block — `state: directional`, the `shape` at a rough
     cut (stage / users / monetization / surfaces) and `nfr` levels at a coarse
     directional guess. No firm gates, no `set`/`locked`, no quality vision — that is
     /understand. Omit the profile block if one already exists in the live spine.

   Emit into the delta ONLY entries whose id is absent from the live spine (step 2) — the
   persist script also merges additively, but the manifest should already reflect the
   additive intent.

6. **Write the manifest.** Write `seed-manifest.yaml` to `manifest_path` — the
   `spine_delta` (step 5), `same_as` (step 2), `warnings`, plus the provenance + KB
   grounding for EVERY capability the run adds or updates (another play's included) so the
   play's grounding check and keyed persist are mechanical. Never write `_spine.yaml`, the
   profile, or an intent page yourself.

## Output — live docs + the manifest

Written straight to the live model (no draft tree), skip-if-exists:

```
{product_base}product-os/
  {domain-slug}/
    domain.md                                     # full domain grounding (Theme template), in place
    {capability-slug}/
      capability.md                               # directional capability grounding, in place
```

Plus the manifest (STM, non-model) at `manifest_path`, carrying the spine-delta:

```yaml
seed:
  goal: "order management for a D2C store"
  domain: { id: dom-order-mgmt, name: "Order Management", doc: "product-os/order-management/domain.md" }
  spine_delta:                                     # persist merges this into the live _spine.yaml additively
    domains:
      - { id: dom-order-mgmt, slug: order-management, status: proposed, one_line: "Own the order lifecycle end to end", doc: order-management/domain.md }
    capabilities:
      - { id: cap-checkout, slug: checkout, domain: dom-order-mgmt, intents: [grow-online-sales], status: proposed, detail: directional, one_line: "Turn a cart into a paid order", doc: order-management/checkout/capability.md }
    updates:                                       # named updates to entries already in the spine
      - { kind: capability, id: guest-checkout, domain: dom-order-mgmt }   # placed from the holding folder
    profile:                                       # omitted entirely when a live profile already exists
      state: directional
      shape: { stage: mvp, users: consumers, monetization: transactional, surfaces: [web] }
      nfr: { performance: medium, reliability: high, security: high }
  capabilities:                                    # provenance / KB grounding (stays in STM)
    - id: cap-checkout
      name: "Checkout"
      doc: "product-os/order-management/checkout/capability.md"
      detail: directional
      grounding: { kb_shelf: "ecommerce → Checkout" }   # OR: proposal: "<proposals_dir>/checkout.md"
    - id: guest-checkout                           # another play's capability, placed by this run
      name: "Buy without an account"
      grounding: { kb_shelf: "ecommerce → Checkout" }
  same_as:                                         # KB candidates that already exist — not added again
    - { candidate: "ecommerce → Guest checkout", same_as: guest-checkout }
  warnings: []                                     # anything missing or odd, for alignment
  dropped: []                                      # candidates with no grounding, not written
```

Return the enriched contract with the live doc paths written and the `seed-manifest.yaml`
path — paths, never inline content.

## Rules

- **CXO altitude.** Strategic and directional. No functionalities, no acceptance
  criteria, no delivery sequencing — those belong to /understand and /shape.
- **Domain detailed, capabilities directional.** The domain doc is full; each
  capability doc is the directional stage (one `## Directional intent`).
- **Grounded, not invented.** Every capability written traces to a KB shelf or a
  proposal, recorded in the manifest. A candidate with neither is dropped.
- **Directional only.** Capability entries are `status: proposed`, `detail: directional`;
  the profile is `state: directional`. Never emit `active`, `set`, `locked`, or
  `detail: detailed` here.
- **Self-explaining.** Every grounding item names the thing and explains the why — it
  must clear the content standard, because the eval will judge it.
- **Docs live, shared files never (containment split, ADR 026).** Write the `domain.md`
  and `capability.md` docs straight to the live model. NEVER write `_spine.yaml`, the
  profile block, or an intent page — emit their delta as manifest data.
- **Keep what is there.** A new doc where none exists; an existing doc only grown, never
  losing a section or an agent-intent line; a new spine entry only for an absent id, and
  existing entries only through the named `updates`.
- **Never blocked.** Start from whatever the model holds; a gap is a warning.
- **Template-true.** Every doc conforms to its grounding template; the manifest spine
  entries conform to the spine schema (`standards/schemas/product-os/spine.yaml`).
```
