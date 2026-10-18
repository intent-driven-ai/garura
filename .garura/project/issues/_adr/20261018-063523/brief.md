# Brief — approval is part of the product model

Shape: markdown (a framework decision, `docs/adr/`).

## Decision

Approval is part of the product model itself, not a record kept beside it. Every piece of the
model carries its own approval state: each business intent, each agent intent (ICE), each
domain, capability and functionality, the product limits, and each decision. The person sees
three states:

- **approved** — a person accepted these exact words. The piece keeps a fingerprint of its
  words (a short code worked out from the text), who approved it, when, and in which review;
- **changed** — the piece is new, or its words no longer match the fingerprint it was approved
  with; it waits for a person;
- **in progress** — a person sent it back, and it is being reworked; the comments stay open
  until the new version comes back and is answered.

A dropped piece leaves the model; git and the review keep the record of the drop.

**Agents work only on approved pieces.** This is the governance rule of the product model.
Commands (plays, inside a drive or run by hand) may still write any piece, including an
approved one; the write moves that piece to *changed* by its fingerprint, with no play having
to remember to say so, and no agent builds from it until a person approves it again. A rule
stops work, never a write (ontology, "Who writes, and what the rules mean").

**Approval follows links.** An ICE built from a business intent that is not approved is not
approved either; a functionality inside a capability that is not approved waits with it.

**One lifecycle, mapped onto the states that exist.** An approved business intent is
`confirmed`; an approved decision is `accepted`; an approved capability or functionality is
`active`. The ontology names one approval lifecycle for every kind and maps these onto it, so a
page and its approval state never disagree.

**Only the review step writes approval.** It writes *approved* or *in progress* from the
person's answers. Plays write the model; the review tool writes nothing to the model.

**The review tool shows it every time it opens**, not only at the end of a drive: the whole
model's counts (approved, changed, in progress) and each piece's state. "Only changed" means
"everything not approved". A drive's end review (ADR 032) is that same view, narrowed to what
the drive changed.

This widens the ontology rule "Work starts only from an ICE built from a confirmed business
intent" (`core/components/memory/standards/schemas/product-os/ontology.md`, Business Intent,
Rules) from business intents to every piece, and amends ADR 032, whose review sets statuses
for one drive but keeps no approval that lasts after it. The ontology change itself (the
lifecycle on each kind) is built under the ontology work (#597); this ADR decides it.

## Why now

ADR 032 settled how a person reviews what one drive changed. But the product model keeps
changing after a review: any play may write any kind (ADR 031), by hand or inside a drive. With
nothing lasting, an agent cannot tell which pieces a person has agreed to, and a piece approved
last week and changed today would still be built from. Kapil, 2026-10-18: "as you set and
change a business intent, an [ICE], or the product model, this tool needs to keep good track of
what is approved and what needs to be changed." The Kickoff drive (#613) is built next and
makes the first pieces that need approval, so the rule must exist before it is built.

## Options considered

- **Approval as part of the product model (chosen).** Every piece carries its state; agents
  read it from the model they already work from; git keeps its history with the model.
- **A separate approval record beside the model, kept by Garura** (the first draft of the tool
  plan, 18 October). Lost: Kapil, 2026-10-18, "that whole review and approval thing is part of
  the product model itself. It's not outside of it." A side record can disagree with the model,
  and agents would have to read two places to know what they may build.
- **Approval only inside each drive's review, nothing lasting (ADR 032 as it stands).** Lost:
  once the drive's review is over, nothing tells an agent that a later command changed an
  approved piece.
- **Keep only today's rule — work starts from an ICE whose business intent is confirmed.**
  Lost: a capability, functionality or ICE changed by a command after its intent was confirmed
  would still be built from, unseen by any person.

## Decided by

Kapil Viren Ahuja, 2026-10-18, in his words: "To be clear, that whole review and approval thing
is part of the product model itself. It's not outside of it. Every time somebody opens up this
tool, they should be able to see what is changed, what is approved, and what is in progress.
It's just critical because agents can only work on things which are approved. Agents cannot
work on things which are non-approved. Commands can impact it, but that lifecycle is very
critical to the governance of the product model and what is being built." He chose to record
it now, inside #617 ("A").

## Decided in

#617 (spike: decide how a finished drive is reviewed), on branch
`feature/617-decide-how-a-finished-drive-is-reviewed`. Working notes:
`.garura/project/issues/617/specs/review-tool.md` (section "Approval is part of the product
model") and the #617 plan log.
