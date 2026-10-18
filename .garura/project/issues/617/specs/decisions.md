# Decisions — #617: how a finished drive is reviewed

Working notes for the spike. Each question from the issue gets a draft answer and the
committed source it stands on. A draft marked **open** needs Kapil's choice; the others
follow from what is already decided, and stand unless he changes them. Nothing here is
decided until it is in an ADR.

## What a drive leaves behind today

A Kickoff drive runs `/intent` → `/vision` → `/understand` on one branch. When it ends,
these things wait for a person:

| Left by | What waits | Source |
|---------|-----------|--------|
| `/intent` | every business intent it drafted, saved as `proposed`; its ICE is not workable until the intent is confirmed | ADR 031 §4–5, 612 D10 |
| `/vision` | one review record: what its checkpoint would have shown, `decided: false` | drive-contract.md §3, `write_drive_review.py` |
| `/understand` | one review record per capability, `decided: false`; each box-move as its own line, with a decision written `proposed` — and the product's limit already raised on the branch | #615, `persist_understand.py` |
| any play with a learned checkpoint | a `deferred_to_drive_review` line in its learning record; the real answer is still owed | drive-contract.md §5 |
| the drive's plan | big plan updates logged during the run, not yet approved | ADR 030; work-plan rule 15 |
| the drive | the checker's result (a different model or agent), and the evidence record | ADR 029 §2 |
| the drive, if it stopped | the question that stopped it, or the play that failed its done check | ADR 029 §2 and §6 "Halts if" |

Everything above is on the drive's branch. Nothing reaches main until the merge, and the
merge always waits for a person (merge-change C7, pinned).

These are what the plays leave, not what the person reviews. The person reviews the
outcome — the intents and the product model (Q1); the records above tell the review step
what changed and why.

## Q1 — What the review looks at — **decided: the outcome**

Kapil, 2026-10-17: "the plays and stuff are all either updating business intents or
agenting intents, fundamentally updating the product model. That is what we need to
review. That's what the outcome is. Reviewing the play itself does nothing. What we
really need to focus on is the outcomes." And: "The human interaction happens at the
input and the output. We're not reviewing the play itself. We're reviewing the outcome of
the play, which is the product model, the business, and the end-to-end times."

**Answer:** the review looks at what the drive changed in two things:

- **the business intents** — each intent the drive drafted or changed, and the agent
  intents (ICE) under it;
- **the product model** — the domains, capabilities, functionalities, product limits and
  decisions the drive wrote or changed.

It does not look at the plays. The plays' review records, the learned-checkpoint lines,
the checker's result and the evidence are how the review step knows what changed and why;
they are background, never the thing the person reads line by line. A person who accepts
an outcome has answered every play record that stood behind it.

**Stands on:** Kapil's words above; `docs/philosophy/idsd.md` ("A person has exactly two
interfaces: the intent they give, and the output they see"); ADR 031 (business intent and
ICE, two levels).

## Q2 — Who reviews, and what they can do

**Draft:** a person reviews, in the review tools (Q7) — not on the pull request. The
checker runs first, and its result is shown beside what it checked; it never decides for
the person. For each piece of the outcome — an intent, a capability, a limit, a
decision — the person can:

- **accept** — it becomes real (intent confirmed, decision accepted); the play records
  behind it are marked decided and their learned answers appended as approvals;
- **drop** — it is taken back out of the branch (intent dropped, decision rejected);
- **send back** — with a comment; the review step re-runs the play that writes that kind
  of piece, for that one piece, on the same branch, with the comment as its answer; the
  piece comes back to the review.

"Reopen part of the drive" is send back. The review never re-runs the whole drive.

