# BI-9 close: the proposal shown to the product owner (draft, not applied)

2026-11-11. BI-9 (Orchestration) has its five capabilities in the model: Orchestrate agent work through planning, Run plays as loops, Track execution in the team's tracker, Manage ADRs, and Give every gate a way past. This is the close, as for BI-4, BI-6, BI-7 and BI-8: BI-9's page checked against the five, the domain question settled, and the five capability pages that left the domain to the close brought in line. Nothing is applied before the product owner's yes.

## 1. BI-9's page (`.garura/product/product-os/intents/bi-9.md`): kept as it is

Each capability is already named on the page, so no line changes:
- Orchestrate agent work through planning: the Outcome's "through planning", and "A person always knows what's happening and what's next."
- Run plays as loops: the Outcome's "and loops".
- Track execution in the team's tracker: the Outcome's "tracked in the team's tracker".
- Manage ADRs: the Outcome's "with ADRs recorded as decisions are made".
- Give every gate a way past: the Must not, "Stop a person. Every gate has a way past it that records what's owed.", which that capability holds as work.
- The two Proof lines are each met by parts now in the model: "Any work traces up to its intent and down to its result." by Link each piece of work to its intent across trackers; "A person can see where everything stands." by the plan views and the one list of what is owed.
- Also weighed: a third Proof line for the way past. It lost: the Must not already says it, Give every gate a way past reads the second Proof as covering what is owed, and the page is the product owner's words, changed only when a capability needs it.

## 2. The domain question: the five capabilities stay in software delivery planning

- Decision proposed: all five stay in software delivery planning, and the domain's first paragraph says so.
- Why: the domain already holds the work these five order, run, track and record, and BI-6, BI-7 and BI-8 settled the same way. The domain's name is parked for a later review.
- Also weighed: a domain of its own for Orchestration. It lost for the reason BI-7's and BI-8's did: a new domain page now would be redone at the parked name review, and no knowledge shelf in any memory tier covers it (each of the five capability pages records "Shelf: none").
- The domain page (`.garura/product/product-os/software-delivery-planning/domain.md`), first paragraph (line 4), one sentence added before its last sentence:
  - Added: It also orchestrates the work: it chooses and orders what runs next, runs plays as loops, tracks the work in the team's tracker, records each decision on how the project is built as an ADR, and gives every gate a way past.
  - Kept: "It does not release the work or run the product." and every other sentence.

## 3. The five capability pages that left the domain to the close

On each page one or two sentences are replaced by one; the rest of the paragraph stays word for word. Each page gains one Sources line quoting the domain page's new sentence, after its last Sources line.

a. orchestrate-agent-work/capability.md, line 30
- Old: It sits in software delivery planning for now. The domain's first paragraph does not yet say that the domain also runs the work; that is owed at the close of Orchestration.
- New: It sits in software delivery planning with the other capabilities of Orchestration, and the domain's first paragraph says so.

b. run-plays-as-loops/capability.md, line 28
- Old: It sits in software delivery planning. The domain's opening does not say yet that the domain runs its work in loops; that line is owed at BI-9's close.
- New: It sits in software delivery planning with the other capabilities of Orchestration, and the domain's first paragraph says so.

c. track-execution/capability.md, line 25
- Old: It sits in software delivery planning for now; the domain's first paragraph is widened at BI-9's close.
- New: It sits in software delivery planning with the other capabilities of Orchestration, and the domain's first paragraph says so.

d. manage-adrs/capability.md, line 26
- Old: It sits in software delivery planning with the other capabilities of Orchestration. The domain's first paragraph does not name Orchestration yet; widening it is owed at this intent's close.
- New: It sits in software delivery planning with the other capabilities of Orchestration, and the domain's first paragraph says so.

e. give-every-gate-a-way-past/capability.md, line 34
- Old: as d.
- New: as d.

Sources line added on all five: - .garura/product/product-os/software-delivery-planning/domain.md: "It also orchestrates the work: it chooses and orders what runs next, runs plays as loops, tracks the work in the team's tracker, records each decision on how the project is built as an ADR, and gives every gate a way past."

## 4. Left as it is
- BI-9's Touches list (43 lines) and stage.
- The capability pages' Sources lines that quote the list's note "Owed at BI-9's close", which stay true as the record of where the line came from.
- The domain page's mark "To be deepened later", which a discovery play removes.

## How it is applied, on the product owner's yes
One run of enrich-grounding's named-line changes through product-os-keeper (six pages: the domain's line 4, and on each capability page its domain sentence's line and one Sources line), all or nothing; then the structure check, a check that only those lines changed, and the personal-path scan; then the result and the tree. Committing waits for "commit and cp".
