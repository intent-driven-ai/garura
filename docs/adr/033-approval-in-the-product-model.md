# ADR 033 — Approval Is Part of the Product Model, and Agents Work Only on Approved Pieces

**Status:** Accepted
**Date:** 2026-10-18
**Level:** framework
**Decided by:** Kapil Viren Ahuja
**Decided in:** #617 (spike: decide how a finished drive is reviewed), on branch `feature/617-decide-how-a-finished-drive-is-reviewed`; working notes in `.garura/project/issues/617/specs/review-tool.md` ("Approval is part of the product model") and the #617 plan log
**Amends:** ADR 032 — §5 "The answers are applied as one commit": "statuses are set" becomes a lasting approval written on each piece, kept after the drive; with it §2 and §3, what the review tools show: the whole model's approval state every time they open, a drive's end review being that view narrowed to what the drive changed; and §4's send back leaves the piece in progress until its new version is answered · ADR 031 — §4 "ICE is worked on only when its intent is confirmed": an ICE is workable only when the ICE itself, the capability or functionality it sits on, and its business intent are all approved
**Affects:** `core/components/memory/standards/schemas/product-os/ontology.md` (Business Intent, Rules: "Work starts only from an ICE built from a confirmed business intent", widened to every piece; the ICE rule on when it is workable; one approval lifecycle on every kind — built under #597), `core/components/memory/standards/schemas/product-os/spine.yaml` (the `status` of domains, capabilities and functionalities: `active` is approved; the `/shape` fill rule that sets capabilities active), `core/components/memory/standards/schemas/product-os/decision.yaml` (`accepted` is approved), `core/components/memory/standards/schemas/product-os/product-profile.yaml` (the product limits carry an approval state), `core/components/memory/standards/schemas/product-os/grounding/` (where a page shows its state), `core/components/plays/intent/scripts/check_ice_workable.py` and its copy in `core/components/plays/play-creator/references/` (check approval, not only a confirmed intent), `core/components/memory/standards/rules/direct-model-write.md` (the `/intent` and `/adr` by-hand exceptions), `core/components/memory/standards/rules/drive-contract.md` (the end review writes approval), `docs/philosophy/idsd.md` ("The Plan Is the Human's Interface; the Product Model Is the Agent's"), `.garura/project/issues/617/specs/review-tool.md` (the overview counts; story 5a), the `/intent`, `/vision`, `/understand`, `/shape` and `/adr` plays, the Kickoff drive (#613, not built yet), and the review step and the two review tools (not built yet)
**ICE impact:** Every agent intent's workability changes. Today an ICE is workable when its node names at least one confirmed business intent. After this ADR an agent takes an ICE only when the ICE itself is approved, the capability or functionality it sits on is approved, and the business intent it is built from is approved (confirmed). A play that rewrites an approved ICE or node moves it to changed, and no agent builds from it until a person approves it again. Every play that checks workability (`check_ice_workable.py`) reads the approval state. The ICE kind keeps its shape; it gains the approval state every piece carries.
**Business intent check:** kind — the Business Intent kind's rules change (its `confirmed` stage is mapped to approved, it gains the approval fingerprint, and the rule on where work starts is widened); no person's business intent changes, and only a person still confirms or drops one
**Related:** ADR 032 (drive review of outcomes), ADR 031 (business intent and ICE), ADR 026 (direct model writes), ADR 029 (drives), #597 (the product ontology), #613 (Kickoff), #617, #637

## Context

ADR 032 settled how a person reviews what one drive changed. Its review sets statuses for that drive. Nothing it writes lasts after it.

But the product model keeps changing after a review. Any play may write any kind, by hand or inside a drive (ADR 031 §2). A piece a person approved last week can be changed by a command today. Nothing tells an agent which pieces a person has agreed to. So an agent would still build from a piece no person has seen.

Today's rule covers only one link: "Work starts only from an ICE built from a confirmed business intent" (`ontology.md`, Business Intent, Rules). A capability, a functionality or an ICE changed after its intent was confirmed would still be built from.

Kapil, 2026-10-18: "as you set and change a business intent, an [ICE], or the product model, this tool needs to keep good track of what is approved and what needs to be changed." And: "that whole review and approval thing is part of the product model itself. It's not outside of it. Every time somebody opens up this tool, they should be able to see what is changed, what is approved, and what is in progress. It's just critical because agents can only work on things which are approved. Agents cannot work on things which are non-approved. Commands can impact it, but that lifecycle is very critical to the governance of the product model and what is being built."

The Kickoff drive (#613) is built next. It makes the first pieces that need approval, so the rule must exist before it is built.

## Decision

### 1. Approval lives in the product model

Approval is part of the product model itself, not a record kept beside it. Every piece of the model carries its own approval state:

- each business intent;
- each agent intent (ICE);
- each domain, capability and functionality;
- the product limits;
- each decision.

### 2. Three states the person sees

- **Approved** — a person accepted these exact words. The piece keeps a fingerprint of its words (a short code worked out from the text), who approved it, when, and in which review.
- **Changed** — the piece is new, or its words no longer match the fingerprint it was approved with. It waits for a person.
- **In progress** — a person sent it back, and it is being reworked. The comments stay open until the new version comes back and is answered.

A dropped piece leaves the model. Git and the review keep the record of the drop.

### 3. Agents work only on approved pieces

This is the governance rule of the product model.

Commands — plays, inside a drive or run by hand — may still write any piece, an approved one included. The write moves that piece to **changed**, by its fingerprint. No play has to remember to say so. No agent builds from that piece until a person approves it again.

A rule stops work, never a write (ontology, "Who writes, and what the rules mean").

### 4. Approval follows links

An ICE built from a business intent that is not approved is not approved either. A functionality inside a capability that is not approved waits with it.

### 5. One lifecycle, mapped onto the states that exist

- An approved business intent is `confirmed`.
- An approved decision is `accepted`.
- An approved capability or functionality is `active`.

The ontology names one approval lifecycle for every kind and maps these onto it. So a page and its approval state never disagree.

### 6. Only the review step writes approval

The review step writes **approved** or **in progress**, from the person's answers. Plays write the model. The review tool writes nothing to the model.

### 7. The review tool shows it every time it opens

Not only at the end of a drive. It shows the whole model's counts — approved, changed, in progress — and each piece's state. "Only changed" means "everything not approved". A drive's end review (ADR 032) is that same view, narrowed to what the drive changed.

### 8. What this widens and amends

- **The ontology rule** "Work starts only from an ICE built from a confirmed business intent" widens from business intents to every piece. This ADR decides it; the ontology change itself (the lifecycle on each kind) is built under the ontology work (#597).
- **ADR 032** — its review set statuses for one drive and kept nothing that lasts. Now the review step writes a lasting approval on each piece (§5); the tools show the whole model's approval state each time they open (§2, §3); a send-back leaves the piece in progress (§4). The rest of ADR 032 stands.
- **ADR 031 §4** — an ICE is workable only when the ICE, its node and its business intent are all approved. It is still worked out from the model (the state, the fingerprint and the links), not kept as a separate "workable" flag, so §4's reason holds. ADR 031 §2 (any play writes any kind; a rule never stops a write) is kept and built on.

## Consequences

### Positive

- An agent knows what it may build from by reading the model it already works from. There is one place to look.
- A piece changed after it was approved is caught by its fingerprint, with no play having to remember to flag it.
- The person sees, every time the tool opens, what is approved, what changed and what is in progress.
- Git keeps the approval history with the model, in the same change.
- A write is never blocked: work stops, not writes, as ADR 031 set.

### Negative / Risks

- **More of the model waits for a person.** Every piece a play writes or rewrites is changed until approved. Agents may sit idle until the person reviews.
- **The ontology, the spine, the decision schema, the limits and the page shapes must all change**, under #597, before agents can rely on the rule.
- **Every play that works on ICE must read the approval state**, and the workable check must follow links up to the business intent.
- **Fingerprints are sensitive to small edits.** A change of a single word moves a piece to changed and sends it back to the person.
- **Three places approve outside the review step today:** `/intent` run by hand confirms an intent at its pinned gate (ADR 031 §5); `/adr` run by hand accepts a decision on the person's typed word; `/shape` sets capabilities `active`. This ADR says only the review step writes approval. How those three record approval (fingerprint, who, when) is not decided here; it must be settled when the lifecycle is built (#597).
- **The review step and the two tools are not built yet** (ADR 032). Until they are, nothing writes approval.

## Alternatives Considered

- **A separate approval record beside the model, kept by Garura** (the first draft of the tool plan, 18 October) — lost: Kapil, 2026-10-18, "that whole review and approval thing is part of the product model itself. It's not outside of it." A side record can disagree with the model, and agents would have to read two places to know what they may build.
- **Approval only inside each drive's review, nothing lasting** (ADR 032 as it stands) — lost: once the drive's review is over, nothing tells an agent that a later command changed an approved piece.
- **Keep only today's rule — work starts from an ICE whose business intent is confirmed** — lost: a capability, functionality or ICE changed by a command after its intent was confirmed would still be built from, unseen by any person.

## Work This Creates

None is filed yet; they are filed only when Kapil asks.

1. The approval lifecycle on every kind in the ontology, with each kind's existing states mapped onto it (#597).
2. The approval fields (fingerprint, who, when, which review) in the spine, the decision schema, the limits and the page shapes.
3. The workable check reads approval and follows links (`check_ice_workable.py` and every play that works on ICE).
4. The review step writes approved or in progress (story 5a in `review-tool.md`).
5. The review tool shows the whole model's approval state each time it opens.
6. Settle how `/intent` and `/adr` run by hand, and `/shape`'s `active`, record approval.

## References

- `.garura/project/issues/617/specs/review-tool.md` — "Approval is part of the product model", with Kapil's words
- `core/components/memory/standards/schemas/product-os/ontology.md` — "Who writes, and what the rules mean"; Business Intent, Rules
- ADR 032 — Drive review of outcomes; ADR 031 — Business intent and ICE; ADR 026 — Direct model writes
