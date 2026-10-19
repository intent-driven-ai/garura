# ADR 032 — A Drive Ends With a Review of Its Outcome, in an Intent Review Tool and a Product Review Tool

**Status:** Accepted — amended in part by [ADR 033](033-approval-in-the-product-model.md): §5 statuses set at the review become a lasting approval on each piece; §2/§3 the tools show the whole model's approval state every time they open; a send-back leaves the piece in progress; and amended in part by [ADR 035](035-agents-work-only-from-memory.md): §3 "Two review tools": the review tool (one app with Intents and Product views — .garura/project/issues/617/specs/review-tool.md) gains a third view, Memory: what each tier holds, the memory updates waiting for a person, and which memory each decision came from; and amended in part by [ADR 036](036-approved-answer-lands-in-short-term-memory.md): §3 "Two review tools", as amended by ADR 035: the third section is Memory and ADRs, not Memory — it also shows the ADRs waiting for a person, and every memory review and ADR review happens there, on the same Catch up cards as Intents and Product (#644); and amended in part by [ADR 037](037-agent-decisions-keep-a-trace-and-the-review-tool-has-five-sections.md): §3 "Two review tools", as amended by ADR 033, ADR 035 and ADR 036: the review tool has five sections — Intents, Product, ADRs, Memory and Agent decisions — in place of a third section called Memory and ADRs; the Intents and Product views, and ADR 033's part of §3 (they show the whole model's approval state when they open), stand
**Date:** 2026-10-17
**Level:** framework
**Decided by:** Kapil Viren Ahuja · **Decided in:** #617 (spike: how a finished drive is reviewed), under #594 and business intent #606; working notes in `.garura/project/issues/617/specs/decisions.md` (Q1–Q7)
**Amends:** ADR 029 — §5 "Every drive ends in a review" and Open Question 1; with it, how §2's "the plays' reviews happen after the drive ends" is done (through the outcome, not play by play) · ADR 030 — §5, inside a drive the big plan updates are marked approved when the review's answers are applied; the plan is not shown in the review · ADR 031 — §5, the person confirms or drops the proposed intents in the intent review tool, not on the pull request, and may send one back · ADR 026 — the Decision's "review happens through the feature-branch git diff and the end-sequence PR": inside a drive the person reviews the model writes in the two review tools, and the pull request only lands them; write-then-review stays
**Affects:** `docs/philosophy/idsd.md` ("The Plan Is the Human's Interface; the Product Model Is the Agent's": the product model is reviewed by the person, at the outcome level), `core/components/memory/standards/rules/drive-contract.md` (§3 review records, §5 learned answers appended by the drive's review), `core/components/memory/standards/rules/work-plan.md` (rule 15), `core/components/memory/standards/rules/direct-model-write.md` (the `/intent` and `/adr` exceptions' "drive's end review"), the `/understand` play (a dropped box-move; send-back for one capability), the `/intent` play (Step 4 and C4: where intents are confirmed; send-back for one intent), the `/vision` play (Step 6: its review record), `core/components/plays/play-creator/references/write_drive_review.py` (records marked decided by the review step), the Kickoff drive (#613, not built yet), and two new tools (not built yet)
**ICE impact:** The agent intents of the plays that run inside a drive change. `/intent` (C4, Step 4): its proposed intents are confirmed, dropped or sent back in the intent review tool. `/understand` (C8, C13): a dropped box-move is undone and the capability sent back; a send-back re-runs it for one capability. `/vision` (Step 6, C11): its deferred review record is answered through the outcome. The Kickoff drive (#613) gains the review as its last step. ICE as a kind does not change: an ICE is still workable only once its business intent is confirmed.
**Business intent check:** none — no person's business intent changes; the Business Intent kind keeps its stages and its rule that only a person confirms or drops it; only the place where the person does it changes
**Related:** ADR 029 (drives), ADR 030 (plan mode), ADR 031 (business intent and ICE), ADR 026 (direct model writes), #613 (Kickoff), #612, #614, #615 (`/intent`, `/vision`, `/understand` inside a drive), #569 (a review viewer), #637 (intents linked both ways to the product)

## Context

A drive runs its plays without stopping. So each play's review moves to the drive's end (ADR 029 §2).

Three plays now leave work behind inside a drive. `/intent` saves its intents as proposed (#612). `/vision` writes a review record (#614). `/understand` writes review records and proposed decisions, and it raises the product's limit at once when a capability needs more (#615). Nothing picks any of this up yet. The Kickoff drive (#613) cannot be finished without the end review.

ADR 029 §5 left the review open: "How a finished drive is reviewed is still open; the review will likely be a drive of its own." Its Open Question 1 points to this spike, #617.

A drive writes many files. Kapil, 2026-10-17: "the drive will create a lot of files and lot of content and PR cant be be way toreview this. this needs a proper review tooling."

He also set what the review is for: "the plays and stuff are all either updating business intents or agenting intents, fundamentally updating the product model. That is what we need to review. That's what the outcome is. Reviewing the play itself does nothing."

## Decision

### 1. The review is the drive's last step

Every drive ends with a review. The review is the drive's last step. It is not a drive of its own (Kapil: "this is last step").

### 2. The person reviews the outcome, not the plays

The person reviews what the drive changed:

- in the **business intents**, and the agent intents (ICE) under each;
- in the **product model**: domains, capabilities, functionalities, product limits and decisions.

The review stays at the outcome level, not the detail under it. The person never reviews a play. The plays' review records tell the review step what changed and why; they are not shown play by play.

The plan is not reviewed here. It stays the person's way to follow the work (ADR 030).

### 3. Two review tools, not the pull request

The person reviews in two proper review tools:

- an **intent review tool** — the business intents and the agent intents under each;
- a **product review tool** — the product model, read by meaning, not by file.

The pull request is not where the person reviews.

### 4. Accept, drop, or send back

For each piece of the outcome the person can:

- **accept** it;
- **drop** it;
- **send it back** with a comment. The play that writes that kind of piece re-runs for that one piece, on the same branch.

### 5. The answers are applied as one commit

The person's answers are written as files on the drive's branch. The review step applies them as one commit:

- statuses are set;
- dropped pieces are removed;
- the plays' review records are marked decided;
- learned-checkpoint answers are appended;
- big plan updates are marked approved.

Then the end sequence lands the change. The pull request only lands it. The merge stays pinned to the person.

### 6. A failed drive gets the same review

A failed drive gets the same review, plus where it stopped and why. The person then either:

- fixes it and resumes; or
- drops the drive: the pull request is closed, the branch is deleted, and nothing merges.

### 7. Dropping a box-move

A box-move is a raised product limit. Inside a drive, `/understand` writes its decision as `proposed`.

Dropping a box-move does three things:

- it lowers the limit back to the highest level the accepted needs still ask for;
- it rejects the decision;
- it sends that capability back to `/understand`, to fit inside the limit or be cut.

### 8. The ontology is the structure; the product model is reviewed

The ontology is the fixed structure, made once. The product model is what the agents produce inside it, and the person reviews it.

`docs/philosophy/idsd.md` says the product model is "not a human interface; only its ontology is". That no longer holds, and this ADR amends it. The product model is still written for the agents. The person reviews it at the end of each drive, at the outcome level.

### What this changes in older ADRs

- **ADR 029 §5 and Open Question 1** — answered: the review is the drive's last step, on the outcome.
- **ADR 030 §5** — inside a drive, big plan updates are marked approved when the review's answers are applied. The plan is not shown in the review. ADR 030 §0 (the plan is the person's interface) stands.
- **ADR 031 §5** — the person confirms or drops the proposed intents in the intent review tool, not on the pull request. Only a person confirms or drops a business intent, as before.
- **ADR 026** — inside a drive, the model writes are reviewed in the two tools, not as the pull request's diff. Write-then-review stays. Run by hand, a play's review is unchanged.

## Consequences

### Positive

- The person reviews what the product now says, not dozens of changed files.
- The proposed intents, review records and proposed decisions the plays leave behind now have a place to be answered.
- Kickoff (#613) can be finished.
- One last step is fewer parts than a review drive, and it can grow into a drive later.
- Write-then-review (ADR 026) is kept, and `/understand` stays as merged in #615.

### Negative / Risks

- **Two tools must be built** before a drive can be reviewed this way. Until then, Kickoff cannot close.
- **Nothing is seen until the end.** Work inside a drive is not looked at by a person until its last step.
- **The raised limit sits on the branch before anyone agrees to it.** A drop must undo it. The undo is mechanical, because every capability is measured against the limit at the start of the run.
- **Big plan updates are approved with the outcome, not read on their own.** The plan is not shown in the review.
- **Plays and rules must change to match:** `/intent`, `/vision` and `/understand`, the drive contract, the work-plan rule and `idsd.md`. Play changes go through each play's ICE source and `/play-editor`.
- **A send-back re-runs a play for one piece.** Each play that writes a reviewed kind must be able to do that on the drive's branch.

## Alternatives Considered

- **Review as a drive of its own** (ADR 029 §5's expectation) — lost: a drive does not stop for checkpoints, and the review is the one place that must stop for a person. One last step is fewer parts and can grow into a drive later.
- **Review on the pull request** — lost: one Kickoff run writes dozens of files. A pull request shows changed lines, not what the product now says.
- **A viewer per play (#569 as written)** — lost: reviewing a play does nothing; the person reviews the outcome. #569's loop (comment, fix, approve) carries over; its per-play viewer does not.
- **Show the plan in the intent review tool** — lost: the plan is how the person follows the work, not what they review.
- **Never raise a limit before the review** (change `/understand` so a box-move waits) — lost: it breaks write-then-review (ADR 026) and changes the play just merged in #615. The undo is mechanical, because every capability is measured against the limit at the start of the run.
- **Keep `idsd.md`'s line, reading the tools as showing "the ontology"** — lost: the ontology is the fixed structure; what the person reviews is the product model itself.

## Work This Creates

Draft stories from the spike's notes. None is filed yet; they are filed only when Kapil asks.

1. The intent review tool.
2. The product review tool.
3. A script that works out what a drive changed in the intents and the product model, against main, with the play records behind each change.
4. The review step, the drive's last step: open the tools on the drive's outcome, read the person's answers, apply them.
5. The failed-drive path: fix and resume, or drop the drive.
6. Dropping a box-move: lower the limit, send the capability back.
7. Kickoff (#613) runs the review as its last step.
8. #569 rewritten or closed to match.

## References

- `.garura/project/issues/617/specs/decisions.md` — Q1–Q7, with Kapil's words
- ADR 029 — Drives; ADR 030 — Plan mode; ADR 031 — Business intent and ICE; ADR 026 — Direct model writes
- `docs/philosophy/idsd.md` — "The Plan Is the Human's Interface; the Product Model Is the Agent's"
- `core/components/memory/standards/rules/drive-contract.md` — how a play runs inside a drive
