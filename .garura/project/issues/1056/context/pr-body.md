Product ontology version 18: each feature records its own state in the model — `status` on its spine entry only, one of Unplanned, Planned, In progress, Completed or Dropped — and plays read "built" from the model (Completed). It carries ADR 070 into the ontology. The product owner agreed it at the three /specify-ontology checkpoints. Changed kinds: Feature, Capability, ICE (wording), Slice, Plan, Feature issue; Q10, Q50, Q52 change and Q64 to Q71 are added. The spine schema, the skills and the plays change in their own later changes.

Issue: #1056

# Self-review: issue 1056 (the product model records each feature's state)

Rules: the base self-review rules from Phoenix memory (no project override). Branch: feature/1056-ontology-feature-state against main. Diff: `git diff main...HEAD`, 2 commits, 17 files, 2159 lines added and 67 removed (the product ontology is 114 changed lines of it).

Overall: ready to raise. No blocking findings. This review is information for the PR; the approve or reject call is validate-work's.

## What the change is

The second step of issue 1056, after the decision record (ADR 070, already on main). It moves the product ontology from version 17 to 18, so that each feature in the product model records its own state: Unplanned, Planned, In progress, Completed or Dropped. Only a feature has a state; nothing rolls up from features. The old "Built" value, which was worked out from the tracker each time, becomes this stored state. Six kinds change (Capability, Feature, Feature issue, ICE, Plan, Slice), eight questions are added (Q64 to Q71), and the log gets one line. The rest of the diff is the run's own records under the issue folder.

## Scope checks

| Check | Status | Evidence |
|-------|--------|----------|
| Matches the issue | PASS | The issue names this step: "then the ontology change (v18)". The one product file changed is the ontology, and its new rules follow ADR 070 section by section (the five states, who sets each, Dropped coming back as Unplanned, the same Feature issue opening again, a leaving feature going back to Unplanned unless its work started). |
| No scope creep | PASS | The run's own check lists the kinds that changed and the kinds it was allowed to change: both are the same six, with none out of scope. No spine schema, skill, play or script file is touched; ADR 070 lists those as later work. |
| Reasonable size | PASS | One product file, 114 changed lines, and the rest run records of the same shape earlier ontology runs kept (versions 16 and 17). The product owner agreed the questions, the kinds and the links at three checkpoints, each recorded with its reply. |
| No stray artifacts | REVIEW (not blocking) | The run records include a full copy of the ontology as it was before (about 1000 lines), a copy of the ontology template, and three drafts. Versions 16 and 17 kept the same set, so this is accepted practice, but it is most of the line count. |

## Quality checks

| Check | Status | Evidence |
|-------|--------|----------|
| Tests present | PASS (none needed) | A model document, no code. The ontology check reads valid: 14 kinds, 71 questions, no problems found. The change check reads scope ok, version 17 to 18, one new log line, no real name found. |
| Commits are clean | PASS | Two conventional commits, each naming issue 1056: a `feat(ontology)` commit for v18 and a `chore(stm)` commit for the workspace record. No attribution trailer on either. |
| No secrets | PASS | Added lines scanned for keys, tokens, passwords and private-key markers: no match. No home-folder or absolute path in any added line. |
| Docs in step | PASS | The whole-model rule, the flow line, the Feature, Capability, ICE, Slice, Plan and Feature issue kinds, three old questions (Q10, Q50, Q52) and the log all say the same thing. A search for the old wording ("work status", "yet built", "tracker tool" for the built check) finds only the places that still mean something else (a Slice has no work status; the Feature issue lookup by its `Represents` line). |
| Nothing obviously broken | PASS | The branch is 2 commits ahead of main and 0 behind, and a merge test against main gives no conflict. The ontology states every rule in ADR 070 that belongs to it. |

## Findings

1. Low, not blocking: the Feature issue kind still says "Its feature is built only when a person closes the Feature issue." The Feature kind now says the state becomes Completed when its Feature issue closes as completed, including by merging a change that closes it. "A person closes" is a narrower wording than that and "built" is the old word. The two do not conflict, but one pass could align them.
2. Low, not blocking: until the spine schema change lands, the written ontology (version 18) and the spine schema disagree. The ontology says only a feature holds a state, stored as `status`; the spine schema still gives every domain, capability and feature entry the old `status` (proposed, active, deprecated). ADR 070 names the spine schema, link-model-part and the play scripts as the follow-on work, so this is the planned order, not a defect. The ontology also lists the Feature `Status` as required, and today's features have no such value until the model clean-up marks them.
3. Low, not blocking: the work-start records of the earlier ADR step (the issue text copy, the "created" mark and the branch name) were overwritten by this step's start record. The issue text itself still lives in the tracker, and the earlier step's own records are in the history of main.
4. Note: the ontology in Phoenix memory is still version 15 until it is promoted, so agents that read Phoenix memory do not see the state yet. ADR 070 records this under Risks.

## Automated checks

- Merge test against main: no conflict (0 commits behind, 2 ahead).
- Secret scan, home-path scan, attribution scan and closing-keyword scan over the added lines: no match.
- The run's own ontology check (valid, 14 kinds, 71 questions, no problems) and change check (scope ok, version ok, no real names) were read and agree with the diff.
