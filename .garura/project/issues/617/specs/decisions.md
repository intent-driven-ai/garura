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

## Q1 — What the review looks at

**Draft:** the review pack — every line in the table above, gathered into one place. One
line per thing to decide: each proposed intent, each play's record, each box-move, each
owed learned answer, each big plan update; then the checker's result and the evidence as
background. A script gathers the pack from the drive's `review_dir`, the model and the
plan. The person does not hunt for it.

**Stands on:** the records already exist (#614, #615); ADR 029 §2 moved the plays'
reviews to the end, so the end review must show all of them.

## Q2 — Who reviews, and what they can do

**Draft:** a person reviews, in the review tool (Q7) — not on the pull request. The checker runs first, and its
result is in the pack; it never decides for the person. For each line the person can:

- **accept** — the proposed thing becomes real (intent confirmed, decision accepted, the
  record marked decided, the learned answer appended as an approval);
- **drop** — the proposed thing is removed from the branch (intent dropped, decision
  rejected, the piece it wrote taken back out);
- **send back** — the drive re-runs that one play, for that one item, on the same branch,
  with the person's note as its answer; the item comes back to the review.

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

1. The person answers every line (accept, drop, send back) in the review tool (Q7). Send-backs run and come back
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

## Q7 — The review tool — **the key question**

Kapil, 2026-10-17: "what is key is how the review happens. the drive will create a lot of
files and lot of content and PR cant be be way toreview this. this needs a proper review
tooling. we hae to build that right"

So the pull request only lands the change. The person reviews in a proper review tool.
One Kickoff run writes intents, a vision, domains, capabilities, functionalities, a
profile and decisions: dozens of files. A file-by-file diff on a pull request shows lines
that changed, not what the product now says.

**What exists to build on:**

- **#569** (open, no parent): the human-review loop for plays — a browser viewer per
  play, comments on any part, `--refine` fixes the comments, `--approved` is the only way
  the play is done, `--view` opens it again; one shared design system; each play decides
  what its viewer shows. It was written for a play run by hand. Its open questions
  (how a play declares its view, where comments live, how approval fits the gates) are the
  same questions the drive review has.
- **Two local prototypes**, not Garura features: `pr-reviewer` (reviews a pull request's
  files, with comments and per-file verdicts, and a watcher that tells Claude when a
  review is finished) and `play-reviewer` (reviews one play's files). They show what
  works and what does not; they are not the thing to ship.

**Draft answers (not yet put to Kapil):**

- **One tool, for a play run by hand and for a drive.** A play run by hand is a review of
  one play; a drive's review is the same tool showing every play's part. #569 becomes part
  of this work instead of a separate track.
- **It shows the product, not files.** The person reads by meaning: business intent →
  domain → capability → its functionalities and needs, with the vision, the profile and
  the decisions beside them. Each piece shows what changed in this drive. The files stay
  one click away.
- **Each line is a decision.** Accept, drop, or send back with a comment (Q2). A comment
  on any part. Nothing is lost if the person closes the page and comes back.
- **The answers are files on the branch.** The tool writes the person's answers into the
  drive's `review_dir`; the review step reads them and applies them (Q5). Claude never
  reads a web page to learn an answer.
- **Local.** It runs on the person's machine, from the repo, like the prototypes.

**Still to decide:** how each play declares what it shows; the design system (#569); how
send back and refine meet; whether the tool also shows the checker's findings inline.

## Stories this would file (draft — filed only when Kapil asks)

1. A script that gathers the review pack from a drive's `review_dir`, the model and the
   plan.
2. The review tool (Q7), built with #569 as one tool for plays and drives.
3. The review step, the drive's last step (Q4 A): open the tool on the pack, read the
   person's answers, apply them (Q2, Q5).
4. The failed-drive path: fix and resume, or drop the drive (Q3).
5. Dropping a box-move: lower the limit, send the capability back (Q6 A).
6. Kickoff (#613) runs the review as its last step.
