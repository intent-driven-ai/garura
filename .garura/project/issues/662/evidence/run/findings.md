# #662 run — findings (as they come)

Test project `cart-shop`, Garura installed from main (after #661), run under one drive contract
(issue 1, branch `feature/1-cart-shop-kickoff`), each play started with `claude -p` in the
project so it loads the project's own plays and agents.

## /intent (2026-10-20)

Worked: the agent read the ontology from Phoenix memory through the tool, copied it to
short-term memory and kept a trace (`citations --check` ok, 2 records); the person's answers
are in the issue's short-term memory (`answers.yaml`, marked as picked examples); every file
under issue 1; the model delta committed on the drive branch (`852e996`); nothing to GitHub;
the goal saved as proposed for the drive's review.

Findings:
- I-1 — `preflight.py` does not accept `--contract`; the play ran it without the flag.
- I-2 — the close did not ask `template-manager` for its templates (Step L of
  `_shared/play-close.md`), so no delivery report was rendered from the template.
- I-3 — the session stamp found no session id (headless run); soft, never blocks.

## /vision (2026-10-20)

Worked: seeded the ecommerce domain, three directional capabilities and a directional profile,
committed on the drive branch (`bd1e485`); grounding read through the tool; 10 decision records,
`citations --check` ok; no wait at the checkpoint (drive) — a review record in
`review/drive/`; a memory update raised where no tier answered: `mu-20261020-001`
("Abandoned-cart recovery", `draft_source: model` — no web research in a headless run),
target the issue's short-term memory. Kapil approved it ("approve"); applied to
`1/context/answers/kb/ecommerce-abandoned-cart-recovery.md`.

Findings:
- V-1 — the judge's guidance cut (`guidance_block.py`) gives the detailed-stage guidance only;
  /vision writes directional docs, so the first judging failed; the run made its own
  directional guidance file. The cut must pick the stage's block. (A fault in #661's H3 fix.)
- V-2 — the conditional gate's learning files (`.garura/core/gate-evals.jsonl`,
  `.garura/core/gate-policy.yaml`) are written outside the issue (config
  `gates.conditional.ledger|policy`), against "the issue ID governs".
- V-3 — the contract's `decide` allows only `decided_in: review-tool`; the review tool is not
  built, so a typed approval in a session is recorded under that value.
- V-4 — the run files under issue 1 (`context/`, `review/`) are left uncommitted by the play;
  "the drive decides" — the drive's own commit owns them (#613).

## /understand (2026-10-20)

Worked: detailed all three capabilities (13 grounding docs, all passed the judge — two after one
rewrite), set the quality bar, committed on the drive branch (`240634f`); the scope guard held.
**The approved memory update was found and used**: 14 decisions rest on
`1/context/answers/kb/ecommerce-abandoned-cart-recovery.md` (the applied `mu-20261020-001`).
Six new memory updates raised where no tier answered (`mu-20261020-002` … `-007`: abandonment
window, win-back window, privacy regimes ×2, reminder frequency, record retention) — waiting
for a person, none approved by the play.

Findings:
- U-1 — decisions resting on the applied update do not set `from_update` in their record; the
  trace's source names the applied file, but the link to the update is not explicit.
- U-2 — every memory update's draft is `draft_source: model`; a headless run cannot research
  the web, so a person approves model drafts.
- U-3 — the play first handed eight judges a placeholder path (no guidance), noticed, and
  re-ran them with the real paths (the H3 cut works when called with real paths).
- U-4 — cost: /understand about $11.8 for three capabilities (13 docs); /vision about $5.2;
  /intent about $2.5.

## The whole run — checks (item 6)

- `citations --issue 1 --check`: ok, 30 decision records, 0 problems, none without a trace.
  Trace steps by tier: Phoenix 43, short-term 21, Garura 4 (the product model).
- A memory update raised, approved and used: `mu-20261020-001` — raised by /vision, approved
  by Kapil ("approve", 2026-10-20), applied to the issue's short-term memory, used by 14
  /understand decisions.
- No answer from the model alone: every gap became a memory update (7 in all); the person's
  answers (/intent) are in the issue's short-term memory, marked as picked examples.
- Files: every run file is under issue 1, except the gate learning files (V-2).
- Nothing written to GitHub (drive contract).

Records: `issue-1/` (the issue's short-term memory, status markers left out), `model/` (the
product model the three plays wrote), `drive-branch-log.txt`, `citations-check.json`,
`memory-updates.json`.

## Dispositions (item 7, 2026-10-20)

Fixed on this branch (Kapil: "go ahead with the five fixes"):
- I-1 — `/intent` checks a drive contract with the shared `check_drive_contract.py` (`cf57a928`).
- V-1 — `guidance_block.py --stage`: the judge gets its doc's own stage's guidance (`9a0538fb`).
- V-2 — each issue keeps its own gate history (`review/gate-evals.jsonl`); the learner reads
  every issue's ledger for the one project policy (Kapil chose 1) (`b78e0cda`).
- V-3 — `decide` accepts `decided_in: session` (Kapil chose 1) (`2bc2da48`).
- U-1 — `cite` names the applied update a decision rests on (`2bc2da48`).

For their own issues (filed when Kapil asks):
- I-2 — the play close did not ask `template-manager` for its templates.
- V-4 — in a drive, the run files under the issue are left uncommitted (the drive's commit, #613).
- U-2 — a headless run cannot research the web; every memory update draft was the model's.
- I-3 — the session stamp finds no session id in a headless run (soft; noted only).
- U-4 — cost of one run: about $2.5 (/intent), $5.2 (/vision), $11.8 (/understand) (noted only).
