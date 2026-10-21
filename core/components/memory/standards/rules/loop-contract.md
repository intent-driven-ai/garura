# Loop Contract

Single source of what a **loop contract** holds and how a play runs when it is handed
one (ADR 029; #614). A loop is a run of plays that keeps going until its goal is met,
then gets reviewed. The loop owns one issue, one branch and one pull request; the plays
inside it open none of their own. The contract is how a loop hands a play what it needs.

**The issue ID governs** (ADR 039). Everything the loop and its plays write
— memory, evidence, working files, answers — goes under the loop's issue,
`{stm_base}<issue>/`. The issue ties the work to the tracker and to the business intent it
serves.

**A loop reads no memory**, and neither do its plays (ADR 039 §2): a loop and its plays are
workflows; their agents read memory, only through the memory tool.

Canonical checker: `play-creator/references/check_loop_contract.py`, stamped into each
play that can run inside a loop. Canonical review-record writer:
`play-creator/references/write_loop_review.py`. Plays read this rule; they do not
restate it.

## What a contract holds

A JSON file, passed to the play as `--contract <path>`:

```json
{
  "loop_run_id": "discovery-20261017-120000",
  "loop": "discovery",
  "branch": "feature/613-discovery",
  "issue": 613,
  "review_dir": ".garura/project/issues/613/review/loop/",
  "round": 1,
  "plays":   ["intent", "vision", "understand"],
  "inputs":  { "<play>": { "<input name>": "<path or value>" } },
  "answers": { "<play>": { "<question id>": "<the person's answer — asked before the loop started, or after a round's draft>" } }
}
```

| Field | Required | Meaning |
|-------|----------|---------|
| `loop_run_id` | yes | The loop's run id; every play records it, so the loop's review can find each play's record. |
| `loop` | yes | Which loop is running (e.g. `discovery`). |
| `branch` | yes | The loop's branch. The play must already be on it. |
| `issue` | yes | The loop's main issue. |
| `review_dir` | yes | Where each play writes its review record for the loop's end review. |
| `round` | no | The loop's round, from 1 (absent means 1). A play on a round above 1 fills what it left open. |
| `plays` | no | The loop's plays, in order (written by `write_loop_contract.py`). |
| `inputs` | no | Per play, the inputs the loop hands it (paths, or values such as intent ids). Under ADR 043 these are, besides any `argument`: `capture` — the one reading of the loop's source (`source_manifest`, `journeys`, `view_texts`, and the person's `write_up`), which the play reads instead of walking the source again; and, on a later round, `targets` — exactly the work the loop's gap skills gave this play. A play's input is never another play's output. |
| `answers` | no | Per play, the answers to the questions the play would ask, gathered before the loop started (ADR 029: questions first); on a later round, also the person's answers to the loop's questions (ADR 041). |

## How a play runs inside a loop

1. **Check the contract first.** Run `check_loop_contract.py`. It writes `run.json`
   (`in_loop`, `loop_run_id`, `branch`, `issue`, `review_dir`, `round`, the play's own
   `inputs` and `answers`). An invalid contract, or a current branch that is not the
   contract's branch, is a hard halt. With no `--contract`, it writes `in_loop: false`
   and the play runs by hand, unchanged.
2. **Write under the loop's issue.** The play's working folder goes to
   `{stm_base}<issue>/context/<play>/<run key>/`, its status markers to
   `{stm_base}<issue>/status/`, its evidence to `{stm_base}<issue>/evidence/<play>/`, and every
   question and answer to that issue's short-term memory — `<issue>` is the contract's
   `issue`. Run by hand, the same paths hold with the issue `start-change` gives.
3. **Open nothing.** Skip the injected `start-change` and the injected end sequence
   (commit-change → propose-change → review-change → merge-change). The loop opens and
   lands the change. The play's OWN commit step — the one in its workflow, such as a model
   play's "commit the model delta" — still runs, on the loop's branch, so the next play in
   the loop starts from a clean tree; the loop commits the round once more after its gap
   skills (ADR 043).
