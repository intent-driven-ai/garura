# Drive Contract

Single source of what a **drive contract** holds and how a play runs when it is handed
one (ADR 029; #614). A drive is a run of plays that keeps going until its goal is met,
then gets reviewed. The drive owns one issue, one branch and one pull request; the plays
inside it open none of their own. The contract is how a drive hands a play what it needs.

**The issue ID governs** (ADR 039). Everything the drive and its plays write
— memory, evidence, working files, answers — goes under the drive's issue,
`{stm_base}<issue>/`. The issue ties the work to the tracker and to the business intent it
serves.

**A drive reads no memory**, and neither do its plays (ADR 039 §2): a drive and its plays are
workflows; their agents read memory, only through the memory tool.

Canonical checker: `play-creator/references/check_drive_contract.py`, stamped into each
play that can run inside a drive. Canonical review-record writer:
`play-creator/references/write_drive_review.py`. Plays read this rule; they do not
restate it.

## What a contract holds

A JSON file, passed to the play as `--contract <path>`:

```json
{
  "drive_run_id": "kickoff-20261017-120000",
  "drive": "kickoff",
  "branch": "feature/613-kickoff",
  "issue": 613,
  "review_dir": ".garura/project/issues/613/review/drive/",
  "round": 1,
  "plays":   ["intent", "vision", "understand"],
  "inputs":  { "<play>": { "<input name>": "<path or value>" } },
  "answers": { "<play>": { "<question id>": "<the person's answer, asked before the drive started>" } }
}
```

| Field | Required | Meaning |
|-------|----------|---------|
| `drive_run_id` | yes | The drive's run id; every play records it, so the drive's review can find each play's record. |
| `drive` | yes | Which drive is running (e.g. `kickoff`). |
| `branch` | yes | The drive's branch. The play must already be on it. |
| `issue` | yes | The drive's main issue. |
| `review_dir` | yes | Where each play writes its review record for the drive's end review. |
| `round` | no | The drive's round, from 1 (absent means 1). A play on a round above 1 fills what it left open. |
| `plays` | no | The drive's plays, in order (written by `write_drive_contract.py`). |
| `inputs` | no | Per play, the inputs the drive hands it (paths, or values such as intent ids). |
| `answers` | no | Per play, the answers to the questions the play would ask, gathered before the drive started (ADR 029: questions first). |

## How a play runs inside a drive

1. **Check the contract first.** Run `check_drive_contract.py`. It writes `run.json`
   (`in_drive`, `drive_run_id`, `branch`, `issue`, `review_dir`, `round`, the play's own
   `inputs` and `answers`). An invalid contract, or a current branch that is not the
   contract's branch, is a hard halt. With no `--contract`, it writes `in_drive: false`
   and the play runs by hand, unchanged.
2. **Write under the drive's issue.** The play's working folder goes to
   `{stm_base}<issue>/context/<play>/<run key>/`, its status markers to
   `{stm_base}<issue>/status/`, its evidence to `{stm_base}<issue>/evidence/<play>/`, and every
   question and answer to that issue's short-term memory — `<issue>` is the contract's
   `issue`. Run by hand, the same paths hold with the issue `start-change` gives.
3. **Open nothing.** Skip the injected `start-change` and the injected end sequence
   (commit-change → propose-change → review-change → merge-change). The drive opens and
   lands the change. The play's OWN commit step — the one in its workflow, such as a model
   play's "commit the model delta" — still runs, on the drive's branch, so the next play in
   the drive starts from a clean tree.
4. **Resolve the play's checkpoint as by hand; never wait at a conditional one.** Resolve
   the gate exactly as `gate-config.md` says. A config skip is recorded as a skip and a
   policy auto-pass as an auto-pass, as by hand. Only where the gate would WAIT does the
   play not wait: it writes what the checkpoint would have shown — its summary and the
   files it stands on — as a review record, with `write_drive_review.py`, into
   `review_dir`, and records `checkpoint deferred to the drive's review (drive
   <drive_run_id>)` as a Checkpoint Decisions row. The drive's end review reads the record.
   **A pinned checkpoint is never deferred by a contract.** `gate-config.md` says a pinned
   gate never resolves off. Inside a drive it is either asked up front — its answer is in
   the contract's `answers`, gathered before the drive started — or it becomes the drive's
   question, like any other the play cannot answer (rule 5; ADR 041). A play may defer a pinned checkpoint to the drive's review
   only where its own intent names that exception (as `/intent`'s confirmation does,
   ADR 031 D10).
5. **A question the play cannot answer goes to the drive — it does not stop the play.** The
   play's agents look in memory first, through the memory tool (ADR 034, ADR 035); what no
   tier answers and research can, is drafted as a memory update a person approves (ADR 035 §5,
   ADR 036 §2) — nothing rests on it before that. A question still open is written to
   `<review_dir>/open-<play>.json` (`{"play", "round", "questions": [{"id", "ask", "about",
   "blocks", "for_person", "examples"}]}`); the play does all the work it does not block,
   saves what it made as proposed with the gap named, never picks an answer for itself, and
   closes. On a later round (the contract's `round` is above 1) the play reads what the other
   plays wrote and fills what it can — only from its sources, approved memory (an applied
   memory update included) and the product model the drive's plays wrote; never from a
   memory update still waiting for a person (ADR 035). A question stops the **drive** only when no play of the
   drive can answer it: the drive asks it then, with its other open questions, all at once
   (ADR 029 §2 as ADR 041 reads it: the question belongs to the whole drive). The person's answer is kept in the drive issue's short-term memory (ADR 039 §1).
6. **A learned checkpoint still learns.** A play whose checkpoint learns from people's
   answers (`gate_eval.py`) records a deferred crossing as `deferred_to_drive_review` (a
   skip or an auto-pass is recorded as by hand). The learner skips that line — it neither
   counts as an approval nor breaks a run of them. The drive's review later appends the
   person's real answer as a new line for the same shape (the ledger is append-only); how
   the drive's review does that belongs to the drive-review design (#617).
7. **Close as a sub-play.** The play runs the Standard Play Close (`_shared/play-close.md`,
   beside the plays): its evidence file as `evidence.record` says, no delivery report of its
   own, and a compact result for the drive. The drive writes the one delivery report for the
   run, and its own evidence.

Run by hand, a play is unchanged: its opening, its checkpoint and its end sequence run as
its gate settings say.

## One contract for the whole drive

A drive writes one contract and hands the same file to every play it runs; each play reads
its own `inputs.<play>` and `answers.<play>`. When a later play's input is what an earlier play made,
the drive adds it to that play's `inputs` and writes the file again before the later play
starts (same `drive_run_id`); a play reads the contract when it starts. A play with an older, narrower check of its
own (`/intent` checks only `drive_run_id` and `branch`) accepts the full contract, because
the full contract holds those fields too; such plays move to the shared checker over time.

## Related

- ADR 029 — Drives (questions first; no stops for the plays' checkpoints; a new question
  stops the drive; the drive owns one issue, one branch, one pull request).
- ADR 041 — a drive runs in rounds and owns the questions no play can answer; `/build-memory`
  builds the memory it lacks before it asks.
- `standards/rules/gate-config.md` — gate kinds; the `deferred_to_drive_review` answer.
- `standards/rules/pipeline-position.md` — the injected opening and end sequence a drive skips.
