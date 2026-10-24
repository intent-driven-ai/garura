---
name: enrich-capability-ice
description: Find the capabilities a prototype's screens show (find mode, ADR 043), or detail one capability — already in the model, seeded from the person's recorded answers, or read off the screens — promote its capability.md from the directional stage to the detailed stage (benefit hypothesis, boundary, guiding rules, features), author a detailed feature.md grounding doc for each feature it identifies, set the capability's structured nfr_needs + compliance_needs, and emit the implied per-dimension levels. Grounded in the capability's KB shelf. Generative artifact production for the /discover-capabilities play. Under direct-model-write (ADR 026) it writes ONLY the per-node docs (capability.md, feature.md) straight to the live model, and emits every shared-file delta (the spine entry fields, the new feature entries) as structured data in the enrich-manifest — it NEVER writes _spine.yaml, profile.yaml, or decisions. Also used by /shape-slice (through product-os-keeper) for a capability a slice needs and the model lacks, seeded from the person's answers, with depth set to directional — the page stays at the directional stage, marked to be deepened. A gap it cannot fill is returned as data in the manifest's gaps, never as a question. Use when /discover-capabilities needs a seeded capability detailed and its features created, or /shape-slice needs a new capability, its features and their ICE written.
version: 0.3.0
user-invocable: false
model: opus
allowed-tools: Read, Write, Bash, Glob
---

# enrich-capability-ice

Takes a capability — one already in the model, one the person named, or one this skill
reads off a prototype's screens (ADR 043) — and **details it**: it deepens the capability's grounding from the directional stage to the
detailed stage, **identifies and authors its features**, and sets the capability's
own NFR needs. This is /discover-capabilities's generative worker — the **product-manager** step,
where the product is understood in full down to the feature. Under direct-model-write
(ADR 026) it writes the per-node docs straight to the live model and emits the shared-file
delta as structured manifest data; /discover-capabilities's checkpoint, roll-up, and keyed persist
script turn that manifest into the spine/profile/decision writes.

## Altitude — write at product-manager level

/discover-domains was the CXO conversation (directional). /discover-capabilities is the **product manager**
detailing the product. So the writing here is concrete and complete — the full capability
and its features, the detail a build needs — but still product language, not code.
Sequencing the work into deliverable verticals is the **product owner's** job (/shape-scope); do
none of that here.

## Write discipline — direct-model-write containment split (ADR 026)

This skill is the LLM worker in a direct-model-write play. Per
`standards/rules/direct-model-write.md` it obeys the **containment split**, and this is
mandatory:

- It writes ONLY the per-node grounding docs — the target's `capability.md` and one
  `feature.md` per feature — **straight to the live model** under
  `{product_base}product-os/`, each its own file. There is no `draft/` tree.
- It **NEVER** writes any shared model file: not `_spine.yaml`, not `profile.yaml`, not
  `decisions/`. The spine/profile/decision mutations are the job of /discover-capabilities's
  deterministic keyed persist script, which reads this skill's manifest.
- The spine-delta it used to write into a draft `_spine.yaml` — the target capability's
  `detail`/`nfr_needs`/`compliance_needs` and the new `features` entries — is now
  emitted as **structured data in `enrich-manifest.yaml`** (a non-model STM artifact). The
  keyed persist script applies those fields to the live spine in place, node-keyed.

Because the LLM only ever writes separate doc files, /discover-capabilities's file-level scoped guard
is sufficient for this skill's blast radius, and node-level containment inside the shared
spine/profile is preserved by the keyed script.

## What it produces (against the locked contracts)

Everything conforms to its template (`standards/schemas/product-os/grounding/`, read from
`schemas_dir`) and must clear the content-quality eval (the play runs the linter + the judge over the docs):

- the **detailed** `capability.md` — the capability template's DETAILED stage: Benefit
  hypothesis, Boundary (In / Out / Never), Guiding rules, Features (each a one-line
  index entry linked to a feature id it creates). Written in place over the live
  directional `capability.md`.
