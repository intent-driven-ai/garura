# Brief — how a finished drive is reviewed

Shape: markdown (a framework decision, `docs/adr/`).

## Decision

Every drive ends with a review, and the review is the drive's last step (not a drive of its
own). The person reviews the **outcome** of the drive, never its plays: what the drive changed
in the business intents (and the agent intents, ICE, under them) and in the product model
(domains, capabilities, functionalities, product limits, decisions). The review stays at the
outcome level, not the detail under it. The plan is not reviewed there.

The person reviews in two proper review tools, not on the pull request:

- an **intent review tool** — the business intents and the agent intents under each;
- a **product review tool** — the product model, read by meaning, not by file.

For each piece of the outcome the person can accept it, drop it, or send it back with a
comment (the play that writes that kind of piece re-runs for that one piece, on the same
branch). The answers are written as files on the drive's branch; the review step applies them
as one commit (statuses set, dropped pieces removed, the plays' review records marked decided,
learned-checkpoint answers appended, big plan updates marked approved). Then the end sequence
lands the change; the pull request only lands it, and the merge stays pinned to the person.

A failed drive gets the same review plus where it stopped and why; the person fixes and
resumes, or drops the drive (close the pull request, delete the branch, nothing merges).

Dropping a box-move (a raised product limit, whose decision `/understand` writes `proposed`
inside a drive) lowers the limit back to the highest level the accepted needs still ask for,
rejects the decision, and sends that capability back to `/understand` to fit or be cut.

The ontology is the fixed structure, made once; the product model is what the agents produce
inside it, and the person reviews it. `docs/philosophy/idsd.md`'s "the product model … not a
human interface; only its ontology is" no longer holds and is amended.

## Why now

A drive runs its plays without stopping, so each play's review moves to the drive's end
(ADR 029 §2). `/intent`, `/vision` and `/understand` now leave proposed intents, review records
and proposed decisions behind inside a drive (#612, #614, #615), and nothing picks them up.
Kickoff (#613) cannot be finished without the end review. ADR 029 §5 left it open (open
question 1, spike #617).

Kapil, 2026-10-17:
- "this is last step"
- "what is key is how the review happens. the drive will create a lot of files and lot of
  content and PR cant be be way toreview this. this needs a proper review tooling. we hae to
  build that right"
- "what we need is a product review tool and an intent review tool. Think of it: the plays and
  stuff are all either updating business intents or agenting intents, fundamentally updating
  the product model. That is what we need to review. That's what the outcome is. Reviewing the
  play itself does nothing. What we really need to focus on is the outcomes."
- "The human interaction happens at the input and the output. We're not reviewing the play
  itself. We're reviewing the outcome of the play, which is the product model, the business,
  and the end-to-end times."
- "No, the plan is not that we have to review it. We have to look at the outcomes: the intents
  and the product model."
- "Ontology is the structure. We are going to create it once, and everything is going to follow
  the ontology. … the user gives the intents. Agent intents are what the agent performs on, but
  the human looks at what the outcome is. The product model is what the agents work on. They
  give that piece, right, so that has to be reviewed by the human. Without that, we don't know
  what it is that we are building."

## Options considered

- **Review as a drive of its own** (ADR 029 §5's expectation) — lost: a drive does not stop
  for checkpoints, and the review is the one place that must stop for a person; one last step
  is fewer parts and can grow into a drive later.
- **Review on the pull request** — lost: one Kickoff run writes dozens of files; a pull
  request shows changed lines, not what the product now says.
- **A viewer per play (#569 as written)** — lost: reviewing a play does nothing; the person
  reviews the outcome. #569's loop (comment, fix, approve) carries over; its per-play viewer
  does not.
- **Show the plan in the intent review tool** — lost: the plan is how the person follows the
  work, not what they review.
- **Never raise a limit before the review** (change `/understand` so a box-move waits) — lost:
  it breaks write-then-review (ADR 026) and changes the play just merged in #615; the undo is
  mechanical because every capability is measured against the limit at the start of the run.
- **Keep idsd.md's line, reading the tools as showing "the ontology"** — lost: the ontology is
  the fixed structure; what the person reviews is the product model itself.

## Decided by

Kapil, 2026-10-17.

## Decided in

#617 (spike), under #594 and business intent #606. Working notes:
`.garura/project/issues/617/specs/decisions.md` (Q1–Q7).
