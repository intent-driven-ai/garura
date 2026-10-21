# ADR 044 — The Shared Drive Run Owns the Steps Between Plays, and Inside a Drive the Gap-Closing Script May Write Shared Model Files

**Status:** Accepted
**Date:** 2026-10-21
**Level:** framework
**Decided by:** Kapil Viren Ahuja · **Decided in:** #693 — after the reviews of PR #691 (#689) and PR #696 (#692, finding H1)
**Amends:** ADR 029 — §2 "How a drive runs", the bullet "No rules of its own": the Shared Drive Run owns the run steps every drive runs between its plays (R3 the write-up, R4b reading the source once, R5 the two gap skills after each round); a drive still has no product rules of its own · ADR 026 — Decision, "Containment split", "Every shared file … is written solely by the play's deterministic keyed script": inside a drive, `close-model-gaps`' script `apply_links.py` may also write shared model files and move holding-folder pages, only inside `<product_base>product-os/`
**Affects:** `core/components/drives/_shared/drive-run.md` (its opening line, R3, R4b, R5 step 7), `core/components/skills/close-model-gaps/` (`SKILL.md`, `scripts/apply_links.py`, `scripts/intent_touches.py`, `scripts/test_apply_links.py`), `core/components/agents/product-os-keeper.md` (the "Write a shared model file yourself" rule and its drive exception), `core/components/memory/standards/rules/direct-model-write.md` (rule 3 and lint L-DMW-5), `core/components/plays/drive-creator/SKILL.md` ("carries no rules of its own"), `core/components/plays/drive-creator/scripts/lint_drive.py` and `core/components/plays/drive-editor/scripts/lint_drive.py` (docstring citing ADR 029 §2), `core/grounding/glossary.md` (the Drive entry)
**ICE impact:** none for any play or drive — Kickoff and its plays already run this way (ADR 043). The `product-os-keeper` agent keeps one declared exception to its shared-file rule: inside a drive, its `close-model-gaps` script writes the spine and intent pages' Touches lists and moves holding-folder pages. This records that exception; it does not widen it.
**Business intent check:** none — a framework decision on what the Shared Drive Run owns and who writes shared model files. `close-model-gaps` writes only the Touches link list on an intent page, never intent content; the Business Intent kind's rules stand (ADR 031).
**Related:** ADR 026, ADR 029, ADR 041, ADR 042, ADR 043, #689, #691, #692, #696, #693

## Context

ADR 043 decided that a drive reads the source once, takes a short write-up from the person, and closes the model's gaps after each round with two skills. That work now lives in the Shared Drive Run (`drive-run.md`), the steps every drive shares.

Two older rules still say otherwise. Reviews found both.

- The review of PR #691 (#689) found that ADR 029 §2 says a drive has "no rules of its own". But `drive-run.md` now owns the capture, the write-up and the gap closing.
- The review of PR #696 (#692, finding H1) found that ADR 026, and the model keeper's rules on main, say only a play's keyed persist script writes shared model files. But `close-model-gaps` writes them inside a drive.

ADR 043 decided the gap skills. It did not amend ADR 029 §2 or ADR 026's shared-file rule. This ADR does that, so the written rules match what runs.

ADR 043 already amends ADR 026's "Clean tree in, committed delta out" (the drive commits the round once). This ADR does not repeat it.

## Decision

### 1. The Shared Drive Run owns the steps between plays

The Shared Drive Run (`core/components/drives/_shared/drive-run.md`) owns the steps every drive runs between its plays:

- taking the person's write-up (R3);
- reading the source once, into a shared capture (R4b);
- running `find-model-gaps` and then `close-model-gaps` after each round (R5).

These are run steps. They are not rules about the product. So a drive still carries no product rules of its own. Every product rule still lives in the plays.

### 2. Inside a drive, the gap-closing script may write shared model files

Inside a drive, the script of `close-model-gaps` (`apply_links.py`) may:

- write the shared model files — the spine, and the Touches list on intent pages;
- move pages out of the holding folders, to sit under their parent.

It writes only inside `<product_base>product-os/`. It refuses any path outside it. It lists every file it changed in its report.

Outside a drive, nothing changes. A play's keyed persist script is still the only writer of shared model files.

## Consequences

### Positive

- The written rules match what runs. A reviewer no longer finds a conflict between ADR 029, ADR 026 and the shared run.
- The steps every drive needs are written once, in one place, not copied into each play.
- The gaps between plays are closed by the one step that sees all of them.
- The exception is narrow and checked. One script, inside a drive, inside the model folder, with a list of what it changed.

### Negative / Risks

- ADR 026's containment now has two writers of shared files inside a drive: each play's persist script and `apply_links.py`. Their writes to the spine must not clash. ADR 043 has the drive make spine writes in turn; that must hold.
- "No product rules" and "run steps" can blur. A future step added to the Shared Drive Run must be a run step, not a rule about the product. Nothing checks that mechanically.
- `apply_links.py` is not keyed to one node, as a play's persist script is. Its safety rests on the folder check, the agreed `gaps.json`, and its change report.
- Several files still cite the old wording ("no rules of its own", "only the keyed script") and must be updated to point here.

## Alternatives Considered

- **Move the capture, write-up and gap steps into each play** — every play would repeat the same steps. And the gaps between plays can only be closed by something that sees all of them, which is the drive (ADR 043).
- **Route `close-model-gaps` through each play's persist script** — the gaps span plays. No single play owns them, so no single play's script can close them.

## Work This Creates

- `drive-run.md`: say it owns run steps, not product rules, and cite this ADR beside ADR 029.
- `direct-model-write.md`: add the drive exception to rule 3 and to lint L-DMW-5.
- `product-os-keeper.md`: cite this ADR in the shared-file exception.
- `/drive-creator` and `/drive-editor`: update the "no rules of its own" wording in `SKILL.md` and both `lint_drive.py` docstrings.
- The glossary's Drive entry.

## References

- Brief: `.garura/project/issues/_adr/20261021-150850/brief.md`
- `core/components/drives/_shared/drive-run.md`
- `core/components/skills/close-model-gaps/scripts/apply_links.py`
- `core/components/memory/standards/rules/direct-model-write.md`
- ADR 026, ADR 029, ADR 043