- one **`feature.md`** per feature it identifies — the feature template:
  What it does, Inputs / Outputs, Rules & behavior, Acceptance criteria, Out of scope.
  Written as a new file in the live model.
- the **enrich-manifest** (STM, non-model) carrying the **spine-delta as structured data**:
  the target capability entry fields (`detail: detailed`, structured `nfr_needs` +
  `compliance_needs`, its `doc` pointer), the new `features` entries (id, slug,
  `capability` ref, status proposed, one_line, doc pointer), the roll-up input (per-dimension
  implied levels + compliance), and the KB shelf grounding used. NO `_spine.yaml` is written.

## Input

| Field | Required | Description |
|-------|----------|-------------|
| `mode` | no | `find` to list the capabilities a capture's screens show (Find mode, below); absent to detail one capability. |
| `out_found` | for `find` | Where to write `found.yaml`. |
| `capability` | yes, to detail | The target capability: its id, slug, and the path to its directional `capability.md` in the live model — **or**, for a capability /discover-capabilities is seeding, the path to `<working>/seed.yaml` with the person's recorded answers (`one_line`, `why`, `domain`, `doc`, `answered_by: human`) — or, for /shape-slice, the capability's entry in the caller's `fills.json` (the path of the file and the id), with the question record as the person's answers. |
| `kb_domain` | yes | The domain the capability belongs to. |
| `shelf_path` | yes | That domain's shelf (`knowledge/domains/<kb_domain>.md`), copied into short-term memory by the agent through the memory tool. Read this copy — never memory itself (ADR 039). |
| `schemas_dir` | yes | The grounding templates, the content standard and the spine schema, copied into short-term memory the same way. |
| `capture` | no | A prototype's shared capture (#689): its source manifest (the views kept, each with its text and picture), its journeys, and the folder of view texts. With it, the features come from what the screens let a person do and see, and every page names where it is seen. |
| `product_base` | yes | From config. The live model root: read the existing spine + the capability's current directional doc, and WRITE the detailed `capability.md` and the new `feature.md` docs in place under `{product_base}product-os/`. Only the target node's docs — never a shared file, never a sibling node's doc. |
| `manifest_path` | yes | Where to write `enrich-manifest.yaml` (STM, non-model) — carries the spine-delta as structured data for the keyed persist script. |
| `stm_base` | yes | From config. |
| `depth` | no | `detailed` (the default) or `directional`. With `directional` (/shape-slice), the capability's page stays at the directional stage and is marked to be deepened: the manifest's `capability.detail` is `directional` and `capability.deepen` is `true`, and the page says it is to be deepened with `/discover-capabilities`. Its features get pages at the depth the person's answers give. |
| `features` | with `depth: directional` | The features the caller already chose for this capability (their ids, slugs and doc paths, from the caller's needs list). Write a page for each of these, and identify no other feature. |

## Find mode — the capabilities a prototype's screens show (ADR 043)

Called with `mode: find`, a `capture` and an `out_found` path (and no `capability`), the
skill writes no model file. It reads every view of the capture (its text and picture) and
the journeys, and lists each capability the product offers its user: one per thing a person
can do or see there, named in the product's words — never one panel or label of a screen,
never the sample data, never something no screen shows. It reads the spine and lists a
capability already in the model under its own id (it is detailed, not added twice). For each
it writes, to `out_found`:

```yaml
found:
  - id: <short-slug>
    one_line: <one sentence: what this capability is>
    why: <why the product needs it, from the screens and the write-up>
    domain: <a domain id from the spine when one clearly holds it, else "">
    intents: [<business intent ids in the model it serves, else empty>]
    screens: ["<screen>: \"<the exact words there>\"", ...]
```

A capability with no domain known is fine: it waits in the holding folder, not ready until
it is attributed. The play then details each one, one dispatch per capability.

## Process

Reasoning — detailing the capability, identifying its features, writing each
function's behavior and acceptance criteria, judging the NFR levels — is yours. Template
conformance and the content bar are non-negotiable.

1. **Read the directional capability + the shelf.** Read the anchor: the live directional
   `capability.md` (its directional intent), or — when `capability` is a `seed.yaml` — the
   answers it carries, verbatim: the person's (`answered_by: human`) or the screens'
   (`answered_by: screens`, with the screens it is seen on). Then read the capability's KB shelf at `shelf_path` and pull its personas, systems, NFR hints, scope, and
   feature baseline. Ground the detail in that material; for a seed, add nothing to
   the person's answers that the shelf does not support.

   With `depth: directional`, steps 2 and 3 write at the directional stage: the capability's
   page holds its intent, its one line, why it is needed, its Features index and its agent
   intent, from the person's answers and the shelf, and says just under its title "To be
   deepened with `/discover-capabilities`." Step 3 writes a page only for each feature in
   `features`, at its doc path, and holds what the answers give; nothing is stretched past
   them.

2. **Write the detailed capability doc, in place.** Promote the live `capability.md` to the
   detailed stage — overwrite it under `{product_base}product-os/`. For a seeded capability
   there is no directional doc yet: write the FIRST `capability.md`, at the detailed stage,
   at the seed's `doc` path (for a capability read off the screens with no domain, the holding
   folder `capabilities/<id>/capability.md`), and set `capability.doc` in the manifest to that path: the benefit hypothesis
   (who it serves, the believed value, the proof), the boundary (In / Out / Never, each line
   explained), the guiding rules (each with its reason), and the Features index — one
   explained line per feature, linked to the id you assign it in step 3.

