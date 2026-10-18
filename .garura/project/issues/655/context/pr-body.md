## What this delivers

The written agreement for how agents find and update memory (ADR 035 §4). The memory tool (#657), Phoenix memory (#656), memory updates (#658) and citations (#659) all build against it, and moving the tool to Griffin later changes nothing on Garura's side.

- **`core/tools/memory/contract/v1.json`** — version 1, in a subset of JSON Schema. Eleven commands: `health`, `find`, `search`, `read`, `cite` to find memory; `pull`, `pulled`, `propose`, `updates`, `decide`, `apply` to update it. Three tiers — `short-term`, `garura`, `phoenix` — looked in that order, stopping at the first tier that answers. Every lookup names its issue, and short-term memory is only that issue's folder. Every piece of text carries its tier, file, lines and a fingerprint (sha256 of the text). A lookup never skips a tier: a tier with no setting is the error `tier_missing`, never "nothing found".
- **When no tier answers** — research drafts the answer, a person approves it (`decide`), and it is written to the issue's own short-term memory (`apply`). A draft from the web or the model never goes straight to Garura or Phoenix memory: that is a promotion, done outside the work. A memory update goes waiting → approved or rejected → applied, and only a person decides; a step in the wrong state is `not_approved` or `wrong_state`.
- **`core/tools/memory/README.md`** — the plain guide: tiers, lookup order, commands, when no tier answers, request and answer rules, errors, and what is not memory.
- **Sample answers and a check** — 20 samples pass (every command; the `tier_missing`, `not_approved`, `bad_request` and `wrong_state` errors; the empty answer that cues a memory update; a short-term answer, a search of every tier and a promotion); 23 broken samples fail, each for its own rule; 49 tests cover the check itself, and removing any one of its 44 rule lines fails a test. Run from `core/tools/memory/`: `python3 contract/check_contract.py` and `python3 contract/test_check_contract.py`.
- **Settled with Kapil, 2026-10-18:**
  - "approve, A, A": the learned checkpoint answers are not memory; a play's own working files stay direct — only memory lookups go through the tool.
  - After the first review of this PR: short-term lookups read only the current issue ("It reads only in the current issue that it is working on"); a researched answer is approved by a person and goes into the issue's short-term memory ("That information goes into STM, the local memory"); promotion "happens outside".
- The folder names no project path and imports only the standard library, so it can move to Griffin as it is.

Also on this branch, as Kapil asked: the #653 plan updates of 2026-10-18 (the files ADR 035 names, folded into plan items 3, 8 and 10; item 11 is now a **Memory and ADRs** section in the review tool, with the Catch up cards of #644) and a matching note in the #654 story texts.

Closes #655

## Self-review

Rules: base `standards/rules/self-review.md` (no project override). Findings that stop the raise: **none** (0 blocking, 13 non-blocking). Full review: `.garura/project/issues/655/context/self-review.md`. Checks, from `core/tools/memory/`: `python3 contract/check_contract.py` (exit 0), `python3 contract/test_check_contract.py` (OK), `ruff check contract/` (clean).

**Fixed before raising** (findings 1–4, 6, and the new commit subject of 9): a web or model draft could target Garura or Phoenix memory directly; 9 of the check's rule lines had no test; `every_tier` had no sample and two unchecked rules; refusals (`bad_request`) were never checked and `read` was not tied to its request; small drift between the contract, the guide and the plans. Finding 5 is also fixed: the new `wrong_state` error. The self-review file predates these fixes; the counts above are current.

**Size:** 65+ files, about 9,000 added lines; about 3,000 are the change (the tool folder and plans), the rest run records.

**For the reviewer (non-blocking, carried):**
- ADR 035 §5 says an approved update is written to Garura or Phoenix memory; it needs an amendment for the short-term step. §7 names a Memory view only; #653 item 11 is now a Memory and ADRs section. Both through `/adr`.
- ADR 034 §2 and ADR 035 "Not decided here" still list the two questions Kapil settled.
- `decide` cannot yet prove a person, not an agent, gave the word — #658.
- Eleven commands against the issue's nine: `health` (the install check calls it), `pulled` (what is behind), `decide` (a person's word). "Go up a tier" is the lookup order, not a command.
- Naming: `version` has three meanings; `pull` and `pulled` differ by one letter.
- Four older commit subjects run past 72 characters (pushed; not rewritten).
- The #653 plan notes and the #654 story note ride on this branch, as Kapil asked.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
