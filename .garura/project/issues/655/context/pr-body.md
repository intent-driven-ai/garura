## What this delivers

The written agreement for how agents find and update memory (ADR 035 §4). The memory tool (#657), Phoenix memory (#656), memory updates (#658) and citations (#659) all build against it, and moving the tool to Griffin later changes nothing on Garura's side.

- **`core/tools/memory/contract/v1.json`** — version 1, in a subset of JSON Schema. Eleven commands: `health`, `find`, `search`, `read`, `cite` to find memory; `pull`, `pulled`, `propose`, `updates`, `decide`, `apply` to update it. Three tiers — `short-term`, `garura`, `phoenix` — looked in that order, stopping at the first tier that answers. Every piece of text carries its tier, file, lines and a fingerprint (sha256 of the text). A lookup never skips a tier: a tier with no setting is the error `tier_missing`, never "nothing found". A memory update goes waiting → approved or rejected → applied, and only a person decides.
- **`core/tools/memory/README.md`** — the plain guide: tiers, lookup order, commands, request and answer rules, errors, and what is not memory.
- **Sample answers and a check** — 15 samples (every command, the `tier_missing` and `not_approved` errors, and the empty answer that cues a memory update) pass; 12 broken samples fail; 20 tests cover the check itself. Run from `core/tools/memory/`: `python3 contract/check_contract.py` and `python3 contract/test_check_contract.py`.
- **Settled with Kapil** ("approve, A, A"): the learned checkpoint answers are not memory; a play's own working files stay direct — only memory lookups go through the tool.
- The folder names no project path and imports only the standard library, so it can move to Griffin as it is.

Also on this branch, as Kapil asked: the #653 plan update of 2026-10-18 (the files ADR 035 names, folded into plan items 3, 8 and 10) and a matching note in the #654 story texts.

Closes #655

## Self-review

Rules: base `standards/rules/self-review.md` (no project override). Findings that stop the raise: **none**. Full review: `.garura/project/issues/655/context/self-review.md`.

**Fixed before raising** (self-review findings 1–7 and 12): an answer could say "nothing found" after skipping a tier; search hits had no fingerprint and `pull` no tier; request and answer rules were unwritten; the check accepted `1` as `true` and a newline in a path, had a narrow boundary scan, and had no tests of its own; the #653 plan did not mark the contract built.

**Scope**
- [PASS] Matches #655: the contract, its guide, samples (including a missing-tier error) and a passing check, in the tool's own folder.
- [PASS] No code outside `core/tools/memory/`; the rest is plans and run records.

**Quality**
- [PASS] The check and its 20 tests pass; no merge conflicts; no secrets.
- [PASS] Commits are conventional and name #655.

**For the reviewer (non-blocking)**
- Eleven commands against the issue's list of nine: `health` is in the plan (the install check calls it); `pulled` shows what is behind; `decide` records a person's word. "Go up a tier" is the lookup order, not a command.
- `decide` cannot yet tell a person from an agent; that is #658's to settle.
- The two settled questions are recorded in the guide and the #655 plan; ADR 034 §2 still lists learned checkpoint answers, and ADR 035 still lists both as open.
- Three commit subjects run past 72 characters.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