3. **Identify and author the features, in place.** Break the capability into its
   features — the functions it must perform. **From a prototype capture, the screens
   decide them:** a feature is something a person does or sees there — an action, a view
   with its states, a rule the screen enforces — named in the words its users would use. One
   panel, count or label of a screen is a part of the feature that shows it (its What it
   does, Inputs / Outputs or Rules), never a feature of its own. Nothing the screens do
   not show and the shelf does not hold becomes a feature. For each, author a detailed
   `feature.md` (what it does, inputs/outputs, rules & behavior with edge cases,
   acceptance criteria as Given/When/Then, out of scope, then `## Sources`: each screen it is
   seen on and the exact words a person reads there, in double quotes) as a NEW file in the
   live model,
   and record a spine `features` entry in the manifest (id, slug, `capability` = the
   target id, status proposed, one_line, doc pointer) — you write the entry to the MANIFEST,
   never to `_spine.yaml`. Detail increases here — a feature reads richer than its
   capability, never leaner.

4. **Set the capability's NFR needs (into the manifest).** In the manifest's `capability`
   block, record `nfr_needs`: for each dimension this capability actually constrains, a
   `level` (none<low<medium<high<xhigh), a concrete measurable `target`, and a `gate` (how it
   is checked — e.g. "p99 < 150ms, load test"). List `compliance_needs` (regimes this
   capability triggers). Per capability — one capability's uptime need can differ from
   another's. A vague adjective ("fast", "secure") is not acceptable. These are manifest
   fields the keyed persist script writes to the live spine entry; you never write them to
   `_spine.yaml` yourself.

5. **Emit the roll-up input.** In the manifest, record the capability's per-dimension
   implied levels + compliance (the input the roll-up script maxes against the box) and the
   KB shelf material used. The level call is this skill's judgment; the threshold math is
   the roll-up script's.

6. **Write the docs + manifest.** Write the detailed `capability.md` and the new
   `feature.md` docs in place under `{product_base}product-os/`, and write
   `enrich-manifest.yaml` to `manifest_path`. Never write `_spine.yaml`, `profile.yaml`, or
   any decision — those are the keyed persist script's, applied from the manifest.

## Output

Live docs and the manifest. Written straight to the live model (no draft tree):

```
{product_base}product-os/
  {domain}/{capability}/
    capability.md                                 # DETAILED — overwrites the directional one, in place
    {feature}/
      feature.md                            # new, one per feature
```