**Stands on:** 612 D10 ("the last steps of a drive is where validation final review
happens — that is the review, pr etc."); ADR 029 §2 (checked by someone else); the
pinned merge.

## Q3 — A failed drive against one that scored

**Draft:** the same review, with one more line at the top: where the drive stopped and
why. Because nothing reached main, the person has two ways out:

- **fix and resume** — answer the question or fix the cause; the drive continues from the
  play that stopped, on the same branch; the review happens again at the new end;
- **drop the drive** — close the pull request and delete the branch; nothing merges; the
  main issue stays open, with the reason in its handoff.

Work the failed drive finished before it stopped is still reviewed line by line if the
person resumes. It is thrown away only if they drop the drive.

**Stands on:** ADR 029 §3 (one branch, one pull request); ADR 029 §5 (a review follows
either way).

## Q4 — Is the review a drive of its own — **decided: A**

ADR 029 §5 and the issue expect the review to become a drive of its own.

- **A — a review play that every drive runs last.** One play: gather the pack, show it,
  take the person's answer per line, apply the answers, then the change plays land it.
  The drive's last step is this play.
- **B — a review drive.** Its own run of plays — for example check, decide, land — that
  starts after a work drive ends.

**Decided: A** (Kapil, 2026-10-17: "this is last step"). The review is the last step of
every drive, not a drive of its own.

Why A was recommended: a drive does not stop for checkpoints (ADR 029 §2), and the review
is the one place that must stop for a person. A review drive would be the only drive whose
whole job is stopping. One play is fewer parts (Occam), and it can grow into a drive later
without undoing anything: the pack, the answers and the apply step stay the same
(reversible). Choose B if the review should later run its own checker and fix loop
without a person.

## Q5 — How the review closes the change

**Draft:** in this order, all on the drive's branch:

1. The person answers every line (accept, drop, send back) in the review tools (Q7). Send-backs run and come back
   until no line is open.
2. The answers are applied as one commit: statuses set, dropped pieces removed, records
   marked `decided: true`, learned answers appended, big plan updates marked approved.
3. The end sequence runs: commit-change → propose-change → review-change →
   merge-change. The pull request lands the change; it is not where the person reviews
   it (Q7). The merge is pinned and waits for the person, as today.
4. The merge closes the main issue and its child issues; the drive writes its one handoff
   on the main issue.

**Stands on:** ADR 029 §3 (the drive closes its change when its review is finished; one
handoff); drive-contract.md §5 (the review appends the real learned answer); merge-change
C7.

## Q6 — A dropped box-move — **decided: A**

Inside a drive `/understand` raises the product's limit at once (for example security from
high to xhigh) and writes the box-move's decision as `proposed`. If the person drops that
decision, the capability still needs more than the product now allows.

- **A — lower the limit and send the capability back.** Dropping a box-move sets the limit
  back to the highest level the accepted needs still ask for, rejects the decision, and
  sends that capability back to `/understand` to fit inside the limit (or to be cut). The
  play stays as merged in #615.
- **B — never raise the limit before the review.** Change `/understand` so that inside a
  drive it writes the box-move and its decision but leaves the limit as it is; accepting
  raises it. Dropping still sends the capability back.

**Decided: A** (Kapil, 2026-10-17: "A"). Lower the limit and send the capability back.