4. **Resolve the play's checkpoint as by hand; never wait at a conditional one.** Resolve
   the gate exactly as `gate-config.md` says. A config skip is recorded as a skip and a
   policy auto-pass as an auto-pass, as by hand. Only where the gate would WAIT does the
   play not wait: it writes what the checkpoint would have shown — its summary and the
   files it stands on — as a review record, with `write_loop_review.py`, into
   `review_dir`, and records `checkpoint deferred to the loop's review (loop
   <loop_run_id>)` as a Checkpoint Decisions row. The loop's end review reads the record.
   **A pinned checkpoint is never deferred by a contract.** `gate-config.md` says a pinned
   gate never resolves off. Inside a loop it is either asked up front — its answer is in
   the contract's `answers` — or it becomes the loop's question, like any other the play
   cannot answer (rule 5; ADR 041): the play stops short of the crossing, saves what it made
   as proposed, and finishes; the person answers on a later round, and the play crosses the
   gate then. That is not a deferral to the loop's review. A play may defer a pinned checkpoint to the loop's review
   only where its own intent names that exception (as `/intent`'s confirmation does,
   ADR 031 D10).
5. **A question the play cannot answer goes to the loop — it does not stop the play.** The
   play's agents look in memory first, through the memory tool (ADR 034, ADR 035); what no
   tier answers and research can, is drafted as a memory update a person approves (ADR 035 §5,
   ADR 036 §2) — nothing rests on it before that. A question still open is written to
   `<review_dir>/open-<play>.json` (`{"play", "round", "questions": [{"id", "ask", "about",
   "blocks", "for_person", "examples"}]}`); the play does all the work it does not block,
   saves what it made as proposed with the gap named, never picks an answer for itself, and
   closes. On a later round (the contract's `round` is above 1) the play reads what the other
   plays wrote and fills what it can — only from its sources, approved memory (an applied
   memory update included) and the product model the loop's plays wrote; never from a
   memory update still waiting for a person (ADR 035). A question no play of the loop can
   answer goes to the loop's knowledge plays: they search the sources and memory, draft
   knowledge pages and our proposed answers, and the loop briefs the person on what is left —
   never a questionnaire (ADR 041, ADR 042). The person's answers are kept in the loop issue's
   short-term memory (ADR 039 §1) and reach the play on the next round as
   `answers.<play>.<question id>`.
6. **A learned checkpoint still learns.** A play whose checkpoint learns from people's
   answers (`gate_eval.py`) records a deferred crossing as `deferred_to_loop_review` (a
   skip or an auto-pass is recorded as by hand). The learner skips that line — it neither
   counts as an approval nor breaks a run of them. The loop's review later appends the
   person's real answer as a new line for the same shape (the ledger is append-only); how
   the loop's review does that belongs to the loop-review design (#617).
7. **Close as a sub-play.** The play runs the Standard Play Close (`_shared/play-close.md`,
   beside the plays): its evidence file as `evidence.record` says, no delivery report of its
   own, and a compact result for the loop. The loop writes the one delivery report for the
   run, and its own evidence.

Run by hand, a play is unchanged: its opening, its checkpoint and its end sequence run as
its gate settings say.

## One contract for the whole loop

A loop writes one contract and hands the same file to every play it runs; each play reads
its own `inputs.<play>` and `answers.<play>`. No play's input is another play's output (ADR 043):
the plays read the one capture and write their own kind, and the loop links what they wrote
after the round with its gap skills. When the source is read (R4b) or a round gives a play
work, the loop adds it to that play's `inputs` and writes the file again before the play
starts (same `loop_run_id`). At the start of each round it writes the file again with the new
`round` and any answers the person gave; a play reads the contract when it starts. A play with an older, narrower check of its
own (`/intent` checks only `loop_run_id` and `branch`) accepts the full contract, because
the full contract holds those fields too; such plays move to the shared checker over time.

## Related

- ADR 029 — Drives, now loops (ADR 045) (questions first; no stops for the plays' checkpoints; a new question
  stops the loop; the loop owns one issue, one branch, one pull request).
- ADR 041 — a loop runs in rounds and owns the questions no play can answer.
- ADR 042 — the knowledge member plays: `/search-knowledge` and `/build-knowledge` find and build
  what the loop lacks; `/review-knowledge` briefs the person, never a questionnaire.
- `standards/rules/gate-config.md` — gate kinds; the `deferred_to_loop_review` answer.
- `standards/rules/pipeline-position.md` — the injected opening and end sequence a loop skips.
