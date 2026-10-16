# Drive Contract

Single source of what a **drive contract** holds and how a play runs when it is handed
one (ADR 029; #614). A drive is a run of plays that keeps going until its goal is met,
then gets reviewed. The drive owns one issue, one branch and one pull request; the plays
inside it open none of their own. The contract is how a drive hands a play what it needs.

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
| `inputs` | no | Per play, the inputs the drive hands it (paths, or values such as intent ids). |
| `answers` | no | Per play, the answers to the questions the play would ask, gathered before the drive started (ADR 029: questions first). |

## How a play runs inside a drive

1. **Check the contract first.** Run `check_drive_contract.py`. It writes `run.json`
   (`in_drive`, `drive_run_id`, `branch`, `issue`, `review_dir`, the play's own
   `inputs` and `answers`). An invalid contract, or a current branch that is not the
   contract's branch, is a hard halt. With no `--contract`, it writes `in_drive: false`
   and the play runs by hand, unchanged.
2. **Open nothing.** Skip the injected `start-change` and the injected end sequence
   (commit-change → propose-change → review-change → merge-change). The drive opens and
   lands the change. The play still commits its own work on the drive's branch.
3. **Do not stop at the play's own checkpoint.** Write what the checkpoint would have
   shown — its summary and the files it stands on — as a review record, with
   `write_drive_review.py`, into `review_dir`. The drive's end review reads it.
4. **A question the drive did not answer still stops the play.** The play asks the
   person and never picks an answer for itself (ADR 029: a new question stops the
   drive).
5. **A learned checkpoint still learns.** A play whose checkpoint learns from people's
   answers (`gate_eval.py`) records the crossing as `deferred_to_drive_review`. The
   learner skips that line — it neither counts as an approval nor breaks a run of them —
   until the drive's review writes the person's real answer.

Run by hand, a play is unchanged: its opening, its checkpoint and its end sequence run as
its gate settings say.
