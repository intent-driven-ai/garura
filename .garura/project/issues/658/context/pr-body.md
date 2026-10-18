## What this delivers

**Memory updates, landing in short-term memory.** When no tier answers, an agent raises a memory update: what is missing, a drafted entry, where the draft came from (person, web, model or memory), and whether it blocks the work. Nothing in it is used until a person approves it. The approved answer is written to the issue's own short-term memory, and the work decides from memory. `core/tools/memory/` gains `propose`, `updates`, `decide` and `apply` (`updates.py`).

Kapil, 2026-10-18:
- "STM - always STM. i told you we will have /learn-memory and /promote-memory that will take care of project and phoenix memory" — every update lands in short-term memory, a person's own answers too; moving memory up is those plays, not this tool.
- "yes keeps going, unless the memory is really blocking" — an update carries `blocking`.
- "use the tool we built for product and intent... each needs an explicit approval from a human" — `decide` records the person, their words, and that they decided in the review tool. Until the tool is built, a local prototype page on the review tool's own design stands in ("it remains a local prototype for now"); it is not committed.

**Contract version 3** (`core/tools/memory/contract/v3.json`; versions 1 and 2 kept): updates target short-term memory only; `blocking`; `decided_in`; a Phoenix read says `saved_to` or `not_saved`; new error `would_overwrite`.

**The two faults from the PR #674 review are fixed:** `pull` takes the contract's `{path}`; a used Phoenix file is never saved over a different Garura file.

**A waiting draft is never used:** a lookup does not read the updates folder (a test caught that it did; fixed).

**Shown end to end, twice, with Kapil approving on the page:** two gaps raised two updates; neither was found while it waited; approved ones were written and found in the same issue, not in another; the rejected one was refused at apply and wrote nothing. Records: `.garura/project/issues/658/evidence/e2e-658.md`, `e2e-658-run2.md`.

The review tool's design (`.garura/project/issues/617/specs/review-tool.md`) now shows memory updates approved one by one in its Memory and ADRs section; the whole tool, with that section (#664), is built inside Garura in the #606 plan.

Closes #658

## Where the issue text no longer matches

| Issue says | What happened |
|---|---|
| A promotion moves an approved answer to Garura memory | Not here: `/learn-memory` and `/promote-memory` plays (not filed yet) |
| A person's own answers become Garura memory with stable ids | Not here: they land in short-term memory too ("STM - always STM") |
| Until the review tool exists, the person approves by typing | A local prototype page on the review tool's design stands in |
| The approval record proves a person gave the word | Recorded (who, words, review tool), not yet enforced: a caller can still run `decide` itself. The review tool's server (#642) keeps the person's answer as its own event |
| `propose-kb-node` becomes a memory update | Not here: it changes a skill, so it moves with the skills (#661, #663) |
| Settle whether a drive keeps going | Settled: it keeps going unless an update blocks (`blocking`); no drive reads the flag yet |

## Not in this change

- `/learn-memory` and `/promote-memory`; the review tool and its Memory and ADRs section (#641–#644, #664, in the #606 plan).
- Amending ADR 035 §5 and ADR 036 §2–§4 for these decisions (its own `/adr` change).

## Self-review

Rules: `standards/rules/self-review.md` from Phoenix memory (Garura memory has no copy). Blocking: **0**. Notes: 12, in `.garura/project/issues/658/context/self-review.md`.

Checks: `test_memory.py` 50 (51 after the fixes below), `test_pull.py` 13, `test_check_contract.py` 51; the contract check passes (24 samples, 26 broken, boundary); ruff clean; plans valid; merges cleanly with main; no client, personal or secret text.

Fixed after the self-review: an update can no longer target the updates folder (it could corrupt the update records); the `propose`, `decide` and `apply` summaries in the contract now say short-term memory only and the review tool; stale lines in the #658 and #653 plans. Not changed: one commit subject (`7ed299d1`) is 75 characters against 72.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