Why A was recommended: it keeps write-then-review (ADR 026) and the play as just merged.
Undoing is mechanical, because every capability is already measured against the limit as
it stood at the start of the run (#615). In Kickoff `/understand` is the last play, so no
later play reads the raised limit before the review. Choose B if a limit must never show a
level nobody has agreed to, even on a branch.

## Q7 — The review tools — **decided: review the outcome, with two tools**

Kapil, 2026-10-17, first: "what is key is how the review happens. the drive will create a
lot of files and lot of content and PR cant be be way toreview this. this needs a proper
review tooling. we hae to build that right". Then: "what we need is a product review tool
and an intent review tool" — see his words under Q1.

**Decided:**

- **The pull request only lands the change.** One Kickoff run writes dozens of files; a
  pull request shows changed lines, not what the product now says.
- **Two tools, both on the outcome:**
  - **the intent review tool** — the business intents and the agent intents (ICE) under
    each: what the person wants, who asked, the proof it is met, and what it is being
    broken into;
  - **the product review tool** — the product model: domains, capabilities,
    functionalities, product limits and decisions, read by meaning, not by file.
- **No play review.** A tool that shows one play's output is not the goal. #569 asked
  for a viewer per play; its loop (comment on any part, fix the comments, approve) carries
  over to the two outcome tools, but the per-play viewer does not.

**The level the person reviews at** (Kapil, 2026-10-17: "I'm not looking at the
low-level plans, the pieces, and the details, but an outcome is critical"): the
outcome — what the intents are and what the product is — not the detail under it.

**The product model is reviewed by the person; the ontology is not** (Kapil, 2026-10-17:
"Ontology is the structure. We are going to create it once, and everything is going to
follow the ontology. We don't need to update the ontology every single time. It's what
the ontology outputs." And: "the user gives the intents. Agent intents are what the agent
performs on, but the human looks at what the outcome is. The product model is what the
agents work on. They give that piece, right, so that has to be reviewed by the human.
Without that, we don't know what it is that we are building.").

- The ontology is the fixed structure, made once. It is not what the person reviews.
- The product model is what the agents produce inside that structure. It is the outcome,
  and the person reviews it.
- `docs/philosophy/idsd.md` says the product model is "not a human interface; only its
  ontology is". That no longer holds: the product model is written for the agents and
  reviewed by the person at the end of each drive, at the outcome level. The ADR amends
  that line and its table.

**The plan is not reviewed here** (Kapil, 2026-10-17: "No, the plan is not that we have
to review it. We have to look at the outcomes: the intents and the product model."). The
plan stays the person's way to follow the work (ADR 030); the review tools show only the
intents and the product model.

**Draft answers (not yet put to Kapil):**

- **Each piece shows what changed in this drive** — added, changed or removed — against
  main, at the outcome level. The detail under it is not what the person reviews.
- **Each piece is a decision** — accept, drop, or send back with a comment (Q2). A comment
  on any part. Nothing is lost if the person closes the page and comes back.
- **The two tools link both ways.** Business intents are already linked both ways to the
  parts of the product they touch (ontology v4, #637), so from an intent the person can
  open the capabilities it touches, and back.
- **The answers are files on the branch.** The tools write the person's answers into the
  drive's `review_dir`; the review step reads them and applies them (Q5). Claude never
  reads a web page to learn an answer.
- **Local.** They run on the person's machine, from the repo.
- **Used outside a drive too.** Any play that changes intents or the product model can
  open the same tools when run by hand, because they review the outcome, not the play.

**Still to decide:** the design system (#569); what #569 becomes.

**Prior art, not the thing to ship:** the local `pr-reviewer` and `play-reviewer`
prototypes (comments, verdicts, a watcher that tells Claude a review is finished).

## Stories — filed 2026-10-18 (Kapil: "file the stories and land it")

One list, merged 2026-10-18 from three that overlapped: ADR 032's "Work This
Creates", ADR 033's "Work This Creates", and the tool plan (`specs/review-tool.md`
§7). Each story names what a person gets and how we know it works.

**A. The review tool** — its own folder, built to move into Griffin.

1. **#641 · The contract.** The written agreement between Garura and the tool: what a
   review pack holds (each BInt, ICE and product part, before and after, with its
   approval state) and what events come back. Done when two example packs — a
   finished Kickoff and a failed one — pass the check.
2. **#642 · The server.** Garura can start a review, the tool keeps it, and every action
   comes back as a numbered event that is never lost. Done when the server's tests
   pass on the example packs and nothing in its folder mentions Garura.
3. **#643 · Reading.** The person sees the whole model's state (approved, changed, in
   progress), the Intents view (each BInt with its ICE under it) and the Product
   view, Final or Changes, Only changed or Everything. Light only. Done when the
   example pack reads well on a laptop and on a phone.
4. **#644 · Acting.** Comment on words or on an area, edit, remove, accept, send back,
   drop, Finish — in the full page and in Catch up (one card at a time). Done when
   each action, from either place, arrives as the same event.

**B. Approval in the product model** (ADR 033) — with the ontology work, #597.

5. **#645 · The approval states in the model.** Every piece carries approved, changed or
   in progress, with the fingerprint of its words, who and when; mapped onto
   confirmed, accepted and active. Done when a piece approved once shows "changed"
   after a play edits its words, and stays "approved" when nothing touches it.
6. **#646 · Agents work only on approved pieces.** The readiness check reads approval and
   follows links (ICE, its capability or functionality, its BInt). Done when an
   agent refuses an ICE whose BInt is not approved.
7. **#647 · Approval outside the review.** How `/intent` and `/adr` run by hand, and
   `/shape`, record approval. Needs a decision first (ADR 033, its Work item 6).

**C. Garura's side of the review** — under #594.

8. **#648 · Open and listen.** Garura works out what changed against main, builds the
   pack, opens the tool, and its listener writes each event onto the branch.
   Done when an action in the tool lands as a file on the branch.
9. **#649 · The send-back loop.** Garura reworks one sent-back piece, sends the new
   version, and replies on the comment. Done when a send-back comes back to the
   tool with the reply, and the comment is still pinned.
10. **#650 · The review step.** The drive's last step applies all answers as one commit
    and writes approval; it also handles a failed drive (fix and resume, or drop)
    and a dropped box-move (the limit goes back down). Done when a Kickoff branch
    ends in one commit that matches what the person chose.

**Changes to issues that already exist** (not new stories):

- #613 (Kickoff): "runs the review as its last step" added to its acceptance criteria (done).
- #569 (old per-play review viewer): closed as not planned, with a comment pointing to #641–#644 and #648–#650 (done).

Settled while building, not before filing: D1 (how events reach Garura, story 2
and 8) and D2 (the person's direct edits, story 4 and 10) — `specs/review-tool.md`
§9.
