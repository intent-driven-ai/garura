## What this adds

`/adr` — a play, skill and sub-agent that manage decision records (ADRs), in every form:

- **One template** in core memory, `standards/templates/adr.md`, with one set of core fields and two shapes: Markdown for Garura's own ADRs (`docs/adr/`), `decision.yaml` records for product decisions. `decision.yaml` moves to v2 — the new fields are additive (migration note included).
- **`author-adr`** (skill) drafts an ADR from the template, always as proposed. Its `scripts/adr.py` does the mechanical work: next number, lint, index, overlap candidates, forward pointers, accept, and the business-intent guard (33 tests).
- **`adr-keeper`** (sub-agent) gathers the context — which older ADRs the decision supersedes or amends (with the part), what it affects, its ICE impact, its business-intent check — has the skill draft it, and checks it.
- **`/adr`** (play), compiled from the intent Kapil approved: run by hand, a pinned approval before anything is accepted; inside a drive, saved as proposed and accepted at the drive's final review (`/adr accept <file>`). Older ADRs gain only a forward pointer, written after acceptance; the ADR index is rebuilt. A decision that would change a person's business intent is shown to the person and never applied. `apply_adr.py` and `check_adr_scope.py` (20 tests). Its accept step is added to the pinned gates.
- **Starts managing the ADRs here:** `/adr` is in the harness install; `docs/adr/_index.md` lists all 31 existing ADRs. Existing ADRs stay as written for now (decision A4).

## How it was tried

On ADR 031 as if new: a brief with no ADR numbers in it, against the ADR folder from before ADR 031 existed. It found ADR 026, 027 and 029 on its own, each with the right part, judged nine other candidates not affected, marked the business-intent check `kind`, and the drive, accept-later, pointer and index paths all worked. Records: `.garura/project/issues/632/specs/trial-adr-031/`.

Design decisions A1–A8 with Kapil: `.garura/project/issues/632/specs/plan.md`.

Closes #632

## Self-review

# Self-review — #632 /adr play, author-adr skill, adr-keeper agent

Rules source: ~/.garura/core/memory/standards/rules/self-review.md (base, not overridden).
Diff reviewed: origin/main...HEAD on feature/632-adr-play. 9 commits, 38 files. Excluding the issue's own
STM records, 24 files and about 3,100 added lines.

Informational only. Nothing here stops the raise. Findings marked [WARN] are worth a look; none is a defect in the change's own goal.

## Scope checks

- [PASS] Matches the issue. Every changed file serves the ADR manager: the ADR template, the decision record schema (v2), the author-adr skill, the adr-keeper agent, the /adr play with its scripts, the install wiring, the ADR index, and the docs for the agent and skill.
- [PASS] No scope creep. The only edits to existing files are small: gate-config.md (one sentence on the ADR accept gate), pipeline-next.md (one line for `adr`), the schema index, install.py (adds the three new components to the harness scope), the install manifest, agents.md and skills.md.
- [PASS] Reasonable size. About 3,100 lines of new code and prose, but it lands as seven separate commits, one concern each (template, skill, agent, play, install, docs, records), so it can be reviewed one piece at a time.
- [PASS] No stray artifacts. No commented-out blocks, no leftover TODO or debug prints. The `print` calls in the scripts are their JSON output, which is how they report. The scratch trial files under specs/trial-adr-031 are deliberate trial evidence for this issue, kept like the other issues' records.
- [PASS] Deliberate duplicate is in sync. plays/adr/scripts/adr.py and skills/author-adr/scripts/adr.py are byte-for-byte identical (checked with cmp).
- [WARN] One uncommitted file sits in the tree: .garura/project/issues/632/context/resolved-rules.json, written by this very review run. It is a run record, not part of the change. Commit it with the records or leave it out.

## Quality checks

- [PASS] Tests present. test_adr.py: 33 passed, 0 failed. test_apply_adr.py: 20 passed, 0 failed. Both ran clean in this review.
- [PASS] Play lint. lint_play.py on plays/adr/SKILL.md: verdict PASS, 0 gaps (all 13 checks pass, including the standard play close, stop condition and next-command).
- [WARN] Ruff reports 2 style findings, both E741 (a variable named `l`): plays/adr/scripts/preflight.py line 127 and plays/adr/scripts/session_stamp.py line 49. No other ruff findings across the new .py files. Cosmetic, does not change behavior. Fix by renaming `l` to `line`.
- [PASS] Commits are clean. All 9 use conventional format (feat, chore, docs), each is one concern, and each references #632.
- [PASS] No secrets. A scan of the added lines for keys, tokens, passwords and private-key headers found only the word "token" in prose about inference cost and path tokens. No credentials.
- [WARN] Docs partly in step. The agent roster (agents.md) and the skills list (skills.md) are updated, and the ADR index is added. The "Complete Play Roster" table in docs/components/plays.md has no row for the new `adr` play, while its sibling `intent` play is listed. Add one row.
- [PASS] Nothing obviously broken. The play's intent source (reference/ice.md) is present beside the compiled SKILL.md, so the intent-to-play path is kept. The install manifest counts moved consistently (agents 4 to 5, skills 11 to 12, plays 8 to 9) with the install.py scope change.

## Summary

Ten items pass cleanly, three are [WARN] and informational: the stray run record, the two `l` variable names, and the missing row in the plays roster doc. Zero items are marked as failing.

## After the review

The play roster gap was fixed before the push (the `/adr` row in docs/components/plays.md). The two E741 warnings are in the shared preflight.py and session_stamp.py, copied unchanged into every play; they are a recorded follow-up from #612.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
