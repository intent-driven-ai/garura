# Self-review: issue 1056 (the product model records each feature's state)

Rules: the base self-review rules from Phoenix memory (no project override). Branch: feature/1056-feature-state-in-model against main. Diff: `git diff main...HEAD`, 2 commits, 23 files, 1065 lines added.

Overall: ready to raise. No blocking findings. This review is information for the PR; the approve or reject call is validate-work's.

## What the change is

The first step of issue 1056: the decision record that lets each feature in the product model hold its own state (Unplanned, Planned, In progress, Completed, Dropped). It adds ADR 070, puts forward pointers on ADR 068 and ADR 069, rebuilds the ADR index, and keeps the run records of the decision.

## Scope checks

| Check | Status | Evidence |
|-------|--------|----------|
| Matches the issue | PASS | The issue text names this step: "a decision record that amends ADR 069 ... then the ontology change". The diff holds that decision record and nothing of the ontology change. |
| No scope creep | PASS | Every file is the ADR, its two forward pointers, the index, or run records under the issue and decision folders. No ontology, spine, skill or play file is touched; ADR 070 lists them under "Affects" and "Work This Creates" for later work. |
| Reasonable size | PASS | One decision file of 157 lines, three one-line pointer or index edits, and about 900 lines of run records. Easy to review in one sitting; the real review surface is the ADR. |
| No stray artifacts | REVIEW (not blocking) | The run records keep a first draft (`adr-draft-v1.md`) beside the final one and a copy of the ADR template. This matches how earlier decision runs are kept, so it is accepted practice, but a reviewer may prefer fewer copies. |

## Quality checks

| Check | Status | Evidence |
|-------|--------|----------|
| Tests present | PASS (none needed) | Docs and run records only; no behavior change. The decision's own lint and business-intent guard both ran clean (recorded in the run's check file: lint valid, guard "no person's business intent changes"). |
| Commits are clean | PASS | Two conventional commits, each naming issue 1056: a `docs(adr)` commit for the decision and a `chore(stm)` commit for the workspace record. |
| No secrets | PASS | Added lines scanned for keys, tokens, passwords and private-key markers: no match. |
| Docs in step | PASS | The index lists ADR 070 and adds "amended in part by 070" to ADR 068 and ADR 069, matching the Status lines on both. |
| Nothing obviously broken | PASS | The line numbers ADR 070 cites in the ontology (lines 23, 178, 184, 398, 417, 445, 464, 509, 558, 671, 775, 802, 809) and in the spine schema (lines 45, 74, 110) were spot-checked and point at the text the ADR describes. |

## Findings

1. Low, not blocking: one committed run record (the decision's manifest) holds a full machine path with the home folder in it. It sits under the run records, not in the ADR. Other run records may need the same check; Fixed before the push: the path now reads repo-relative, and a scan of the branch finds no home-folder path.
2. Low, not blocking: ADR 070 says removing the old status touches 280 entries and gives 239 features. These counts were not re-checked here; the later clean-up work will confirm them against the spine.
3. Note: ADR 070 reads "Accepted" and ADR 069's line "The model does not go out of date when a plan, an epic or an issue changes" no longer holds in full. The ADR states this itself under Risks, so no action here.

## Automated checks

- No merge conflict check was run beyond the diff read; the branch is two commits ahead of main with no files in common with main's newer changes beyond the ADR index and the two ADR Status lines.
- No attribution line and no closing keyword before an issue number in the added text.