Plus the manifest (STM, non-model) at `manifest_path`:

```yaml
enrich:
  capability_ref: cap-checkout
  grounded_in: "ecommerce -> Checkout"            # the shelf material used
  capability:                                     # spine-delta for the target entry — persist applies it to _spine.yaml
    detail: detailed
    doc: ecommerce/checkout/capability.md         # relative to product-os/
    nfr_needs:
      performance: { level: high, target: "p99 < 150ms", gate: "load test" }
      reliability:  { level: high, target: "99.9% uptime", gate: "uptime SLO monitor" }
    compliance_needs: [PCI-DSS]
  features:                                # NEW spine entries — persist adds them to _spine.yaml
    - { id: func-guest-checkout, slug: guest-checkout, capability: cap-checkout, status: proposed, one_line: "Buy without an account", doc: ecommerce/checkout/func-guest-checkout/feature.md }
    - { id: func-address-validation, slug: address-validation, capability: cap-checkout, status: proposed, one_line: "Validate shipping addresses", doc: ecommerce/checkout/func-address-validation/feature.md }
  implied_levels:                                 # roll-up input (== the nfr_needs levels)
    performance: { level: high, gate: "load test" }
    reliability: { level: high, gate: "uptime SLO monitor" }
  compliance: [PCI-DSS]
  gaps:                                           # what no answer, screen or shelf gives — data, never a question
    - { about: cap-checkout, missing: "who may refund an order", why: "the Rules section cannot be written without it" }
```

Return the enriched contract with the live doc paths written and the `enrich-manifest.yaml`
path — paths, never inline content.

## Rules

- **Every page says where it is seen (#689).** The detailed `capability.md` and each
  `feature.md` carry `## Sources` before their agent intent: each screen with its words
  in double quotes, and the shelf on its own line (`- Shelf: …`).
- **Fill what the screen does not show; never leave it open.** A behaviour the prototype does
  not show (what happens after an error, how long something is kept) is written as our
  default and marked as ours ("our default — the prototype does not show this"). It is never
  "recorded as an open question". Only a business rule an agent intent cannot be written
  without, and that nothing shows or holds, is returned as data in the manifest's `gaps`
  (`{about, missing, why}`); the calling play's question skill writes the question.

- **Product-manager altitude.** Detail the capability and its features fully — no
  delivery sequencing, no slices, no epics (that is /shape-scope).
- **Promote, don't reseed.** The capability doc moves directional → detailed; the manifest's
  `capability.detail` is `detailed`. Never leave it directional, unless the caller gives
  `depth: directional`: then the page stays directional, `capability.detail` is
  `directional` and `capability.deepen` is `true`, so the page and the spine agree. A capability seeded from the
  person's answers gets its first doc directly at the detailed stage — the seed's answers are
  its anchor, never stretched past what the person said and the shelf supports.
- **Features created here.** Every feature gets a manifest spine entry AND a
  detailed `feature.md`; the capability's Features index links each by id.
- **NFR is per-capability.** Record this capability's own `nfr_needs` (level + target + gate
  per dimension) and `compliance_needs` in the manifest; they roll up into the product
  profile downstream.
- **Concrete needs.** Every NFR need is a measurable value with a gate, never a vague
  adjective.
- **Grounded.** Detail draws on the capability's KB shelf; record which shelf material was
  used in the manifest.
- **Self-explaining.** Every grounding item names the thing and explains the why — it must
  clear the content standard, because the eval will judge it.
- **Docs live, shared files never (containment split, ADR 026).** Write the target's
  `capability.md` and its new `feature.md` docs straight to the live model. NEVER
  write `_spine.yaml`, `profile.yaml`, or a decision — emit their delta as manifest data.
  Never touch another capability's docs or entries — only the target and its features.
- **Template-true.** Every doc conforms to its grounding template; the manifest spine entries
  conform to the spine schema (`standards/schemas/product-os/spine.yaml`).
```
