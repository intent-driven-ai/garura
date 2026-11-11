# BI-8 close: the proposal shown to the product owner (draft, not applied)

2026-11-10. BI-8 (Developer tooling) has its two capabilities in the model: Ship every change the same way, and Review what agents make (Argus). This is the close, as for BI-4, BI-6 and BI-7: BI-8's page brought in line with the two, the domain question settled, the approved pages that left the domain to the close brought in line, and the approved lines that still name the dropped self-review, or give the review to Ship every change the same way, brought in line. Nothing is applied before the product owner's yes.

## 1. BI-8's page (`.garura/product/product-os/intents/bi-8.md`)

Lines of the page quoted on approved pages: the Outcome's opening words ("People judge what agents made at the level of the outcome", on Ship every change the same way) and "ship with Garura" (two open points on Argus's pages); the Why (Argus); the second Proof (two Argus features); the Must not (two Argus pages). Every quoted part stays word for word.

- Outcome, first sentence, widened to the agreed capability line:
  - Old: People judge what agents made at the level of the outcome, reviewing ADRs, memories, domains, capabilities and ICE in tools that ship with Garura.
  - New: People judge what agents made at the level of the outcome, reviewing business intents, ADRs, memories, domains, capabilities, ICE and agent decisions in tools that ship with Garura.
- Outcome, kept: Argus comes first.
- Outcome, one sentence added after it, the product owner's agreed line for the first capability: Every change goes from opening to merge through the same steps, with an outside review and a person's yes.
- Why, kept, one sentence added after it: Every change must also land the same way, so each one can be traced from its issue to its merge.
- Proof, kept: the two lines.
- Proof, one line added after them: Every change that lands went through the same steps, and none merged without the outside review's approval and a person's yes.
- Must not: kept.
- Stage, tracker and the 19 Touches lines: kept.
- "ship with Garura" stays, because how Argus reaches a project is an open point on two approved pages.

## 2. The domain question: both capabilities stay in software delivery planning

- Decision proposed: Ship every change the same way and Review what agents make (Argus) stay in software delivery planning, and the domain's first paragraph says so.
- Why: the domain already holds every part these two land and review, the review of each change (Check the code against its standards) sits there, and BI-6 and BI-7 settled the same way. The domain's name is parked for a later review.
- Also weighed: a domain of its own for Developer tooling. It lost for the reason BI-7's did: a new domain page now would be redone at the parked name review, and memory does not settle it: both capability pages record that no knowledge shelf covers landing a change or reviewing what agents made.
- The domain page (`.garura/product/product-os/software-delivery-planning/domain.md`), first paragraph, one sentence added before its last sentence:
  - Added: It also lands every change the same way, with an outside review and a person's yes, and gives people one tool to review what agents made.
  - Kept: "It does not release the work or run the product." and every other sentence.

## 3. The two capability pages that left the domain to the close

Each sentence is replaced; the rest of its paragraph stays word for word. Each page gains one Sources line quoting the domain page's new sentence, after its last Sources line.

a. ship-every-change/capability.md, line 27
- Old: It sits in software delivery planning for now; where Developer tooling sits is settled when its two capabilities are drafted.
- New: It sits in software delivery planning with Review what agents make (Argus), and the domain's first paragraph says so.

b. review-agent-work/capability.md, line 44
- Old: It sits in software delivery planning for now; its domain is settled at BI-8's close.
- New: It sits in software delivery planning with Ship every change the same way, and the domain's first paragraph says so.

Sources line added on both: - .garura/product/product-os/software-delivery-planning/domain.md: "It also lands every change the same way, with an outside review and a person's yes, and gives people one tool to review what agents made."

## 4. BI-4's three lines that name the dropped self-review

The product owner dropped the self-review on 2026-11-10 ("yes, record it with self-review dropped"). The rest of each line stays word for word.

c. check-code-against-standards/capability.md, line 12
- Old: Opening the branch, committing, raising the change with its self-review, and merging it with a person's yes stay with Ship every change the same way, …
- New: Opening the branch, committing, raising the change and merging it with a person's yes stay with Ship every change the same way, …

d. check-code-against-standards/capability.md, line 56
- Old: - Out: opening the branch, committing, raising the change with its self-review, and merging it with a person's yes. …
- New: - Out: opening the branch, committing, raising the change and merging it with a person's yes. …

e. check-code-against-standards/fn-review-each-change/feature.md, line 63
- Old: - Raising the change, its self-review, and merging it with a person's yes. Ship every change the same way, in Developer tooling, does them.
- New: - Raising the change and merging it with a person's yes. Ship every change the same way, in Developer tooling, does them.

## 5. BI-3's three lines that give the review to Ship every change the same way

The review of each change is Check the code against its standards', in Code → Validation; Ship every change the same way runs it as one step of its path ("the outside review stays BI-4's, as one step of this path", capabilities.md, the list set on 2026-11-10).

f. build-work-test-first/capability.md, line 65
- Old: - Out: opening the branch, committing, reviewing and landing the change. Ship every change the same way, in Developer tooling, owns them.
- New: - Out: opening the branch, committing and landing the change, and reviewing it. Ship every change the same way, in Developer tooling, owns the first three, and Check the code against its standards, in Code → Validation, reviews the change.

g. fix-defects-test-first/capability.md, line 70: the same old and new line as f.

h. fix-defects-test-first/fn-fix-defect-code/feature.md, line 77
- Old: - Committing, reviewing and landing the change. Ship every change the same way does them.
- New: - Committing, reviewing and landing the change. Ship every change the same way commits and lands it, and Check the code against its standards reviews it.

## 6. Left as they are

- The lines on Ship every change the same way's own pages that say the self-review is still run today: they describe the play as built.
- Sources lines that quote a record holding "a self-review" or the first Argus line (check-code-against-standards/capability.md, fn-673, fn-731, fn-recommend-changes, fn-hand-on-findings): each quotes its record truly, as of its date.
- "Review what agents make, in Developer tooling, owns it." on fn-recommend-changes and fn-hand-on-findings: it names the right capability.
- The open points on each page, which stay open, among them how Argus reaches a project and where its code is kept.
- The defects found and not filed: review-pr.bypass in core/config.yaml is read by no play's code; the self-review rules say it does not block the raise while check_self_review.py blocks it; /propose-change reads its rules by path and records a home-folder path (#982, #914); #664 is out of step with ADR 037; docs/components/plays.md lists six plays that are gone.
